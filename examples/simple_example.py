#!/usr/bin/env python3
"""
Simple GoTo Connect Authentication Example

This example shows the basic usage of the simplified authentication library.
"""

from gotoconnect_auth import GoToConnectAuth


def main():
    """Demonstrate basic authentication and API usage."""
    
    # Initialize authentication from environment variables
    # Make sure you have GOTO_CLIENT_ID and GOTO_CLIENT_SECRET in your .env file
    auth = GoToConnectAuth.from_env()
    
    try:
        # Authenticate (opens browser for first-time auth)
        print("Authenticating with GoTo Connect...")
        auth.authenticate()
        
        if auth.is_authenticated():
            print("✅ Successfully authenticated!")
            
            # Get user information
            print("\nGetting user information...")
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            user_info = response.json()
            print(f"👤 User: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
            print(f"📧 Email: {user_info.get('email', '')}")
            
            # Get meetings
            print("\nGetting meetings...")
            response = auth.get("https://api.goto.com/rest/meetings/v1/meetings")
            meetings = response.json()
            print(f"📊 Found {len(meetings.get('meetings', []))} meetings")
            
        else:
            print("❌ Authentication failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
