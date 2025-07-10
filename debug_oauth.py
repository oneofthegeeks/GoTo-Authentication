#!/usr/bin/env python3
"""
Debug OAuth Flow

This script provides detailed debugging information for the OAuth authentication process.
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


def debug_oauth_flow():
    """Debug the OAuth authentication flow."""
    print("🔍 Debug OAuth Flow")
    print("=" * 50)
    
    try:
        # Initialize authentication
        print("🔄 Initializing authentication...")
        auth = GoToConnectAuth.from_env()
        
        # Show configuration
        print(f"\n📋 Configuration:")
        print(f"   Client ID: {auth.client_id[:8]}...")
        print(f"   Redirect URI: {auth.redirect_uri}")
        print(f"   Auth URL: {auth.auth_url}")
        print(f"   Token URL: {auth.token_url}")
        
        # Check if already authenticated
        if auth.is_authenticated():
            print("✅ Already authenticated!")
            return True
        
        print("\n🔄 Starting OAuth flow...")
        print("💡 This will open your browser for authentication.")
        print("💡 After you authenticate, the browser should redirect to:")
        print(f"   {auth.redirect_uri}")
        print("💡 If the redirect doesn't work, check your browser's address bar.")
        
        # Start authentication with timeout
        try:
            auth.authenticate()
            print("✅ Authentication successful!")
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            print("\n🔧 Troubleshooting tips:")
            print("1. Check if your browser opened the authentication URL")
            print("2. Make sure you completed the login in the browser")
            print("3. Check if the browser redirected to the callback URL")
            print("4. Look for any error messages in the browser")
            print("5. Try running 'py quick_test.py' for a simpler test")
            return False
            
    except Exception as e:
        print(f"❌ Error during OAuth flow: {e}")
        return False


def main():
    """Main function."""
    print("🚀 Starting OAuth Debug")
    print("=" * 50)
    
    success = debug_oauth_flow()
    
    if success:
        print("\n🎉 OAuth flow completed successfully!")
        print("💡 You can now run 'py simple_api_test.py' to test the API.")
    else:
        print("\n❌ OAuth flow failed.")
        print("💡 Check the troubleshooting tips above.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 