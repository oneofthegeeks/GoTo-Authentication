# GoTo Connect Authentication Library v1.0.0

## 🎉 Major Release: Simplified Authentication Library

This release introduces a completely redesigned and simplified GoTo Connect authentication library that makes API authentication easy and reusable for any Python project.

## ✨ What's New

### 🚀 Simplified Authentication
- **One-line setup**: `auth = GoToConnectAuth.from_env()`
- **Automatic browser opening**: No manual URL navigation required
- **Environment variable support**: Uses `.env` files for easy configuration
- **Clean API**: Intuitive methods for all operations

### 🔄 Automatic Token Refresh
- **No manual intervention**: Tokens refresh automatically when they expire
- **Seamless experience**: Users don't need to re-authenticate
- **Smart storage**: Uses system keyring with file fallback
- **Background handling**: All complexity is handled behind the scenes

### 🔒 Enhanced Security
- **Secure storage**: Uses system keyring by default for token storage
- **File fallback**: Falls back to file storage if keyring unavailable
- **No hardcoded credentials**: All examples use placeholders
- **HTTPS only**: All API calls use secure connections

### 📦 Minimal Dependencies
- **Only 3 essential packages**: requests, python-dotenv, keyring
- **No conflicts**: Clean dependency tree
- **Fast installation**: Quick setup and deployment
- **Version constraints**: Proper version requirements

## 🚀 Quick Start

### Installation
```bash
pip install gotoconnect-auth
```

### Basic Usage
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

### Automatic Token Refresh
```python
# Tokens are automatically refreshed when they expire
# No manual intervention needed!
auth.authenticate()  # Only needed once
response = auth.get("https://api.goto.com/rest/users/v1/users/me")  # Works even after token expires
```

## 🔧 Key Features

### ✅ Simple Authentication
- **Environment variables**: Uses `.env` files for configuration
- **Direct initialization**: Support for direct credential passing
- **Automatic browser opening**: No manual URL navigation
- **Error handling**: Comprehensive exception handling

### ✅ HTTP Methods
- **GET requests**: `auth.get(url)`
- **POST requests**: `auth.post(url, json=data)`
- **PUT requests**: `auth.put(url, json=data)`
- **DELETE requests**: `auth.delete(url)`
- **Automatic authentication**: All methods include auth headers

### ✅ Token Storage Options
- **SecureTokenStorage**: Keyring with file fallback (default)
- **FileTokenStorage**: Simple file-based storage
- **MemoryTokenStorage**: In-memory storage for testing

### ✅ Error Handling
- **AuthenticationError**: Authentication failures
- **TokenExpiredError**: Token expiration issues
- **ConfigurationError**: Configuration problems
- **NetworkError**: Network-related errors

## 📚 Documentation

### Complete Documentation
- **README.md**: Quick start guide and overview
- **USAGE_GUIDE.md**: Detailed usage examples and patterns
- **Examples**: Working code examples for all use cases
- **API Reference**: Complete method documentation

### Working Examples
- **Basic Authentication**: Simple setup and usage
- **Complete Example**: Full workflow demonstration
- **Production Example**: Production-ready patterns
- **Error Handling**: Comprehensive error handling examples

## 🛠️ Development

### Setup Development Environment
```bash
# Clone the repository
git clone https://github.com/oneofthegeeks/GoTo-Authentication.git
cd GoTo-Authentication

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Run tests
python test_release.py
```

### Testing
```bash
# Run comprehensive test
python test_release.py

# Run examples
python examples/complete_example.py
python examples/simple_example.py
```

## 🔄 Migration from Previous Versions

### Before (Complex)
```python
from gotoconnect_auth import GoToConnectAuth, KeyringTokenStorage
from gotoconnect_auth.exceptions import GoToConnectAuthError, AuthenticationError

# Complex initialization
auth = GoToConnectAuth(
    client_id="your_id",
    client_secret="your_secret",
    redirect_uri="http://localhost:8080/callback",
    token_storage=KeyringTokenStorage(),
    auth_url="https://authentication.logmeininc.com/oauth/authorize",
    token_url="https://authentication.logmeininc.com/oauth/token"
)

# Complex error handling
try:
    auth.authenticate()
    if auth.is_authenticated():
        response = auth.get("https://api.goto.com/rest/users/v1/users/me")
        # ... more code
except GoToConnectAuthError as e:
    # ... error handling
```

### After (Simple)
```python
from gotoconnect_auth import GoToConnectAuth

# Simple initialization
auth = GoToConnectAuth.from_env()

# Simple authentication
auth.authenticate()

# Simple API calls
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_info = response.json()
print(f"Hello, {user_info.get('firstName', '')}!")
```

## 📦 Dependencies

### Minimal Dependencies
- `requests>=2.25.0` - HTTP library
- `python-dotenv>=0.19.0` - Environment variable loading
- `keyring>=23.0.0` - Secure credential storage

### No Conflicts
- Clean dependency tree
- No version conflicts
- Fast installation

## 🔒 Security

### Best Practices
- **Environment variables**: Use `.env` files for development
- **Production ready**: Use environment variables in production
- **HTTPS only**: All API calls use secure connections
- **Secure storage**: Uses system keyring by default

### Security Features
- **No hardcoded credentials**: All examples use placeholders
- **Secure token storage**: Uses system keyring with file fallback
- **Input validation**: Proper validation of user inputs
- **Error messages**: Don't leak sensitive information

## 🎯 Benefits

1. **Faster Setup**: Get started in under 5 minutes
2. **Fewer Dependencies**: Only 3 essential packages
3. **Clearer Code**: Easy to understand and modify
4. **Better Documentation**: Focused on what users need
5. **Simpler Examples**: Easy to copy and modify
6. **Automatic Token Refresh**: No manual intervention needed
7. **Secure Storage**: Uses system keyring by default

## 📋 Files Changed

### New Files
- `gotoconnect_auth/simple_auth.py` - Simplified authentication class
- `gotoconnect_auth/simple_storage.py` - Streamlined token storage
- `examples/complete_example.py` - Full working example
- `examples/simple_example.py` - Basic usage example
- `test_release.py` - Comprehensive test script
- `USAGE_GUIDE.md` - Detailed usage guide
- `RELEASE_CHECKLIST.md` - Release preparation guide

### Updated Files
- `README.md` - Comprehensive documentation
- `gotoconnect_auth/__init__.py` - Simplified imports
- `setup.py` - Clean package setup
- `requirements.txt` - Minimal dependencies

## 🚀 Next Steps

1. **Install the library**: `pip install gotoconnect-auth`
2. **Set up your credentials**: Create a `.env` file with your GoTo Connect credentials
3. **Try the examples**: Run `python examples/complete_example.py`
4. **Test your setup**: Run `python test_release.py`
5. **Start building**: Use the library in your projects!

## 📞 Support

- 📖 **Documentation**: Check README.md and USAGE_GUIDE.md
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Discussions**: Start a discussion for questions
- 📧 **Contact**: Reach out to maintainers

## 🙏 Acknowledgments

- GoTo Connect for providing the API
- The Python community for excellent libraries
- Contributors and users of this library

---

**Ready to get started?** Check out the [Quick Start Guide](README.md) or [Detailed Usage Guide](USAGE_GUIDE.md) to begin using the simplified GoTo Connect authentication library!
