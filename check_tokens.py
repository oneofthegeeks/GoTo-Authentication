#!/usr/bin/env python3
"""
Check Stored Tokens

This script checks if you already have valid authentication tokens stored.
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

def check_stored_tokens():
    """Check if valid tokens are already stored."""
    print("🔍 Checking Stored Tokens")
    print("=" * 40)
    
    try:
        # Initialize authentication
        auth = GoToConnectAuth.from_env()
        
        # Check if authenticated
        is_auth = auth.is_authenticated()
        print(f"🔐 Authentication Status: {'✅ Authenticated' if is_auth else '❌ Not Authenticated'}")
        
        if is_auth:
            print("🎉 You already have valid tokens!")
            print("💡 You can now run API tests without re-authenticating.")
            return True
        else:
            print("❌ No valid tokens found.")
            print("💡 You'll need to complete the OAuth flow.")
            return False
            
    except Exception as e:
        print(f"❌ Error checking tokens: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Token Check")
    print("=" * 50)
    
    success = check_stored_tokens()
    
    if success:
        print("\n✅ You're ready to test the API!")
        print("💡 Run: py simple_api_test.py")
    else:
        print("\n💡 You need to authenticate first.")
        print("💡 Try signing out of GoTo Connect and running the test again.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 