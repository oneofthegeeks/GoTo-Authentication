# GoTo Connect Authentication Library

A simple, reusable Python library for authenticating with GoTo Connect APIs.

## 🚀 Quick Start

### 1. Install the Library

```bash
# Install dependencies
pip install requests python-dotenv keyring

# Or use the setup script
python simple_setup.py
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

### Option 1: Quick Setup
```bash
python simple_setup.py
```

### Option 2: Manual Installation
```bash
pip install requests python-dotenv keyring
```

## 🔧 Usage

### Basic Authentication

```python
from gotoconnect_auth import GoToConnectAuth

# Initialize from environment variables
auth = GoToConnectAuth.from_env()

# Authenticate
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

## 🔒 Security

- **Never commit your `.env` file** with real credentials
- The library uses secure storage (keyring) by default
- Tokens are automatically refreshed when they expire
- Use environment variables in production

## 📚 Examples

Check out the `examples/` directory for complete working examples:

- `simple_example.py` - Basic authentication and API calls
- `meeting_manager.py` - Advanced meeting management

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/yourusername/gotoconnect-auth.git
cd gotoconnect-auth

# Install in development mode
pip install -e .

# Run tests
python -m pytest tests/ -v
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 **Documentation**: Check the examples directory
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Discussions**: Start a discussion for questions
