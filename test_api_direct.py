#!/usr/bin/env python3
"""
Direct API Test for GoTo Connect

This script tests the GoTo Connect API directly without the OAuth flow issues.
"""

import os
import sys
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_directly():
    """Test the GoTo Connect API directly."""
    print("🔍 Direct API Test")
    print("=" * 50)
    
    # Get credentials from environment
    client_id = os.getenv('GOTO_CLIENT_ID')
    client_secret = os.getenv('GOTO_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Missing credentials in .env file")
        return False
    
    print(f"✅ Using Client ID: {client_id[:8]}...")
    
    # Test 1: Check if we can access the API documentation
    print("\n1️⃣ Testing API Documentation...")
    try:
        response = requests.get("https://api.goto.com/")
        print(f"✅ API Documentation accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ API Documentation error: {e}")
    
    # Test 2: Check authentication endpoint
    print("\n2️⃣ Testing Authentication Endpoint...")
    try:
        response = requests.get("https://authentication.logmeininc.com/oauth/authorize")
        print(f"✅ Authentication endpoint accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Authentication endpoint error: {e}")
    
    # Test 3: Check if we can make a simple request
    print("\n3️⃣ Testing Basic API Request...")
    try:
        # This will fail without auth, but we can see the response
        response = requests.get("https://api.goto.com/v1/users/me")
        print(f"✅ API endpoint accessible: {response.status_code}")
        if response.status_code == 401:
            print("ℹ️  Expected 401 - requires authentication")
        elif response.status_code == 200:
            print("🎉 API is working!")
            return True
    except Exception as e:
        print(f"❌ API request error: {e}")
    
    print("\n💡 The API endpoints are accessible but require authentication.")
    print("💡 The OAuth flow needs to be completed to get access tokens.")
    
    return False

def main():
    """Main function."""
    print("🚀 Starting Direct API Test")
    print("=" * 50)
    
    success = test_api_directly()
    
    if success:
        print("\n🎉 API is working perfectly!")
    else:
        print("\n💡 API endpoints are accessible, authentication needed.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 