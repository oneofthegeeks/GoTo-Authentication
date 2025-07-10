# GoTo Connect Authentication Library

A reusable Python library for authenticating with GoTo Connect APIs. This library handles OAuth 2.0 authentication, token refresh, and secure credential storage.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/gotoconnect-auth.svg)](https://badge.fury.io/py/gotoconnect-auth)

## 🚀 Quick Start

```bash
# Install the library
pip install gotoconnect-auth

# Or install from source
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth
pip install -e .
```

```python
from gotoconnect_auth import GoToConnectAuth

# Initialize with your credentials
auth = GoToConnectAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Authenticate and make API calls
auth.authenticate()
response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
print(response.json())
```

## Features

- **OAuth 2.0 Authentication**: Complete OAuth 2.0 flow for GoTo Connect APIs
- **Automatic Token Refresh**: Handles token expiration and automatic refresh
- **Secure Credential Storage**: Uses system keyring for secure storage of credentials
- **Environment Variable Support**: Load credentials from environment variables
- **Easy Integration**: Simple API for including in other projects
- **Error Handling**: Comprehensive error handling and logging

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- A GoTo Connect developer account
- Your GoTo Connect application credentials

### Install from PyPI

```bash
pip install gotoconnect-auth
```

### Install from Source

```bash
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth
pip install -e .
```

### Quick Setup

Run the included setup script to install dependencies and create configuration files:

```bash
python install.py
```

## 🔧 Setup

### 1. Get Your GoTo Connect Credentials

1. Go to the [GoTo Connect Developer Portal](https://developer.goto.com/)
2. Create a new application or use an existing one
3. Note your **Client ID** and **Client Secret**
4. Set the redirect URI to `http://localhost:8080/callback`

### 2. Configure Your Credentials

#### Option A: Environment Variables (Recommended)

Create a `.env` file in your project directory:

```env
GOTO_CLIENT_ID=YOUR_CLIENT_ID_HERE
GOTO_CLIENT_SECRET=YOUR_CLIENT_SECRET_HERE
GOTO_REDIRECT_URI=http://localhost:8080/callback
```

#### Option B: Configuration File

Create a `config.json` file:

```json
{
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uri": "http://localhost:8080/callback"
}
```

### 3. Basic Usage

```python
from gotoconnect_auth import GoToConnectAuth

# Method 1: Direct initialization
auth = GoToConnectAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8080/callback"
)

# Method 2: From environment variables
auth = GoToConnectAuth.from_env()

# Method 3: From configuration file
auth = GoToConnectAuth.from_config("config.json")

# Authenticate (opens browser for first-time auth)
auth.authenticate()

# Make API calls
response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
print(response.json())
```

## 🔧 Advanced Usage

### Custom Token Storage

```python
from gotoconnect_auth import GoToConnectAuth, FileTokenStorage

# Use file-based storage instead of keyring
auth = GoToConnectAuth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET",
    redirect_uri="http://localhost:8080/callback",
    token_storage=FileTokenStorage("tokens.json")
)
```

### Manual Token Management

```python
# Check if authenticated
if auth.is_authenticated():
    print("Already authenticated!")
else:
    auth.authenticate()

# Get current access token
token = auth.get_access_token()

# Refresh token manually
auth.refresh_token()
```

### Error Handling

```python
from gotoconnect_auth import GoToConnectAuthError

try:
    auth = GoToConnectAuth.from_env()
    auth.authenticate()
    response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
except GoToConnectAuthError as e:
    print(f"Authentication error: {e}")
except Exception as e:
    print(f"API error: {e}")
```

## API Reference

### GoToConnectAuth

Main authentication class for GoTo Connect APIs.

#### Methods

- `authenticate()`: Perform OAuth 2.0 authentication
- `get(url, **kwargs)`: Make GET request with authentication
- `post(url, **kwargs)`: Make POST request with authentication
- `put(url, **kwargs)`: Make PUT request with authentication
- `delete(url, **kwargs)`: Make DELETE request with authentication
- `refresh_token()`: Manually refresh the access token
- `is_authenticated()`: Check if currently authenticated
- `get_access_token()`: Get current access token
- `logout()`: Clear stored credentials

#### Class Methods

- `from_env()`: Create instance from environment variables

### Token Storage

The library supports different token storage backends:

- `KeyringTokenStorage` (default): Uses system keyring
- `FileTokenStorage`: Stores tokens in a JSON file
- `MemoryTokenStorage`: Stores tokens in memory (not persistent)

## Configuration

### Environment Variables

- `GOTO_CLIENT_ID`: Your GoTo Connect application client ID
- `GOTO_CLIENT_SECRET`: Your GoTo Connect application client secret
- `GOTO_REDIRECT_URI`: OAuth redirect URI (default: http://localhost:8080/callback)
- `GOTO_AUTH_URL`: Custom authorization URL
- `GOTO_TOKEN_URL`: Custom token URL

### Configuration File

You can also use a configuration file:

```python
from gotoconnect_auth import GoToConnectAuth

auth = GoToConnectAuth.from_config("config.json")
```

Config file format:

```json
{
    "client_id": "YOUR_CLIENT_ID_HERE",
    "client_secret": "YOUR_CLIENT_SECRET_HERE",
    "redirect_uri": "http://localhost:8080/callback"
}
```

## Examples

### Meeting Management

```python
from gotoconnect_auth import GoToConnectAuth

auth = GoToConnectAuth.from_env()
auth.authenticate()

# Create a meeting
meeting_data = {
    "subject": "Test Meeting",
    "startTime": "2024-01-15T10:00:00Z",
    "endTime": "2024-01-15T11:00:00Z"
}

response = auth.post(
    "https://api.goto.com/rest/meetings/v1/meetings",
    json=meeting_data
)
print(f"Meeting created: {response.json()}")
```

### User Management

```python
# Get user information
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_info = response.json()
print(f"User: {user_info['firstName']} {user_info['lastName']}")

# Get all users
response = auth.get("https://api.goto.com/rest/users/v1/users")
users = response.json()
for user in users['users']:
    print(f"User: {user['firstName']} {user['lastName']} ({user['email']})")
```

## 🔒 Security

### Important Security Notes

- **Never commit your `.env` file or `config.json` with real credentials**
- The library uses secure storage (keyring) by default
- Tokens are automatically refreshed when they expire
- Use environment variables in production environments
- Keep your GoTo Connect application credentials secure

### Environment Variables vs Configuration Files

- **Environment Variables** (Recommended): More secure, easier to manage in CI/CD
- **Configuration Files**: Convenient for development, but keep them out of version control

## 🧪 Testing

Run the test suite to verify everything works:

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=gotoconnect_auth --cov-report=html
```

## 📚 Examples

Check out the [examples](examples/) directory for complete working examples:

- [Basic Usage](examples/basic_usage.py) - Simple authentication and API calls
- [Meeting Manager](examples/meeting_manager.py) - Advanced meeting management

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and add tests
4. **Run the test suite**: `python -m pytest tests/ -v`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python -m pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the [examples](examples/) directory
- 🐛 **Issues**: Open an issue on [GitHub](https://github.com/yourusername/gotoconnect-auth/issues)
- 💬 **Discussions**: Start a discussion for questions and ideas
- 📧 **Contact**: Reach out to the maintainers

## 🙏 Acknowledgments

- GoTo Connect for providing the API
- The Python community for excellent libraries
- Contributors and users of this library 