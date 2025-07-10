#!/usr/bin/env python3
"""
Show OAuth URL

This script shows the OAuth authorization URL that you can manually navigate to.
"""

import os
import sys
from urllib.parse import urlencode
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


def show_oauth_url():
    """Show the OAuth authorization URL."""
    print("🔍 OAuth Authorization URL")
    print("=" * 50)
    
    try:
        # Initialize authentication
        print("🔄 Initializing authentication...")
        auth = GoToConnectAuth.from_env()
        
        # Build the authorization URL
        params = {
            'client_id': auth.client_id,
            'redirect_uri': auth.redirect_uri,
            'response_type': 'code',
            'scope': auth.scope or 'messaging.v1.send contacts.v1.write call-events.v1.events.read users.v1.read presence.v1.read recording.v1.notifications.manage voice-admin.v1.write recording.v1.read identity:scim.org collaboration users.v1.lines.read voicemail.v1.voicemails.read messaging.v1.notifications.manage fax.v1'
        }
        
        auth_url = f"{auth.auth_url}?{urlencode(params)}"
        
        print(f"\n📋 Authorization URL:")
        print(f"   {auth_url}")
        print(f"\n💡 You can:")
        print(f"   1. Copy this URL and paste it in your browser")
        print(f"   2. Or let the script open it automatically")
        print(f"   3. After authentication, you'll be redirected to: {auth.redirect_uri}")
        
        # Ask if user wants to open browser
        response = input("\n🤔 Do you want to open this URL in your browser? (y/N): ").strip().lower()
        if response == 'y':
            import webbrowser
            print("🌐 Opening browser...")
            webbrowser.open(auth_url)
            print("✅ Browser opened!")
            print("💡 Complete the authentication in your browser.")
            print("💡 The script will wait for the callback...")
            
            # Now try to authenticate
            try:
                auth.authenticate()
                print("✅ Authentication successful!")
                return True
            except Exception as e:
                print(f"❌ Authentication failed: {e}")
                return False
        else:
            print("💡 You can manually navigate to the URL above.")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main function."""
    print("🚀 OAuth URL Helper")
    print("=" * 50)
    
    success = show_oauth_url()
    
    if success:
        print("\n🎉 Authentication completed!")
        print("💡 You can now run 'py simple_api_test.py' to test the API.")
    else:
        print("\n💡 Manual authentication may be required.")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 