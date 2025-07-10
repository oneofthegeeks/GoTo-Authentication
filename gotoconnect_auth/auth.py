"""
Main authentication module for GoTo Connect APIs.
"""

import os
import time
import webbrowser
import requests
from urllib.parse import urlencode, parse_qs, urlparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from typing import Dict, Optional, Any, Union
from dotenv import load_dotenv

from .storage import TokenStorage, KeyringTokenStorage
from .exceptions import (
    GoToConnectAuthError,
    AuthenticationError,
    TokenExpiredError,
    ConfigurationError,
    NetworkError
)


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """HTTP server to handle OAuth callback."""
    
    def __init__(self, *args, auth_instance=None, **kwargs):
        self.auth_instance = auth_instance
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET request for OAuth callback."""
        try:
            # Parse the authorization code from the callback URL
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            if 'code' in query_params:
                auth_code = query_params['code'][0]
                self.auth_instance._auth_code = auth_code
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response_html = """
                <html>
                <body>
                    <h1>Authentication Successful!</h1>
                    <p>You can close this window now.</p>
                    <script>window.close();</script>
                </body>
                </html>
                """
                self.wfile.write(response_html.encode())
            else:
                # Send error response
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                response_html = """
                <html>
                <body>
                    <h1>Authentication Failed!</h1>
                    <p>No authorization code received.</p>
                </body>
                </html>
                """
                self.wfile.write(response_html.encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response_html = f"""
            <html>
            <body>
                <h1>Authentication Error!</h1>
                <p>Error: {str(e)}</p>
            </body>
            </html>
            """
            self.wfile.write(response_html.encode())


class GoToConnectAuth:
    """Main authentication class for GoTo Connect APIs."""
    
    # GoTo Connect OAuth endpoints
    AUTH_URL = "https://authentication.logmeininc.com/oauth/authorize"
    TOKEN_URL = "https://authentication.logmeininc.com/oauth/token"
    
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str = "http://localhost:8080/callback",
        token_storage: Optional[TokenStorage] = None,
        auth_url: Optional[str] = None,
        token_url: Optional[str] = None
    ):
        """
        Initialize the GoTo Connect authentication client.
        
        Args:
            client_id: Your GoTo Connect application client ID
            client_secret: Your GoTo Connect application client secret
            redirect_uri: OAuth redirect URI
            token_storage: Token storage backend (defaults to KeyringTokenStorage)
            auth_url: Custom authorization URL
            token_url: Custom token URL
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.auth_url = auth_url or self.AUTH_URL
        self.token_url = token_url or self.TOKEN_URL
        
        # Initialize token storage
        self.token_storage = token_storage or KeyringTokenStorage()
        
        # Token state
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[int] = None
        self._auth_code: Optional[str] = None
        
        # Load existing tokens
        self._load_tokens()
    
    @classmethod
    def from_env(cls, **kwargs) -> 'GoToConnectAuth':
        """Create instance from environment variables."""
        load_dotenv()
        
        client_id = os.getenv('GOTO_CLIENT_ID')
        client_secret = os.getenv('GOTO_CLIENT_SECRET')
        redirect_uri = os.getenv('GOTO_REDIRECT_URI', 'http://localhost:8080/callback')
        auth_url = os.getenv('GOTO_AUTH_URL')
        token_url = os.getenv('GOTO_TOKEN_URL')
        
        if not client_id or not client_secret:
            raise ConfigurationError(
                "Missing required environment variables: GOTO_CLIENT_ID and GOTO_CLIENT_SECRET"
            )
        
        return cls(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            auth_url=auth_url,
            token_url=token_url,
            **kwargs
        )
    
    @classmethod
    def from_config(cls, config_path: str, **kwargs) -> 'GoToConnectAuth':
        """Create instance from configuration file."""
        import json
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            raise ConfigurationError(f"Failed to load config file {config_path}: {e}")
        
        required_fields = ['client_id', 'client_secret']
        for field in required_fields:
            if field not in config:
                raise ConfigurationError(f"Missing required field in config: {field}")
        
        return cls(
            client_id=config['client_id'],
            client_secret=config['client_secret'],
            redirect_uri=config.get('redirect_uri', 'http://localhost:8080/callback'),
            auth_url=config.get('auth_url'),
            token_url=config.get('token_url'),
            **kwargs
        )
    
    def authenticate(self) -> None:
        """Perform OAuth 2.0 authentication."""
        # Check if already authenticated
        if self.is_authenticated():
            return
        
        # Check if we have a refresh token
        if self._refresh_token:
            try:
                self.refresh_token()
                return
            except TokenExpiredError:
                # Refresh token is expired, need to re-authenticate
                pass
        
        # Perform OAuth 2.0 authorization code flow
        self._perform_oauth_flow()
    
    def _perform_oauth_flow(self) -> None:
        """Perform the OAuth 2.0 authorization code flow."""
        # Start local server to handle callback
        server = self._start_callback_server()
        
        try:
            # Generate authorization URL
            auth_params = {
                'response_type': 'code',
                'client_id': self.client_id,
                'redirect_uri': self.redirect_uri,
                'scope': 'meetings:read meetings:write users:read',
                'state': 'random_state_string'
            }
            
            auth_url = f"{self.auth_url}?{urlencode(auth_params)}"
            
            # Open browser for user authorization
            print(f"Opening browser for authentication...")
            webbrowser.open(auth_url)
            
            # Wait for callback
            while not self._auth_code:
                time.sleep(0.1)
            
            # Exchange authorization code for tokens
            self._exchange_code_for_tokens()
            
        finally:
            # Stop the callback server
            server.shutdown()
            server.server_close()
    
    def _start_callback_server(self) -> HTTPServer:
        """Start local HTTP server to handle OAuth callback."""
        parsed_uri = urlparse(self.redirect_uri)
        port = parsed_uri.port or 8080
        
        # Create custom handler class with auth instance
        class Handler(OAuthCallbackHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, auth_instance=self, **kwargs)
        
        server = HTTPServer(('localhost', port), Handler)
        
        # Start server in a separate thread
        server_thread = Thread(target=server.serve_forever, daemon=True)
        server_thread.start()
        
        return server
    
    def _exchange_code_for_tokens(self) -> None:
        """Exchange authorization code for access and refresh tokens."""
        if not self._auth_code:
            raise AuthenticationError("No authorization code available")
        
        token_data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': self._auth_code,
            'redirect_uri': self.redirect_uri
        }
        
        try:
            response = requests.post(self.token_url, data=token_data)
            response.raise_for_status()
            
            tokens = response.json()
            self._process_tokens(tokens)
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to exchange code for tokens: {e}")
        except Exception as e:
            raise AuthenticationError(f"Failed to exchange code for tokens: {e}")
    
    def refresh_token(self) -> None:
        """Refresh the access token using the refresh token."""
        if not self._refresh_token:
            raise TokenExpiredError("No refresh token available")
        
        token_data = {
            'grant_type': 'refresh_token',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self._refresh_token
        }
        
        try:
            response = requests.post(self.token_url, data=token_data)
            response.raise_for_status()
            
            tokens = response.json()
            self._process_tokens(tokens)
            
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"Failed to refresh token: {e}")
        except Exception as e:
            raise TokenExpiredError(f"Failed to refresh token: {e}")
    
    def _process_tokens(self, tokens: Dict[str, Any]) -> None:
        """Process and store tokens."""
        self._access_token = tokens.get('access_token')
        self._refresh_token = tokens.get('refresh_token', self._refresh_token)
        
        # Calculate token expiration
        expires_in = tokens.get('expires_in', 3600)
        self._token_expires_at = int(time.time()) + expires_in
        
        # Save tokens to storage
        self._save_tokens()
    
    def _load_tokens(self) -> None:
        """Load tokens from storage."""
        tokens = self.token_storage.load_tokens()
        if tokens:
            self._access_token = tokens.get('access_token')
            self._refresh_token = tokens.get('refresh_token')
            self._token_expires_at = tokens.get('expires_at')
    
    def _save_tokens(self) -> None:
        """Save tokens to storage."""
        tokens = {
            'access_token': self._access_token,
            'refresh_token': self._refresh_token,
            'expires_at': self._token_expires_at
        }
        self.token_storage.save_tokens(tokens)
    
    def is_authenticated(self) -> bool:
        """Check if currently authenticated."""
        if not self._access_token:
            return False
        
        # Check if token is expired
        if self._token_expires_at and time.time() >= self._token_expires_at:
            # Try to refresh the token
            try:
                self.refresh_token()
            except TokenExpiredError:
                return False
        
        return bool(self._access_token)
    
    def get_access_token(self) -> Optional[str]:
        """Get the current access token."""
        if self.is_authenticated():
            return self._access_token
        return None
    
    def logout(self) -> None:
        """Clear stored credentials."""
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None
        self.token_storage.clear_tokens()
    
    def _ensure_authenticated(self) -> None:
        """Ensure we have a valid access token."""
        if not self.is_authenticated():
            self.authenticate()
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        self._ensure_authenticated()
        return {
            'Authorization': f'Bearer {self._access_token}',
            'Content-Type': 'application/json'
        }
    
    def get(self, url: str, **kwargs) -> requests.Response:
        """Make a GET request with authentication."""
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        try:
            response = requests.get(url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"GET request failed: {e}")
    
    def post(self, url: str, **kwargs) -> requests.Response:
        """Make a POST request with authentication."""
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        try:
            response = requests.post(url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"POST request failed: {e}")
    
    def put(self, url: str, **kwargs) -> requests.Response:
        """Make a PUT request with authentication."""
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        try:
            response = requests.put(url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"PUT request failed: {e}")
    
    def delete(self, url: str, **kwargs) -> requests.Response:
        """Make a DELETE request with authentication."""
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        try:
            response = requests.delete(url, headers=headers, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise NetworkError(f"DELETE request failed: {e}") 