"""
Unit tests for GoTo Connect Authentication Library.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import os
from datetime import datetime, timedelta

from gotoconnect_auth import GoToConnectAuth
from gotoconnect_auth.storage import KeyringTokenStorage, FileTokenStorage, MemoryTokenStorage
from gotoconnect_auth.exceptions import (
    GoToConnectAuthError,
    AuthenticationError,
    TokenExpiredError,
    ConfigurationError
)


class TestTokenStorage(unittest.TestCase):
    """Test token storage backends."""
    
    def setUp(self):
        self.test_tokens = {
            'access_token': 'test_access_token',
            'refresh_token': 'test_refresh_token',
            'expires_at': int(datetime.now().timestamp()) + 3600
        }
    
    def test_memory_storage(self):
        """Test memory token storage."""
        storage = MemoryTokenStorage()
        
        # Test save and load
        storage.save_tokens(self.test_tokens)
        loaded_tokens = storage.load_tokens()
        self.assertEqual(loaded_tokens, self.test_tokens)
        
        # Test clear
        storage.clear_tokens()
        self.assertIsNone(storage.load_tokens())
    
    def test_file_storage(self):
        """Test file token storage."""
        test_file = "test_tokens.json"
        storage = FileTokenStorage(test_file)
        
        try:
            # Test save and load
            storage.save_tokens(self.test_tokens)
            loaded_tokens = storage.load_tokens()
            self.assertEqual(loaded_tokens, self.test_tokens)
            
            # Test clear
            storage.clear_tokens()
            self.assertIsNone(storage.load_tokens())
            
        finally:
            # Clean up
            if os.path.exists(test_file):
                os.remove(test_file)
    
    @patch('keyring.set_password')
    @patch('keyring.get_password')
    @patch('keyring.delete_password')
    def test_keyring_storage(self, mock_delete, mock_get, mock_set):
        """Test keyring token storage."""
        storage = KeyringTokenStorage()
        
        # Mock keyring responses
        mock_get.return_value = json.dumps(self.test_tokens)
        
        # Test save
        storage.save_tokens(self.test_tokens)
        mock_set.assert_called_once()
        
        # Test load
        loaded_tokens = storage.load_tokens()
        self.assertEqual(loaded_tokens, self.test_tokens)
        
        # Test clear
        storage.clear_tokens()
        mock_delete.assert_called_once()


class TestGoToConnectAuth(unittest.TestCase):
    """Test the main authentication class."""
    
    def setUp(self):
        self.auth = GoToConnectAuth(
            client_id="test_client_id",
            client_secret="test_client_secret",
            redirect_uri="http://localhost:8080/callback"
        )
    
    def test_initialization(self):
        """Test auth initialization."""
        self.assertEqual(self.auth.client_id, "test_client_id")
        self.assertEqual(self.auth.client_secret, "test_client_secret")
        self.assertEqual(self.auth.redirect_uri, "http://localhost:8080/callback")
        self.assertIsInstance(self.auth.token_storage, KeyringTokenStorage)
    
    @patch.dict(os.environ, {
        'GOTO_CLIENT_ID': 'env_client_id',
        'GOTO_CLIENT_SECRET': 'env_client_secret'
    })
    def test_from_env(self):
        """Test creating auth instance from environment variables."""
        auth = GoToConnectAuth.from_env()
        self.assertEqual(auth.client_id, "env_client_id")
        self.assertEqual(auth.client_secret, "env_client_secret")
    
    def test_from_env_missing_vars(self):
        """Test from_env with missing environment variables."""
        with self.assertRaises(ConfigurationError):
            GoToConnectAuth.from_env()
    
    def test_from_config(self):
        """Test creating auth instance from config file."""
        config_data = {
            'client_id': 'config_client_id',
            'client_secret': 'config_client_secret',
            'redirect_uri': 'http://localhost:8081/callback'
        }
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(config_data)
            
            auth = GoToConnectAuth.from_config("config.json")
            self.assertEqual(auth.client_id, "config_client_id")
            self.assertEqual(auth.client_secret, "config_client_secret")
            self.assertEqual(auth.redirect_uri, "http://localhost:8081/callback")
    
    def test_from_config_missing_file(self):
        """Test from_config with missing config file."""
        with self.assertRaises(ConfigurationError):
            GoToConnectAuth.from_config("nonexistent.json")
    
    def test_from_config_missing_fields(self):
        """Test from_config with missing required fields."""
        config_data = {'client_id': 'test'}  # Missing client_secret
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(config_data)
            
            with self.assertRaises(ConfigurationError):
                GoToConnectAuth.from_config("config.json")
    
    def test_is_authenticated_no_token(self):
        """Test is_authenticated when no token is available."""
        self.assertFalse(self.auth.is_authenticated())
    
    def test_is_authenticated_with_valid_token(self):
        """Test is_authenticated with a valid token."""
        # Mock token storage to return valid tokens
        mock_tokens = {
            'access_token': 'valid_token',
            'refresh_token': 'refresh_token',
            'expires_at': int(datetime.now().timestamp()) + 3600
        }
        
        with patch.object(self.auth.token_storage, 'load_tokens', return_value=mock_tokens):
            self.auth._load_tokens()
            self.assertTrue(self.auth.is_authenticated())
    
    def test_is_authenticated_with_expired_token(self):
        """Test is_authenticated with an expired token."""
        # Mock token storage to return expired tokens
        mock_tokens = {
            'access_token': 'expired_token',
            'refresh_token': 'refresh_token',
            'expires_at': int(datetime.now().timestamp()) - 3600  # Expired
        }
        
        with patch.object(self.auth.token_storage, 'load_tokens', return_value=mock_tokens):
            self.auth._load_tokens()
            # Mock refresh to fail
            with patch.object(self.auth, 'refresh_token', side_effect=TokenExpiredError("Token expired")):
                self.assertFalse(self.auth.is_authenticated())
    
    def test_logout(self):
        """Test logout functionality."""
        # Set some tokens
        self.auth._access_token = "test_token"
        self.auth._refresh_token = "test_refresh"
        self.auth._token_expires_at = 123456789
        
        # Mock token storage clear
        with patch.object(self.auth.token_storage, 'clear_tokens') as mock_clear:
            self.auth.logout()
            
            # Check that tokens are cleared
            self.assertIsNone(self.auth._access_token)
            self.assertIsNone(self.auth._refresh_token)
            self.assertIsNone(self.auth._token_expires_at)
            
            # Check that storage clear was called
            mock_clear.assert_called_once()
    
    @patch('requests.post')
    def test_refresh_token_success(self, mock_post):
        """Test successful token refresh."""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = {
            'access_token': 'new_access_token',
            'refresh_token': 'new_refresh_token',
            'expires_in': 3600
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Set up refresh token
        self.auth._refresh_token = "old_refresh_token"
        
        # Test refresh
        self.auth.refresh_token()
        
        # Check that tokens were updated
        self.assertEqual(self.auth._access_token, "new_access_token")
        self.assertEqual(self.auth._refresh_token, "new_refresh_token")
    
    def test_refresh_token_no_refresh_token(self):
        """Test refresh token when no refresh token is available."""
        with self.assertRaises(TokenExpiredError):
            self.auth.refresh_token()
    
    @patch('requests.post')
    def test_refresh_token_failure(self, mock_post):
        """Test token refresh failure."""
        # Mock failed response
        mock_post.side_effect = Exception("Network error")
        
        self.auth._refresh_token = "test_refresh_token"
        
        with self.assertRaises(TokenExpiredError):
            self.auth.refresh_token()


class TestHTTPMethods(unittest.TestCase):
    """Test HTTP method wrappers."""
    
    def setUp(self):
        self.auth = GoToConnectAuth(
            client_id="test_client_id",
            client_secret="test_client_secret"
        )
        
        # Mock authentication
        self.auth._access_token = "test_token"
        self.auth._token_expires_at = int(datetime.now().timestamp()) + 3600
    
    @patch('requests.get')
    def test_get_request(self, mock_get):
        """Test GET request wrapper."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = self.auth.get("https://api.goto.com/test")
        
        # Check that request was made with correct headers
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertEqual(call_args[0][0], "https://api.goto.com/test")
        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Content-Type', call_args[1]['headers'])
    
    @patch('requests.post')
    def test_post_request(self, mock_post):
        """Test POST request wrapper."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        response = self.auth.post("https://api.goto.com/test", json={"test": "data"})
        
        # Check that request was made with correct headers
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], "https://api.goto.com/test")
        self.assertIn('Authorization', call_args[1]['headers'])
        self.assertIn('Content-Type', call_args[1]['headers'])


if __name__ == '__main__':
    unittest.main() 