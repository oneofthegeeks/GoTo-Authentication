#!/usr/bin/env python3
"""
GoTo Connect Authentication Test Script

This script tests the authentication library to verify it's working correctly.
Run this after setting up your credentials to validate your configuration.
"""

import os
import sys
import json
from datetime import datetime, timedelta

# Add the library to the path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    from gotoconnect_auth import GoToConnectAuth, GoToConnectAuthError
except ImportError:
    print("❌ Error: Could not import gotoconnect_auth library")
    print("Make sure you have installed the library: pip install -e .")
    sys.exit(1)


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)


def print_success(message):
    """Print a success message."""
    print(f"✅ {message}")


def print_error(message):
    """Print an error message."""
    print(f"❌ {message}")


def print_info(message):
    """Print an info message."""
    print(f"ℹ️  {message}")


def print_warning(message):
    """Print a warning message."""
    print(f"⚠️  {message}")


def test_imports():
    """Test that all required modules can be imported."""
    print_header("Testing Imports")
    
    try:
        import requests
        print_success("requests module imported successfully")
    except ImportError:
        print_error("requests module not found. Install with: pip install requests")
        return False
    
    try:
        import keyring
        print_success("keyring module imported successfully")
    except ImportError:
        print_warning("keyring module not found. Install with: pip install keyring")
        print_info("Token storage will fall back to file storage")
    
    try:
        from dotenv import load_dotenv
        print_success("python-dotenv module imported successfully")
    except ImportError:
        print_warning("python-dotenv module not found. Install with: pip install python-dotenv")
        print_info("Environment variable loading may not work")
    
    return True


def test_configuration():
    """Test configuration loading."""
    print_header("Testing Configuration")
    
    # Test environment variables
    load_dotenv()
    client_id = os.getenv('GOTO_CLIENT_ID')
    client_secret = os.getenv('GOTO_CLIENT_SECRET')
    
    if client_id and client_secret:
        print_success("Environment variables found")
        print_info(f"Client ID: {client_id[:8]}...")
        print_info(f"Client Secret: {client_secret[:8]}...")
        return True
    else:
        print_warning("Environment variables not found")
        print_info("Make sure you have a .env file with:")
        print_info("GOTO_CLIENT_ID=your_client_id")
        print_info("GOTO_CLIENT_SECRET=your_client_secret")
        return False


def test_auth_initialization():
    """Test authentication object initialization."""
    print_header("Testing Authentication Initialization")
    
    try:
        # Try to initialize from environment
        auth = GoToConnectAuth.from_env()
        print_success("Authentication object initialized from environment variables")
        return auth
    except Exception as e:
        print_error(f"Failed to initialize from environment: {e}")
        
        # Try with direct initialization (for testing)
        print_info("Trying with placeholder credentials for testing...")
        try:
            auth = GoToConnectAuth(
                client_id="test_client_id",
                client_secret="test_client_secret"
            )
            print_success("Authentication object initialized with test credentials")
            return auth
        except Exception as e2:
            print_error(f"Failed to initialize with test credentials: {e2}")
            return None


def test_token_storage():
    """Test token storage functionality."""
    print_header("Testing Token Storage")
    
    try:
        from gotoconnect_auth.storage import KeyringTokenStorage, FileTokenStorage, MemoryTokenStorage
        
        # Test memory storage
        memory_storage = MemoryTokenStorage()
        test_tokens = {
            'access_token': 'test_token',
            'refresh_token': 'test_refresh',
            'expires_at': int(datetime.now().timestamp()) + 3600
        }
        
        memory_storage.save_tokens(test_tokens)
        loaded_tokens = memory_storage.load_tokens()
        
        if loaded_tokens == test_tokens:
            print_success("Memory token storage working correctly")
        else:
            print_error("Memory token storage test failed")
            return False
        
        # Test file storage
        file_storage = FileTokenStorage("test_tokens.json")
        file_storage.save_tokens(test_tokens)
        loaded_file_tokens = file_storage.load_tokens()
        
        if loaded_file_tokens == test_tokens:
            print_success("File token storage working correctly")
        else:
            print_error("File token storage test failed")
            return False
        
        # Clean up
        file_storage.clear_tokens()
        if os.path.exists("test_tokens.json"):
            os.remove("test_tokens.json")
        
        return True
        
    except Exception as e:
        print_error(f"Token storage test failed: {e}")
        return False


def test_api_endpoints(auth):
    """Test API endpoint connectivity."""
    print_header("Testing API Endpoints")
    
    if not auth:
        print_warning("Skipping API tests - no authentication object")
        return False
    
    # Test basic API connectivity
    try:
        # This is a simple connectivity test
        response = auth.get("https://api.goto.com/rest/users/v1/users/me")
        if response.status_code == 200:
            user_data = response.json()
            print_success("API connectivity test passed")
            print_info(f"Authenticated as: {user_data.get('firstName', '')} {user_data.get('lastName', '')}")
            return True
        else:
            print_error(f"API test failed with status code: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"API connectivity test failed: {e}")
        return False


def test_meeting_operations(auth):
    """Test meeting-related API operations."""
    print_header("Testing Meeting Operations")
    
    if not auth:
        print_warning("Skipping meeting tests - no authentication object")
        return False
    
    try:
        # Test getting meetings
        response = auth.get("https://api.goto.com/rest/meetings/v1/meetings?limit=5")
        if response.status_code == 200:
            meetings_data = response.json()
            meeting_count = len(meetings_data.get('meetings', []))
            print_success(f"Successfully retrieved {meeting_count} meetings")
            
            # Test creating a meeting (will be cleaned up)
            test_meeting = {
                "subject": "Test Meeting - Authentication Library",
                "startTime": (datetime.utcnow() + timedelta(hours=1)).isoformat() + "Z",
                "endTime": (datetime.utcnow() + timedelta(hours=2)).isoformat() + "Z",
                "description": "This is a test meeting created by the authentication library test script"
            }
            
            create_response = auth.post(
                "https://api.goto.com/rest/meetings/v1/meetings",
                json=test_meeting
            )
            
            if create_response.status_code == 201:
                new_meeting = create_response.json()
                meeting_id = new_meeting.get('meetingId')
                print_success(f"Successfully created test meeting: {meeting_id}")
                
                # Clean up - delete the test meeting
                delete_response = auth.delete(f"https://api.goto.com/rest/meetings/v1/meetings/{meeting_id}")
                if delete_response.status_code == 204:
                    print_success("Successfully cleaned up test meeting")
                else:
                    print_warning(f"Could not clean up test meeting: {delete_response.status_code}")
                
                return True
            else:
                print_error(f"Failed to create test meeting: {create_response.status_code}")
                return False
        else:
            print_error(f"Failed to retrieve meetings: {response.status_code}")
            return False
            
    except Exception as e:
        print_error(f"Meeting operations test failed: {e}")
        return False


def run_comprehensive_test():
    """Run all tests and provide a summary."""
    print_header("GoTo Connect Authentication Library Test Suite")
    print_info("This script will test your authentication setup")
    print_info("Make sure you have configured your credentials first")
    
    results = {
        'imports': False,
        'configuration': False,
        'auth_init': False,
        'token_storage': False,
        'api_connectivity': False,
        'meeting_operations': False
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
    
    # Test API connectivity
    results['api_connectivity'] = test_api_endpoints(auth)
    
    # Test meeting operations
    results['meeting_operations'] = test_meeting_operations(auth)
    
    # Print summary
    print_header("Test Results Summary")
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name.replace('_', ' ').title()}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your authentication library is working correctly.")
        print_info("You can now use this library in your projects.")
    elif passed >= total - 2:
        print_warning("⚠️  Most tests passed. Some features may not work as expected.")
        print_info("Check the failed tests above for more information.")
    else:
        print_error("❌ Multiple tests failed. Please check your configuration.")
        print_info("Make sure you have:")
        print_info("1. Set up your GoTo Connect application")
        print_info("2. Configured your credentials in .env file")
        print_info("3. Installed all required dependencies")
    
    return passed == total


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