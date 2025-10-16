"""
GoTo Connect Authentication Library

A simple, reusable Python library for authenticating with GoTo Connect APIs.
"""

from .simple_auth import GoToConnectAuth
from .simple_storage import SecureTokenStorage, FileTokenStorage, MemoryTokenStorage
from .exceptions import GoToConnectAuthError, AuthenticationError, TokenExpiredError, ConfigurationError

__version__ = "1.0.0"
__author__ = "GoTo Connect Auth Library"
__email__ = "support@example.com"

__all__ = [
    "GoToConnectAuth",
    "SecureTokenStorage",
    "FileTokenStorage", 
    "MemoryTokenStorage",
    "GoToConnectAuthError",
    "AuthenticationError",
    "TokenExpiredError",
    "ConfigurationError",
]