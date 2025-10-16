# GoTo Connect Authentication Library - Complete Usage Guide

## 🎯 Overview

This library provides a simple, reusable way to authenticate with GoTo Connect APIs. It handles OAuth 2.0 authentication, automatic token refresh, and secure credential storage.

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

### 4. Basic Usage

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

## 🔧 Detailed Usage

### Authentication Methods

#### Method 1: Environment Variables (Recommended)

```python
from gotoconnect_auth import GoToConnectAuth

# Uses GOTO_CLIENT_ID and GOTO_CLIENT_SECRET from .env file
auth = GoToConnectAuth.from_env()
```

#### Method 2: Direct Initialization

```python
from gotoconnect_auth import GoToConnectAuth

auth = GoToConnectAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="http://localhost:8080/callback"
)
```

### Authentication Flow

#### First-Time Authentication

```python
# This will open your browser for OAuth authentication
auth.authenticate()

# Check if authentication was successful
if auth.is_authenticated():
    print("Successfully authenticated!")
else:
    print("Authentication failed!")
```

#### Subsequent Uses

```python
# The library automatically uses stored tokens
# No need to authenticate again unless tokens are expired
auth = GoToConnectAuth.from_env()

# This will use stored tokens or refresh them automatically
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
```

### Making API Calls

#### GET Requests

```python
# Get user information
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_data = response.json()
print(f"User: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")

# Get meetings
response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
meetings = response.json()
print(f"Found {len(meetings.get('meetings', []))} meetings")
```

#### POST Requests

```python
# Create a meeting
meeting_data = {
    "subject": "Test Meeting",
    "startTime": "2024-01-15T10:00:00Z",
    "endTime": "2024-01-15T11:00:00Z",
    "description": "This is a test meeting"
}

response = auth.post("https://api.goto.com/rest/meetings/v1/meetings", json=meeting_data)
new_meeting = response.json()
print(f"Created meeting: {new_meeting.get('meetingId', 'Unknown')}")
```

#### PUT Requests

```python
# Update a meeting
update_data = {
    "subject": "Updated Meeting Title"
}

response = auth.put(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}", json=update_data)
```

#### DELETE Requests

```python
# Delete a meeting
response = auth.delete(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}")
```

### Token Management

#### Automatic Token Refresh

The library automatically handles token refresh:

```python
# Tokens are automatically refreshed when they expire
# No manual intervention needed!
auth.authenticate()  # Only needed once
response = auth.get("https://api.goto.com/rest/users/v1/users/me")  # Works even after token expires
```

#### Manual Token Management

```python
# Check if authenticated
if auth.is_authenticated():
    print("Already authenticated!")
else:
    auth.authenticate()

# Get current access token
token = auth.get_access_token()
print(f"Access token: {token}")

# Logout (clear stored tokens)
auth.logout()
```

### Token Storage Options

#### Default Storage (Keyring + File Fallback)

```python
from gotoconnect_auth import GoToConnectAuth

# Uses secure keyring storage with file fallback
auth = GoToConnectAuth.from_env()
```

#### File Storage

```python
from gotoconnect_auth import GoToConnectAuth, FileTokenStorage

# Use file storage instead of keyring
auth = GoToConnectAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    token_storage=FileTokenStorage("my_tokens.json")
)
```

#### Memory Storage (Not Persistent)

```python
from gotoconnect_auth import GoToConnectAuth, MemoryTokenStorage

# Use memory storage (tokens lost when program exits)
auth = GoToConnectAuth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    token_storage=MemoryTokenStorage()
)
```

## 🔒 Security Best Practices

### 1. Environment Variables

**✅ Good:**
```env
GOTO_CLIENT_ID=your_client_id_here
GOTO_CLIENT_SECRET=your_client_secret_here
```

**❌ Bad:**
```python
# Never hardcode credentials in your code
auth = GoToConnectAuth(
    client_id="real_client_id",  # Don't do this!
    client_secret="real_client_secret"  # Don't do this!
)
```

### 2. File Security

**✅ Good:**
- Use `.env` files for development
- Use environment variables in production
- Never commit `.env` files with real credentials

**❌ Bad:**
- Committing `.env` files with real credentials
- Storing credentials in version control

### 3. Token Storage

**✅ Good:**
- Use the default secure storage (keyring)
- Use file storage only when keyring is not available

**❌ Bad:**
- Using memory storage in production
- Storing tokens in plain text files

## 🛠️ Error Handling

### Basic Error Handling

```python
from gotoconnect_auth import GoToConnectAuth, AuthenticationError, TokenExpiredError

try:
    auth = GoToConnectAuth.from_env()
    auth.authenticate()
    response = auth.get("https://api.goto.com/rest/users/v1/users/me")
    user_data = response.json()
    print(f"User: {user_data.get('firstName', '')}")
except AuthenticationError as e:
    print(f"Authentication error: {e}")
except TokenExpiredError as e:
    print(f"Token expired: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Advanced Error Handling

```python
import requests
from gotoconnect_auth import GoToConnectAuth, AuthenticationError, TokenExpiredError

def make_api_call(auth, url):
    """Make an API call with proper error handling."""
    try:
        response = auth.get(url)
        return response.json()
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")
        return None
    except TokenExpiredError as e:
        print(f"Token expired: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Usage
auth = GoToConnectAuth.from_env()
auth.authenticate()

user_data = make_api_call(auth, "https://api.goto.com/rest/users/v1/users/me")
if user_data:
    print(f"User: {user_data.get('firstName', '')}")
```

## 📚 Complete Examples

### Example 1: Basic User Information

```python
from gotoconnect_auth import GoToConnectAuth

def get_user_info():
    """Get current user information."""
    auth = GoToConnectAuth.from_env()
    auth.authenticate()
    
    if auth.is_authenticated():
        response = auth.get("https://api.goto.com/rest/users/v1/users/me")
        user_data = response.json()
        
        print(f"👤 User: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
        print(f"📧 Email: {user_data.get('email', '')}")
        print(f"🏢 Company: {user_data.get('company', '')}")
        
        return user_data
    else:
        print("❌ Authentication failed!")
        return None

if __name__ == "__main__":
    get_user_info()
```

### Example 2: Meeting Management

```python
from gotoconnect_auth import GoToConnectAuth
from datetime import datetime, timedelta

def manage_meetings():
    """Manage GoTo Connect meetings."""
    auth = GoToConnectAuth.from_env()
    auth.authenticate()
    
    if not auth.is_authenticated():
        print("❌ Authentication failed!")
        return
    
    # Get existing meetings
    print("📅 Getting existing meetings...")
    response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
    meetings = response.json()
    print(f"Found {len(meetings.get('meetings', []))} meetings")
    
    # Create a new meeting
    print("\n➕ Creating a new meeting...")
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    meeting_data = {
        "subject": "Python Library Test Meeting",
        "startTime": start_time.isoformat() + "Z",
        "endTime": end_time.isoformat() + "Z",
        "description": "This meeting was created using the GoTo Connect Auth Library"
    }
    
    response = auth.post("https://api.goto.com/rest/meetings/v1/meetings", json=meeting_data)
    new_meeting = response.json()
    meeting_id = new_meeting.get('meetingId')
    
    print(f"✅ Created meeting: {meeting_id}")
    
    # Update the meeting
    print("\n✏️ Updating meeting...")
    update_data = {
        "subject": "Updated Python Library Test Meeting"
    }
    
    response = auth.put(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}", json=update_data)
    updated_meeting = response.json()
    
    print(f"✅ Updated meeting: {updated_meeting.get('subject', 'Unknown')}")
    
    # Clean up - delete the meeting
    print("\n🗑️ Cleaning up test meeting...")
    response = auth.delete(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}")
    
    if response.status_code == 204:
        print("✅ Test meeting deleted successfully!")
    else:
        print(f"⚠️ Could not delete meeting: {response.status_code}")

if __name__ == "__main__":
    manage_meetings()
```

### Example 3: Production-Ready Application

```python
import os
import logging
from gotoconnect_auth import GoToConnectAuth, AuthenticationError, TokenExpiredError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GoToConnectClient:
    """Production-ready GoTo Connect client."""
    
    def __init__(self):
        self.auth = GoToConnectAuth.from_env()
        self.base_url = "https://api.goto.com/rest"
    
    def ensure_authenticated(self):
        """Ensure we have a valid authentication."""
        try:
            if not self.auth.is_authenticated():
                logger.info("Authenticating with GoTo Connect...")
                self.auth.authenticate()
            return True
        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False
    
    def get_user_info(self):
        """Get current user information."""
        if not self.ensure_authenticated():
            return None
        
        try:
            response = self.auth.get(f"{self.base_url}/users/v1/users/me")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            return None
    
    def get_meetings(self, limit=50):
        """Get user meetings."""
        if not self.ensure_authenticated():
            return None
        
        try:
            response = self.auth.get(f"{self.base_url}/meetings/v1/meetings?limit={limit}")
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get meetings: {e}")
            return None
    
    def create_meeting(self, subject, start_time, end_time, description=""):
        """Create a new meeting."""
        if not self.ensure_authenticated():
            return None
        
        try:
            meeting_data = {
                "subject": subject,
                "startTime": start_time,
                "endTime": end_time,
                "description": description
            }
            
            response = self.auth.post(f"{self.base_url}/meetings/v1/meetings", json=meeting_data)
            return response.json()
        except Exception as e:
            logger.error(f"Failed to create meeting: {e}")
            return None

def main():
    """Main application function."""
    client = GoToConnectClient()
    
    # Get user information
    user_info = client.get_user_info()
    if user_info:
        logger.info(f"Authenticated as: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
    
    # Get meetings
    meetings = client.get_meetings()
    if meetings:
        meeting_count = len(meetings.get('meetings', []))
        logger.info(f"Found {meeting_count} meetings")
    
    # Create a test meeting
    from datetime import datetime, timedelta
    start_time = datetime.utcnow() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    
    new_meeting = client.create_meeting(
        subject="Python Library Test Meeting",
        start_time=start_time.isoformat() + "Z",
        end_time=end_time.isoformat() + "Z",
        description="This meeting was created using the GoTo Connect Auth Library"
    )
    
    if new_meeting:
        logger.info(f"Created meeting: {new_meeting.get('meetingId', 'Unknown')}")

if __name__ == "__main__":
    main()
```

## 🚀 Deployment

### Environment Variables in Production

```bash
# Set environment variables
export GOTO_CLIENT_ID="your_client_id"
export GOTO_CLIENT_SECRET="your_client_secret"
export GOTO_REDIRECT_URI="http://localhost:8080/callback"
```

### Docker Example

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Set environment variables
ENV GOTO_CLIENT_ID="your_client_id"
ENV GOTO_CLIENT_SECRET="your_client_secret"
ENV GOTO_REDIRECT_URI="http://localhost:8080/callback"

CMD ["python", "app.py"]
```

## 📋 Troubleshooting

### Common Issues

1. **Authentication fails**: Check your credentials and redirect URI
2. **Port 8080 in use**: Change the redirect URI in your GoTo Connect app
3. **Keyring issues**: Use file storage instead
4. **Network errors**: Check your internet connection

### Getting Help

- Check the examples directory
- Review the error messages
- Open an issue on GitHub
- Start a discussion for questions

## 🎯 Next Steps

1. Set up your GoTo Connect application
2. Configure your credentials
3. Test the authentication
4. Start building your application!

For more information, see the README.md file.