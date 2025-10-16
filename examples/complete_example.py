#!/usr/bin/env python3
"""
Complete GoTo Connect Authentication Example

This example demonstrates the full capabilities of the simplified authentication library.
"""

from gotoconnect_auth import GoToConnectAuth
from datetime import datetime, timedelta


def main():
    """Demonstrate complete authentication and API usage."""
    
    print("🚀 GoTo Connect Authentication Library - Complete Example")
    print("=" * 60)
    
    # Initialize authentication from environment variables
    # Make sure you have GOTO_CLIENT_ID and GOTO_CLIENT_SECRET in your .env file
    auth = GoToConnectAuth.from_env()
    
    try:
        # Authenticate (opens browser for first-time auth)
        print("🔐 Authenticating with GoTo Connect...")
        auth.authenticate()
        
        if auth.is_authenticated():
            print("✅ Successfully authenticated!")
            
            # Get user information
            print("\n👤 Getting user information...")
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            user_info = response.json()
            print(f"   Name: {user_info.get('firstName', '')} {user_info.get('lastName', '')}")
            print(f"   Email: {user_info.get('email', '')}")
            print(f"   Company: {user_info.get('company', 'N/A')}")
            
            # Get existing meetings
            print("\n📅 Getting existing meetings...")
            response = auth.get("https://api.goto.com/rest/meetings/v1/meetings?limit=5")
            meetings = response.json()
            meeting_list = meetings.get('meetings', [])
            print(f"   Found {len(meeting_list)} meetings")
            
            for meeting in meeting_list[:3]:  # Show first 3 meetings
                print(f"   - {meeting.get('subject', 'No Subject')} ({meeting.get('startTime', 'No Time')})")
            
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
            
            print(f"   ✅ Created meeting: {meeting_id}")
            print(f"   Subject: {new_meeting.get('subject', 'Unknown')}")
            print(f"   Start: {new_meeting.get('startTime', 'Unknown')}")
            
            # Update the meeting
            print("\n✏️ Updating meeting...")
            update_data = {
                "subject": "Updated Python Library Test Meeting",
                "description": "Updated description from Python library"
            }
            
            response = auth.put(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}", json=update_data)
            updated_meeting = response.json()
            
            print(f"   ✅ Updated meeting: {updated_meeting.get('subject', 'Unknown')}")
            
            # Clean up - delete the test meeting
            print("\n🗑️ Cleaning up test meeting...")
            response = auth.delete(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}")
            
            if response.status_code == 204:
                print("   ✅ Test meeting deleted successfully!")
            else:
                print(f"   ⚠️ Could not delete meeting: {response.status_code}")
            
            # Demonstrate automatic token refresh
            print("\n🔄 Demonstrating automatic token refresh...")
            print("   The library automatically handles token refresh when needed.")
            print("   No manual intervention required!")
            
            # Make another API call to show tokens are still valid
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            if response.status_code == 200:
                print("   ✅ API call successful - tokens are working!")
            
        else:
            print("❌ Authentication failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure you have set up your .env file with your credentials")
        print("2. Check that your GoTo Connect application is properly configured")
        print("3. Ensure your redirect URI matches: http://localhost:8080/callback")
        print("4. Try running the simple test: python test_simple.py")


if __name__ == "__main__":
    main()
