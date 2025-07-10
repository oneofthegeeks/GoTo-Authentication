"""
GoTo Connect Authentication Library

A reusable Python library for authenticating with GoTo Connect APIs.
"""

from .auth import GoToConnectAuth
from .storage import KeyringTokenStorage, FileTokenStorage, MemoryTokenStorage
from .exceptions import GoToConnectAuthError, TokenExpiredError, AuthenticationError

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "GoToConnectAuth",
    "KeyringTokenStorage",
    "FileTokenStorage", 
    "MemoryTokenStorage",
    "GoToConnectAuthError",
    "TokenExpiredError",
    "AuthenticationError",
] 