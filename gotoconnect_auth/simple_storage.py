"""
Simplified token storage for GoTo Connect Authentication Library.
"""

import json
import os
import keyring
from abc import ABC, abstractmethod
from typing import Dict, Optional, Any
from .exceptions import TokenStorageError


class TokenStorage(ABC):
    """Abstract base class for token storage."""
    
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


class SecureTokenStorage(TokenStorage):
    """Secure token storage using system keyring with file fallback."""
    
    def __init__(self, service_name: str = "gotoconnect-auth", username: str = "default"):
        self.service_name = service_name
        self.username = username
        self.fallback_file = "tokens.json"
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to secure storage."""
        try:
            # Try keyring first
            keyring.set_password(
                self.service_name,
                self.username,
                json.dumps(tokens)
            )
        except Exception:
            # Fallback to file storage
            try:
                with open(self.fallback_file, 'w') as f:
                    json.dump(tokens, f, indent=2)
            except Exception as e:
                raise TokenStorageError(f"Failed to save tokens: {e}")
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from secure storage."""
        try:
            # Try keyring first
            tokens_json = keyring.get_password(self.service_name, self.username)
            if tokens_json:
                return json.loads(tokens_json)
        except Exception:
            pass
        
        # Fallback to file storage
        try:
            if os.path.exists(self.fallback_file):
                with open(self.fallback_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        
        return None
    
    def clear_tokens(self) -> None:
        """Clear tokens from storage."""
        try:
            keyring.delete_password(self.service_name, self.username)
        except Exception:
            pass
        
        # Clear file storage too
        try:
            if os.path.exists(self.fallback_file):
                os.remove(self.fallback_file)
        except Exception:
            pass


class FileTokenStorage(TokenStorage):
    """Simple file-based token storage."""
    
    def __init__(self, file_path: str = "tokens.json"):
        self.file_path = file_path
    
    def save_tokens(self, tokens: Dict[str, Any]) -> None:
        """Save tokens to file."""
        try:
            with open(self.file_path, 'w') as f:
                json.dump(tokens, f, indent=2)
        except Exception as e:
            raise TokenStorageError(f"Failed to save tokens to file: {e}")
    
    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Load tokens from file."""
        try:
            if not os.path.exists(self.file_path):
                return None
            
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise TokenStorageError(f"Failed to load tokens from file: {e}")
    
    def clear_tokens(self) -> None:
        """Clear tokens by deleting file."""
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
        except Exception as e:
            raise TokenStorageError(f"Failed to clear tokens: {e}")


class MemoryTokenStorage(TokenStorage):
    """In-memory token storage (not persistent)."""
    
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
