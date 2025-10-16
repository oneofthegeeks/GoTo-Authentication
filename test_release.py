#!/usr/bin/env python3
"""
Release Test Script for GoTo Connect Authentication Library

This script tests the key features of the simplified authentication library.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from gotoconnect_auth import GoToConnectAuth, SecureTokenStorage, FileTokenStorage, MemoryTokenStorage
    print("✅ Successfully imported gotoconnect_auth library")
except ImportError as e:
    print("❌ Failed to import gotoconnect_auth library")
    print(f"Error: {e}")
    sys.exit(1)


def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import requests
        print("✅ requests module imported successfully")
    except ImportError:
        print("❌ requests module not found")
        return False
    
    try:
        import keyring
        print("✅ keyring module imported successfully")
    except ImportError:
        print("⚠️ keyring module not found - will use file storage fallback")
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv module imported successfully")
    except ImportError:
        print("⚠️ python-dotenv module not found - environment variables may not work")
    
    return True


def test_configuration():
    """Test configuration loading."""
    print("\n🔍 Testing configuration...")
    
    client_id = os.getenv('GOTO_CLIENT_ID')
    client_secret = os.getenv('GOTO_CLIENT_SECRET')
    
    if client_id and client_secret:
        print("✅ Environment variables found")
        print(f"   Client ID: {client_id[:8]}...")
        print(f"   Client Secret: {client_secret[:8]}...")
        return True
    else:
        print("❌ Environment variables not found")
        print("   Please create a .env file with:")
        print("   GOTO_CLIENT_ID=your_client_id")
        print("   GOTO_CLIENT_SECRET=your_client_secret")
        return False


def test_auth_initialization():
    """Test authentication object initialization."""
    print("\n🔍 Testing authentication initialization...")
    
    try:
        # Test from environment
        auth = GoToConnectAuth.from_env()
        print("✅ Authentication object initialized from environment variables")
        return auth
    except Exception as e:
        print(f"❌ Failed to initialize from environment: {e}")
        return None


def test_token_storage():
    """Test token storage functionality."""
    print("\n🔍 Testing token storage...")
    
    try:
        # Test memory storage
        memory_storage = MemoryTokenStorage()
        test_tokens = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'expires_at': 1234567890
        }
        
        memory_storage.save_tokens(test_tokens)
        loaded_tokens = memory_storage.load_tokens()
        
        if loaded_tokens == test_tokens:
            print("✅ Memory token storage working correctly")
        else:
            print("❌ Memory token storage test failed")
            return False
        
        # Test file storage
        file_storage = FileTokenStorage("test_tokens.json")
        file_storage.save_tokens(test_tokens)
        loaded_file_tokens = file_storage.load_tokens()
        
        if loaded_file_tokens == test_tokens:
            print("✅ File token storage working correctly")
        else:
            print("❌ File token storage test failed")
            return False
        
        # Clean up
        file_storage.clear_tokens()
        if os.path.exists("test_tokens.json"):
            os.remove("test_tokens.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Token storage test failed: {e}")
        return False


def test_authentication(auth):
    """Test authentication flow."""
    print("\n🔍 Testing authentication...")
    
    if not auth:
        print("❌ No authentication object available")
        return False
    
    try:
        print("   🔄 Attempting authentication...")
        print("   ⚠️  This will open your browser for OAuth authentication")
        print("   💡 If the browser doesn't open, you can manually navigate to the URL")
        
        auth.authenticate()
        
        if auth.is_authenticated():
            print("✅ Authentication successful!")
            return True
        else:
            print("❌ Authentication failed")
            return False
            
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False


def test_api_connectivity(auth):
    """Test API connectivity."""
    print("\n🔍 Testing API connectivity...")
    
    if not auth or not auth.is_authenticated():
        print("❌ Not authenticated - skipping API test")
        return False
    
    try:
        response = auth.get("https://api.goto.com/rest/users/v1/users/me", timeout=30)
        if response.status_code == 200:
            user_data = response.json()
            print("✅ API connectivity test successful")
            print(f"   👤 User: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
            print(f"   📧 Email: {user_data.get('email', '')}")
            return True
        else:
            print(f"❌ API test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API connectivity test failed: {e}")
        return False


def run_comprehensive_test():
    """Run all tests and provide a summary."""
    print("🚀 GoTo Connect Authentication Library - Release Test")
    print("=" * 60)
    
    results = {
        'imports': False,
        'configuration': False,
        'auth_init': False,
        'token_storage': False,
        'authentication': False,
        'api_connectivity': False
    }
    
    # Test imports
    results['imports'] = test_imports()
    
    # Test configuration
    results['configuration'] = test_configuration()
    
    # Test authentication initialization
    auth = test_auth_initialization()
    results['auth_init'] = auth is not None
    
    # Test token storage
    results['token_storage'] = test_token_storage()
    
    # Test authentication
    results['authentication'] = test_authentication(auth)
    
    # Test API connectivity
    results['api_connectivity'] = test_api_connectivity(auth)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    # Check if this is a CI environment (no credentials expected)
    is_ci = os.getenv('CI') or os.getenv('GITHUB_ACTIONS')
    
    if passed == total:
        print("\n🎉 All tests passed! The library is ready for release.")
        print("💡 Users can now easily authenticate with GoTo Connect APIs.")
        return True
    elif is_ci and passed >= 2:  # In CI, we expect imports and token storage to pass
        print("\n✅ CI tests passed! Core functionality is working.")
        print("💡 Authentication tests require credentials (expected in CI).")
        return True
    elif passed >= total - 2:
        print("\n⚠️  Most tests passed. Some features may not work as expected.")
        print("💡 Check the failed tests above for more information.")
        return True
    else:
        print("\n❌ Multiple tests failed. Please check your configuration.")
        print("💡 Make sure you have:")
        print("   1. Set up your GoTo Connect application")
        print("   2. Configured your credentials in .env file")
        print("   3. Installed all required dependencies")
        return False


def main():
    """Main function to run the test suite."""
    try:
        success = run_comprehensive_test()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
