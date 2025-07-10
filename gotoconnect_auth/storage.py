"""
Token storage backends for GoTo Connect Authentication Library.
"""

import json
import os
import keyring
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from .exceptions import TokenStorageError


class TokenStorage(ABC):
    """Abstract base class for token storage backends."""
    
    @abstractmethod
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to storage."""
        pass
    
    @abstractmethod
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from storage."""
        pass
    
    @abstractmethod
    def clear_tokens(self) -> None:
        """Clear tokens from storage."""
        pass


class KeyringTokenStorage(TokenStorage):
    """Token storage using system keyring for secure storage."""
    
    def __init__(self, service_name: str = "gotoconnect-auth", username: str = "default"):
        self.service_name = service_name
        self.username = username
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to system keyring."""
        try:
            keyring.set_password(
                self.service_name,
                self.username,
                json.dumps(tokens)
            )
        except Exception as e:
            raise TokenStorageError(f"Failed to save tokens to keyring: {e}")
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from system keyring."""
        try:
            tokens_json = keyring.get_password(self.service_name, self.username)
            if tokens_json:
                return json.loads(tokens_json)
            return None
        except Exception as e:
            raise TokenStorageError(f"Failed to load tokens from keyring: {e}")
    
    def clear_tokens(self) -> None:
        """Clear tokens from system keyring."""
        try:
            keyring.delete_password(self.service_name, self.username)
        except Exception as e:
            raise TokenStorageError(f"Failed to clear tokens from keyring: {e}")


class FileTokenStorage(TokenStorage):
    """Token storage using a JSON file."""
    
    def __init__(self, file_path: str = "tokens.json"):
        self.file_path = file_path
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to JSON file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(tokens, f, indent=2)
        except Exception as e:
            raise TokenStorageError(f"Failed to save tokens to file {self.file_path}: {e}")
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from JSON file."""
        try:
            if not os.path.exists(self.file_path):
                return None
            
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise TokenStorageError(f"Failed to load tokens from file {self.file_path}: {e}")
    
    def clear_tokens(self) -> None:
        """Clear tokens by deleting the file."""
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
        except Exception as e:
            raise TokenStorageError(f"Failed to clear tokens from file {self.file_path}: {e}")


class MemoryTokenStorage(TokenStorage):
    """Token storage using in-memory storage (not persistent)."""
    
    def __init__(self):
        self._tokens: Optional[Dict[str, Any]] = None
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to memory."""
        self._tokens = tokens.copy()
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from memory."""
        return self._tokens.copy() if self._tokens else None
    
    def clear_tokens(self) -> None:
        """Clear tokens from memory."""
        self._tokens = None 