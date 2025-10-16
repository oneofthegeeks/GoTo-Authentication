#!/usr/bin/env python3
"""
GitHub Release Creation Script

This script helps create a GitHub release for the GoTo Connect Authentication Library.
"""

import os
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False


def check_git_status():
    """Check if git repository is clean."""
    print("🔍 Checking git status...")
    
    try:
        result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  There are uncommitted changes:")
            print(result.stdout)
            return False
        else:
            print("✅ Git repository is clean")
            return True
    except Exception as e:
        print(f"❌ Error checking git status: {e}")
        return False


def check_tag_exists():
    """Check if the tag already exists."""
    print("🔍 Checking if tag v1.0.0 exists...")
    
    try:
        result = subprocess.run("git tag -l v1.0.0", shell=True, capture_output=True, text=True)
        if "v1.0.0" in result.stdout:
            print("✅ Tag v1.0.0 exists")
            return True
        else:
            print("❌ Tag v1.0.0 does not exist")
            return False
    except Exception as e:
        print(f"❌ Error checking tag: {e}")
        return False


def create_release_notes():
    """Create release notes for the GitHub release."""
    print("📝 Creating release notes...")
    
    release_notes = """# GoTo Connect Authentication Library v1.0.0

## 🎉 Major Release: Simplified Authentication Library

This release introduces a completely redesigned and simplified GoTo Connect authentication library that makes API authentication easy and reusable for any Python project.

## ✨ What's New

### 🚀 Simplified Authentication
- **One-line setup**: `auth = GoToConnectAuth.from_env()`
- **Automatic browser opening**: No manual URL navigation required
- **Environment variable support**: Uses `.env` files for easy configuration
- **Clean API**: Intuitive methods for all operations

### 🔄 Automatic Token Refresh
- **No manual intervention**: Tokens refresh automatically when they expire
- **Seamless experience**: Users don't need to re-authenticate
- **Smart storage**: Uses system keyring with file fallback
- **Background handling**: All complexity is handled behind the scenes

### 🔒 Enhanced Security
- **Secure storage**: Uses system keyring by default for token storage
- **File fallback**: Falls back to file storage if keyring unavailable
- **No hardcoded credentials**: All examples use placeholders
- **HTTPS only**: All API calls use secure connections

### 📦 Minimal Dependencies
- **Only 3 essential packages**: requests, python-dotenv, keyring
- **No conflicts**: Clean dependency tree
- **Fast installation**: Quick setup and deployment
- **Version constraints**: Proper version requirements

## 🚀 Quick Start

### Installation
```bash
pip install gotoconnect-auth
```

### Basic Usage
```python
from gotoconnect_auth import GoToConnectAuth

# Initialize authentication
auth = GoToConnectAuth.from_env()

# Authenticate (opens browser for first-time auth)
auth.authenticate()

# Make API calls
response = auth.get("https://api.goto.com/rest/users/v1/users/me")
user_info = response.json()
print(f"Hello, {user_info.get('firstName', '')}!")
```

## 🔧 Key Features

- **Simple Authentication**: One-line setup with environment variables
- **Automatic Token Refresh**: No manual intervention needed
- **Secure Storage**: Uses system keyring with file fallback
- **HTTP Methods**: GET, POST, PUT, DELETE with automatic authentication
- **Error Handling**: Comprehensive exception handling
- **Type Hints**: Full type annotations for better IDE support

## 📚 Documentation

- **README.md**: Quick start guide and overview
- **USAGE_GUIDE.md**: Detailed usage examples and patterns
- **Examples**: Working code examples for all use cases
- **API Reference**: Complete method documentation

## 🛠️ Development

```bash
# Clone the repository
git clone https://github.com/oneofthegeeks/GoTo-Authentication.git
cd GoTo-Authentication

# Install in development mode
pip install -e .

# Run tests
python test_release.py
```

## 🔒 Security

- **Environment variables**: Use `.env` files for development
- **Production ready**: Use environment variables in production
- **HTTPS only**: All API calls use secure connections
- **Secure storage**: Uses system keyring by default

## 🎯 Benefits

1. **Faster Setup**: Get started in under 5 minutes
2. **Fewer Dependencies**: Only 3 essential packages
3. **Clearer Code**: Easy to understand and modify
4. **Better Documentation**: Focused on what users need
5. **Simpler Examples**: Easy to copy and modify
6. **Automatic Token Refresh**: No manual intervention needed
7. **Secure Storage**: Uses system keyring by default

## 📞 Support

- 📖 **Documentation**: Check README.md and USAGE_GUIDE.md
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Discussions**: Start a discussion for questions

---

**Ready to get started?** Check out the [Quick Start Guide](README.md) or [Detailed Usage Guide](USAGE_GUIDE.md) to begin using the simplified GoTo Connect authentication library!"""
    
    try:
        with open("RELEASE_NOTES_v1.0.0.md", "w") as f:
            f.write(release_notes)
        print("✅ Release notes created successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to create release notes: {e}")
        return False


def main():
    """Main function to create GitHub release."""
    print("🚀 GoTo Connect Authentication Library - GitHub Release Creation")
    print("=" * 70)
    
    # Check git status
    if not check_git_status():
        print("❌ Please commit all changes before creating a release")
        sys.exit(1)
    
    # Check if tag exists
    if not check_tag_exists():
        print("❌ Please create the tag first: git tag -a v1.0.0 -m 'Release v1.0.0'")
        sys.exit(1)
    
    # Create release notes
    if not create_release_notes():
        print("❌ Failed to create release notes")
        sys.exit(1)
    
    print("\n🎉 Ready to create GitHub release!")
    print("\n📋 Next steps:")
    print("1. Go to https://github.com/oneofthegeeks/GoTo-Authentication/releases")
    print("2. Click 'Create a new release'")
    print("3. Select tag 'v1.0.0'")
    print("4. Set title to 'GoTo Connect Authentication Library v1.0.0'")
    print("5. Copy the contents of RELEASE_NOTES_v1.0.0.md into the description")
    print("6. Click 'Publish release'")
    print("\n💡 The release notes are saved in RELEASE_NOTES_v1.0.0.md")


if __name__ == "__main__":
    main()
