#!/usr/bin/env python3
"""
Simple API Test for GoTo Connect Authentication

This script tests the actual GoTo Connect API endpoints using your authentication.
It will use existing tokens if available, or authenticate once if needed.
"""

import os
import sys
import time
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
            print("🔄 Need to authenticate...")
            print("⚠️  This will open your browser for OAuth authentication.")
            print("💡 If the browser doesn't open, you can manually navigate to the URL.")
            
            try:
                auth.authenticate()
                print("✅ Authentication successful!")
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                print("💡 Try running 'py quick_test.py' first to authenticate manually.")
                return False
        
        # Test API endpoints
        print("\n🧪 Testing API Endpoints...")
        
        # Test 1: Get user info
        print("\n1️⃣ Testing User Info API...")
        try:
            response = auth.get("https://api.goto.com/v1/users/me")
            if response.status_code == 200:
                user_data = response.json()
                print(f"✅ User Info: {user_data.get('name', 'Unknown')} ({user_data.get('email', 'No email')})")
            else:
                print(f"⚠️  User Info API returned status {response.status_code}")
        except Exception as e:
            print(f"❌ User Info API error: {e}")
        
        # Test 2: Get meetings
        print("\n2️⃣ Testing Meetings API...")
        try:
            response = auth.get("https://api.goto.com/v1/meetings")
            if response.status_code == 200:
                meetings_data = response.json()
                meeting_count = len(meetings_data.get('meetings', []))
                print(f"✅ Found {meeting_count} meetings")
            else:
                print(f"⚠️  Meetings API returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Meetings API error: {e}")
        
        # Test 3: Get account info
        print("\n3️⃣ Testing Account API...")
        try:
            response = auth.get("https://api.goto.com/v1/accounts")
            if response.status_code == 200:
                account_data = response.json()
                print(f"✅ Account Info: {account_data.get('name', 'Unknown account')}")
            else:
                print(f"⚠️  Account API returned status {response.status_code}")
        except Exception as e:
            print(f"❌ Account API error: {e}")
        
        print("\n✅ API testing completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during API testing: {e}")
        return False


def main():
    """Main function."""
    print("🚀 Starting GoTo Connect API Test")
    print("=" * 50)
    
    success = test_api_endpoints()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("💡 Your GoTo Connect authentication is working properly.")
    else:
        print("\n❌ Some tests failed.")
        print("💡 Check your credentials and try again.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 