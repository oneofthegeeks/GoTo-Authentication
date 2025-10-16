#!/usr/bin/env python3
"""
Simple Test Script for GoTo Connect Authentication

This script tests the simplified authentication library.
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


def test_authentication():
    """Test the authentication library."""
    print("🔍 GoTo Connect Authentication Test")
    print("=" * 50)
    
    # Check environment variables
    client_id = os.getenv('GOTO_CLIENT_ID')
    client_secret = os.getenv('GOTO_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in .env file")
        print("Please create a .env file with:")
        print("GOTO_CLIENT_ID=your_client_id")
        print("GOTO_CLIENT_SECRET=your_client_secret")
        return False
    
    print("✅ Credentials found in .env file")
    
    try:
        # Initialize authentication
        print("🔄 Initializing authentication...")
        auth = GoToConnectAuth.from_env()
        print("✅ Authentication object created successfully")
        
        # Test authentication
        print("🔄 Testing authentication...")
        try:
            auth.authenticate()
            print("✅ Authentication successful!")
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
        
        # Test API call
        if auth.is_authenticated():
            print("🔄 Testing API connectivity...")
            try:
                response = auth.get("https://api.goto.com/rest/users/v1/users/me", timeout=30)
                if response.status_code == 200:
                    user_data = response.json()
                    print(f"✅ API test successful!")
                    print(f"👤 Authenticated as: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
                    print(f"📧 Email: {user_data.get('email', '')}")
                    return True
                else:
                    print(f"❌ API test failed with status code: {response.status_code}")
                    return False
            except Exception as e:
                print(f"❌ API test failed: {e}")
                return False
        else:
            print("❌ Authentication validation failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")
        return False


def main():
    """Main function."""
    success = test_authentication()
    
    if success:
        print("\n🎉 Test passed! Your authentication library is working correctly.")
        print("You can now use this library in your projects.")
    else:
        print("\n❌ Test failed. Please check your configuration.")
        print("Make sure you have:")
        print("1. Set up your GoTo Connect application")
        print("2. Configured your credentials in .env file")
        print("3. Installed all required dependencies")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
