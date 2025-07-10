#!/usr/bin/env python3
"""
Basic usage example for GoTo Connect Authentication Library.
"""

from gotoconnect_auth import GoToConnectAuth


def main():
    """Demonstrate basic authentication and API usage."""
    
    # Method 1: Initialize with credentials directly
    auth = GoToConnectAuth(
        client_id="YOUR_CLIENT_ID_HERE",
        client_secret="YOUR_CLIENT_SECRET_HERE",
        redirect_uri="http://localhost:8080/callback"
    )
    
    # Method 2: Initialize from environment variables
    # auth = GoToConnectAuth.from_env()
    
    # Method 3: Initialize from config file
    # auth = GoToConnectAuth.from_config("config.json")
    
    try:
        # Authenticate (this will open a browser for first-time auth)
        print("Authenticating with GoTo Connect...")
        auth.authenticate()
        
        if auth.is_authenticated():
            print("✅ Successfully authenticated!")
            
            # Get current user information
            print("\n📋 Getting user information...")
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            user_info = response.json()
            print(f"👤 User: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
            print(f"📧 Email: {user_info.get('email', '')}")
            
            # Get meetings
            print("\n📅 Getting meetings...")
            response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
            meetings = response.json()
            print(f"📊 Found {len(meetings.get('meetings', []))} meetings")
            
            # Create a test meeting
            print("\n➕ Creating a test meeting...")
            meeting_data = {
                "subject": "Test Meeting from Python Library",
                "startTime": "2024-01-15T10:00:00Z",
                "endTime": "2024-01-15T11:00:00Z",
                "description": "This is a test meeting created using the GoTo Connect Auth Library"
            }
            
            response = auth.post(
                "https://api.goto.com/rest/meetings/v1/meetings",
                json=meeting_data
            )
            new_meeting = response.json()
            print(f"✅ Meeting created: {new_meeting.get('meetingId', 'Unknown')}")
            
        else:
            print("❌ Authentication failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 