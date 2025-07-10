"""
Custom exceptions for GoTo Connect Authentication Library.
"""


class GoToConnectAuthError(Exception):
    """Base exception for GoTo Connect authentication errors."""
    pass


class AuthenticationError(GoToConnectAuthError):
    """Raised when authentication fails."""
    pass


class TokenExpiredError(GoToConnectAuthError):
    """Raised when the access token has expired and cannot be refreshed."""
    pass


class ConfigurationError(GoToConnectAuthError):
    """Raised when there's an issue with the configuration."""
    pass


class TokenStorageError(GoToConnectAuthError):
    """Raised when there's an issue with token storage."""
    pass


class NetworkError(GoToConnectAuthError):
    """Raised when there's a network-related error."""
    pass 