#!/usr/bin/env python3
"""
Authentication Status Checker

This script checks your current authentication status and token information.
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


def check_auth_status():
    """Check authentication status and token information."""
    print("🔍 Authentication Status Check")
    print("=" * 40)
    
    try:
        # Initialize authentication
        print("🔄 Initializing authentication...")
        auth = GoToConnectAuth.from_env()
        
        # Check if authenticated
        is_auth = auth.is_authenticated()
        print(f"🔐 Authentication Status: {'✅ Authenticated' if is_auth else '❌ Not Authenticated'}")
        
        if is_auth:
            # Get token info
            token_info = auth.get_token_info()
            if token_info:
                print(f"📅 Token Expires: {token_info.get('expires_at', 'Unknown')}")
                print(f"🔄 Refresh Token: {'✅ Available' if token_info.get('refresh_token') else '❌ Not Available'}")
                print(f"🔑 Access Token: {'✅ Available' if token_info.get('access_token') else '❌ Not Available'}")
            else:
                print("❌ No token information available")
        
        # Check environment variables
        print("\n🔧 Environment Variables:")
        client_id = os.getenv('GOTO_CLIENT_ID')
        client_secret = os.getenv('GOTO_CLIENT_SECRET')
        redirect_uri = os.getenv('GOTO_REDIRECT_URI')
        
        print(f"   Client ID: {'✅ Set' if client_id else '❌ Missing'}")
        print(f"   Client Secret: {'✅ Set' if client_secret else '❌ Missing'}")
        print(f"   Redirect URI: {'✅ Set' if redirect_uri else '❌ Missing'}")
        
        if not all([client_id, client_secret, redirect_uri]):
            print("\n⚠️  Missing environment variables. Please check your .env file.")
            return False
        
        return is_auth
        
    except Exception as e:
        print(f"❌ Error checking authentication status: {e}")
        return False


def main():
    """Main function."""
    success = check_auth_status()
    
    if success:
        print("\n✅ Authentication is working properly!")
        print("💡 You can now run the simple_api_test.py to test the actual API.")
    else:
        print("\n❌ Authentication issues detected.")
        print("💡 Please run the quick_test.py first to authenticate.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 