#!/usr/bin/env python3
"""
Simple API Test for GoTo Connect Authentication

This script tests the actual GoTo Connect API endpoints using your authentication.
It will use existing tokens if available, or authenticate once if needed.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from gotoconnect_auth import GoToConnectAuth
    print("✅ Successfully imported gotoconnect_auth library")
except ImportError as e:
    print("❌ Failed to import gotoconnect_auth library")
    print(f"Error: {e}")
    sys.exit(1)


def test_api_endpoints():
    """Test various GoTo Connect API endpoints."""
    print("🔍 GoTo Connect API Test")
    print("=" * 50)
    
    try:
        # Initialize authentication
        print("🔄 Initializing authentication...")
        auth = GoToConnectAuth.from_env()
        
        # Check if already authenticated
        if auth.is_authenticated():
            print("✅ Already authenticated!")
        else:
            print("🔄 Authenticating...")
            auth.authenticate()
            if not auth.is_authenticated():
                print("❌ Authentication failed")
                return False
            print("✅ Authentication successful!")
        
        # Test 1: Get current user
        print("\n📋 Test 1: Getting current user...")
        try:
            response = auth.get("https://api.goto.com/rest/users/v1/users/me")
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ User API test successful!")
                print(f"👤 User: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
                print(f"📧 Email: {user_data.get('email', '')}")
                print(f"🏢 Company: {user_data.get('companyName', 'N/A')}")
            else:
                print(f"❌ User API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ User API error: {e}")
            return False
        
        # Test 2: Get meetings
        print("\n📅 Test 2: Getting meetings...")
        try:
            response = auth.get("https://api.goto.com/rest/meetings/v1/meetings?limit=5")
            if response.status_code == 200:
                meetings_data = response.json()
                meeting_count = len(meetings_data.get('meetings', []))
                print(f"✅ Meetings API test successful!")
                print(f"📊 Found {meeting_count} meetings")
                
                # Show first few meetings
                for i, meeting in enumerate(meetings_data.get('meetings', [])[:3]):
                    print(f"   {i+1}. {meeting.get('subject', 'No subject')} - {meeting.get('startTime', 'No time')}")
            else:
                print(f"❌ Meetings API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Meetings API error: {e}")
            return False
        
        # Test 3: Get user lines (phone numbers)
        print("\n📞 Test 3: Getting user lines...")
        try:
            response = auth.get("https://api.goto.com/rest/users/v1/users/me/lines")
            if response.status_code == 200:
                lines_data = response.json()
                line_count = len(lines_data.get('lines', []))
                print(f"✅ Lines API test successful!")
                print(f"📞 Found {line_count} phone lines")
                
                # Show first few lines
                for i, line in enumerate(lines_data.get('lines', [])[:3]):
                    print(f"   {i+1}. {line.get('number', 'No number')} - {line.get('name', 'No name')}")
            else:
                print(f"❌ Lines API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Lines API error: {e}")
            return False
        
        # Test 4: Get contacts
        print("\n👥 Test 4: Getting contacts...")
        try:
            response = auth.get("https://api.goto.com/rest/contacts/v1/contacts?limit=5")
            if response.status_code == 200:
                contacts_data = response.json()
                contact_count = len(contacts_data.get('contacts', []))
                print(f"✅ Contacts API test successful!")
                print(f"👥 Found {contact_count} contacts")
                
                # Show first few contacts
                for i, contact in enumerate(contacts_data.get('contacts', [])[:3]):
                    print(f"   {i+1}. {contact.get('firstName', '')} {contact.get('lastName', '')} - {contact.get('email', 'No email')}")
            else:
                print(f"❌ Contacts API failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Contacts API error: {e}")
            return False
        
        print("\n🎉 All API tests completed successfully!")
        print("✅ Your GoTo Connect Authentication Library is working perfectly!")
        print("✅ You can now use this library in your projects.")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False


def main():
    """Main function."""
    success = test_api_endpoints()
    
    if success:
        print("\n🎉 API test passed! Your library is ready for use.")
    else:
        print("\n❌ API test failed. Please check your configuration.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 