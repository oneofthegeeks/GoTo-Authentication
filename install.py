#!/usr/bin/env python3
"""
Installation script for GoTo Connect Authentication Library.
"""

import os
import sys
import subprocess
import json
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
        print(f"Error output: {e.stderr}")
        return False


def create_env_file():
    """Create a .env file with example values."""
    env_file = Path(".env")
    if env_file.exists():
        print("📝 .env file already exists, skipping creation")
        return True
    
    print("📝 Creating .env file...")
    env_content = """# GoTo Connect API Credentials
GOTO_CLIENT_ID=your_go_to_connect_client_id_here
GOTO_CLIENT_SECRET=your_go_to_connect_client_secret_here

# OAuth Configuration (optional - defaults will be used if not set)
GOTO_REDIRECT_URI=http://localhost:8080/callback
GOTO_AUTH_URL=https://authentication.logmeininc.com/oauth/authorize
GOTO_TOKEN_URL=https://authentication.logmeininc.com/oauth/token
"""
    
    try:
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully")
        print("⚠️  Please update the .env file with your actual GoTo Connect credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def create_config_file():
    """Create a config.json file with example values."""
    config_file = Path("config.json")
    if config_file.exists():
        print("📝 config.json file already exists, skipping creation")
        return True
    
    print("📝 Creating config.json file...")
    config_content = {
        "client_id": "your_go_to_connect_client_id_here",
        "client_secret": "your_go_to_connect_client_secret_here",
        "redirect_uri": "http://localhost:8080/callback",
        "auth_url": "https://authentication.logmeininc.com/oauth/authorize",
        "token_url": "https://authentication.logmeininc.com/oauth/token"
    }
    
    try:
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=4)
        print("✅ config.json file created successfully")
        print("⚠️  Please update the config.json file with your actual GoTo Connect credentials")
        return True
    except Exception as e:
        print(f"❌ Failed to create config.json file: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], check=True, capture_output=True)
    except subprocess.CalledProcessError:
        print("❌ pip is not available. Please install pip first.")
        return False
    
    # Install dependencies
    dependencies = [
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "keyring>=23.0.0",
        "cryptography>=3.4.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep}"):
            return False
    
    return True


def install_package():
    """Install the package in development mode."""
    print("📦 Installing package in development mode...")
    return run_command(f"{sys.executable} -m pip install -e .", "Installing package")


def run_tests():
    """Run the test suite."""
    print("🧪 Running tests...")
    return run_command(f"{sys.executable} -m pytest tests/ -v", "Running tests")


def main():
    """Main installation function."""
    print("🚀 GoTo Connect Authentication Library Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Install package
    if not install_package():
        print("❌ Failed to install package")
        sys.exit(1)
    
    # Create configuration files
    create_env_file()
    create_config_file()
    
    # Run tests
    print("\n🧪 Running tests to verify installation...")
    if run_tests():
        print("✅ All tests passed!")
    else:
        print("⚠️  Some tests failed, but installation completed")
    
    print("\n🎉 Installation completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your GoTo Connect API credentials from https://developer.goto.com/")
    print("2. Update the .env file or config.json with your credentials")
    print("3. Run the examples:")
    print("   python examples/basic_usage.py")
    print("   python examples/meeting_manager.py")
    print("\n📚 For more information, see the README.md file")


if __name__ == "__main__":
    main() 