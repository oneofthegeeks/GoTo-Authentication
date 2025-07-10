# Quick Start Guide

This guide will help you get up and running with the GoTo Connect Authentication Library in just a few minutes.

## Prerequisites

- Python 3.7 or higher
- A GoTo Connect developer account
- Your GoTo Connect application credentials

## Step 1: Get Your GoTo Connect Credentials

1. Go to the [GoTo Connect Developer Portal](https://developer.goto.com/)
2. Create a new application or use an existing one
3. Note your **Client ID** and **Client Secret**
4. Set the redirect URI to `http://localhost:8080/callback`

## Step 2: Install the Library

### Option A: Quick Installation
```bash
python install.py
```

### Option B: Manual Installation
```bash
# Install dependencies
pip install requests python-dotenv keyring cryptography

# Install the library
pip install -e .
```

## Step 3: Configure Your Credentials

### Option A: Environment Variables (Recommended)
Create a `.env` file in your project directory:
```env
GOTO_CLIENT_ID=your_client_id_here
GOTO_CLIENT_SECRET=your_client_secret_here
```

### Option B: Configuration File
Create a `config.json` file:
```json
{
    "client_id": "your_client_id_here",
    "client_secret": "your_client_secret_here"
}
```

## Step 4: Test the Installation

Create a simple test script:

```python
from gotoconnect_auth import GoToConnectAuth

# Initialize auth (will use environment variables)
auth = GoToConnectAuth.from_env()

# Authenticate
auth.authenticate()

# Test API call
if auth.is_authenticated():
    response = auth.get("https://api.goto.com/rest/users/v1/users/me")
    user_info = response.json()
    print(f"Hello, {user_info.get('firstName', '')} {user_info.get('lastName', '')}!")
else:
    print("Authentication failed!")
```

## Step 5: Test Your Setup

After configuring your credentials, test that everything is working:

```bash
# Quick test (recommended first)
python quick_test.py

# Comprehensive test (all features)
python test_authentication.py
```

## Step 6: Run the Examples

The library comes with several examples:

```bash
# Basic usage example
python examples/basic_usage.py

# Advanced meeting management example
python examples/meeting_manager.py
```

## Common Issues

### Authentication Fails
- Make sure your Client ID and Client Secret are correct
- Ensure your redirect URI matches exactly: `http://localhost:8080/callback`
- Check that your GoTo Connect application is properly configured

### Port 8080 Already in Use
The library uses port 8080 for the OAuth callback. If this port is busy:
1. Change the redirect URI in your GoTo Connect app to use a different port
2. Update your configuration to match

### Keyring Issues (Windows)
If you encounter keyring issues on Windows:
```python
from gotoconnect_auth import GoToConnectAuth, FileTokenStorage

# Use file storage instead of keyring
auth = GoToConnectAuth.from_env(
    token_storage=FileTokenStorage("tokens.json")
)
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the [examples](examples/) directory for more usage patterns
- Explore the [API reference](README.md#api-reference) for all available methods

## Getting Help

- Check the [examples](examples/) directory for usage patterns
- Review the [tests](tests/) for implementation details
- Open an issue on GitHub if you encounter problems

## Security Notes

- Never commit your `.env` file or `config.json` with real credentials
- The library uses secure storage (keyring) by default
- Tokens are automatically refreshed when they expire
- Use environment variables in production environments 