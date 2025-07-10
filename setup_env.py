#!/usr/bin/env python3
"""
Environment Setup Script

This script helps you set up your .env file with GoTo Connect API credentials.
"""

import os
import sys


def create_env_file():
    """Create the .env file with user input."""
    print("🔧 GoTo Connect API Environment Setup")
    print("=" * 50)
    print()
    print("This script will help you create your .env file with the required credentials.")
    print("You'll need to get these values from the GoTo Developer Portal:")
    print("  - Go to https://developer.goto.com/")
    print("  - Create a new app or use an existing one")
    print("  - Get your Client ID and Client Secret")
    print("  - Set the redirect URI to: http://localhost:8080/callback")
    print()
    
    # Get user input
    client_id = input("Enter your Client ID: ").strip()
    if not client_id:
        print("❌ Client ID is required!")
        return False
    
    client_secret = input("Enter your Client Secret: ").strip()
    if not client_secret:
        print("❌ Client Secret is required!")
        return False
    
    redirect_uri = input("Enter your Redirect URI (default: http://localhost:8080/callback): ").strip()
    if not redirect_uri:
        redirect_uri = "http://localhost:8080/callback"
    
    # Create .env content
    env_content = f"""# GoTo Connect API Credentials
GOTO_CLIENT_ID={client_id}
GOTO_CLIENT_SECRET={client_secret}
GOTO_REDIRECT_URI={redirect_uri}

# Optional: Token storage method (keyring, file, memory)
# Default is keyring if available, otherwise file
GOTO_TOKEN_STORAGE=keyring
"""
    
    # Write to .env file
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print()
        print("✅ .env file created successfully!")
        print("🔒 Your credentials have been saved securely.")
        print()
        print("Next steps:")
        print("1. Run: py quick_test.py")
        print("2. Follow the authentication flow")
        print("3. Run: py simple_api_test.py")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False


def main():
    """Main function."""
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        overwrite = input("Do you want to overwrite it? (y/N): ").strip().lower()
        if overwrite != 'y':
            print("Setup cancelled.")
            return
    
    success = create_env_file()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 