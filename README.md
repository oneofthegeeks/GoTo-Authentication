# GoTo Connect Authentication Library

A simple, reusable Python library for authenticating with GoTo Connect APIs. This library handles OAuth 2.0 authentication, automatic token refresh, and secure credential storage.

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### 1. Installation

```bash
pip install gotoconnect-auth
```

### 2. Get Your Credentials

1. Go to [GoTo Connect Developer Portal](https://developer.goto.com/)
2. Create a new application
3. Get your **Client ID** and **Client Secret**
4. Set redirect URI to `http://localhost:8080/callback`

### 3. Configure Credentials

Create a `.env` file in your project:

```env
GOTO_CLIENT_ID=your_client_id_here
GOTO_CLIENT_SECRET=your_client_secret_here
GOTO_REDIRECT_URI=http://localhost:8080/callback
```

### 4. Use the Library

```python
from gotoconnect_auth import GoToConnectAuth

# Initialize authentication
auth = GoToConnectAuth.from_env()

# Authenticate (opens browser for first-time auth)
auth.authenticate()

# Make API calls
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_info = response.json()
print(f"Hello, {user_info.get('firstName', '')}!")
```

## 📦 Installation

### From PyPI (Recommended)
```bash
pip install gotoconnect-auth
```

### From Source
```bash
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth
pip install -e .
```

## 🔧 Usage

### Basic Authentication

```python
from gotoconnect_auth import GoToConnectAuth

# Initialize from environment variables
auth = GoToConnectAuth.from_env()

# Authenticate (opens browser for first-time auth)
auth.authenticate()

# Check if authenticated
if auth.is_authenticated():
    print("Successfully authenticated!")
```

### Making API Calls

```python
# GET request
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_data = response.json()

# POST request
meeting_data = {
    "subject": "Test Meeting",
    "startTime": "2024-01-15T10:00:00Z",
    "endTime": "2024-01-15T11:00:00Z"
}
response = auth.post("https://api.goto.com/rest/meetings/v1/meetings", json=meeting_data)
```

### Automatic Token Refresh

The library automatically handles token refresh:

```python
# Tokens are automatically refreshed when they expire
# No manual intervention needed!
auth.authenticate()  # Only needed once
response = auth.get("https://api.goto.com/rest/users/v1/users/me")  # Works even after token expires
```

### Custom Token Storage

```python
from gotoconnect_auth import GoToConnectAuth, FileTokenStorage

# Use file storage instead of keyring
auth = GoToConnectAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    token_storage=FileTokenStorage("my_tokens.json")
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

# Logout
auth.logout()
```

## 🔒 Security

- **Never commit your `.env` file** with real credentials
- The library uses secure storage (keyring) by default
- Tokens are automatically refreshed when they expire
- Use environment variables in production

## 📚 Examples

### Complete Working Example

```python
from gotoconnect_auth import GoToConnectAuth

def main():
    # Initialize authentication
    auth = GoToConnectAuth.from_env()
    
    try:
        # Authenticate (opens browser for first-time auth)
        print("Authenticating with GoTo Connect...")
        auth.authenticate()
        
        if auth.is_authenticated():
            print("✅ Successfully authenticated!")
            
            # Get user information
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            user_info = response.json()
            print(f"👤 User: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
            print(f"📧 Email: {user_info.get('email', '')}")
            
            # Get meetings
            response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
            meetings = response.json()
            print(f"📊 Found {len(meetings.get('meetings', []))} meetings")
            
        else:
            print("❌ Authentication failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
```

## 🛠️ Development

### Setup Development Environment

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

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=gotoconnect_auth --cov-report=html
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the examples directory
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Discussions**: Start a discussion for questions

## 🙏 Acknowledgments

- GoTo Connect for providing the API
- The Python community for excellent libraries
- Contributors and users of this library