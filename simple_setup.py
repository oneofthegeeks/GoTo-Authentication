#!/usr/bin/env python3
"""
Simple Setup Script for GoTo Connect Authentication Library

This script helps you get started quickly with the authentication library.
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


def create_env_file():
    """Create a .env file with example values."""
    env_file = Path(".env")
    if env_file.exists():
        print("📝 .env file already exists, skipping creation")
        return True
    
    print("📝 Creating .env file...")
    env_content = """# GoTo Connect API Credentials
# Get these from https://developer.goto.com/
GOTO_CLIENT_ID=your_client_id_here
GOTO_CLIENT_SECRET=your_client_secret_here
GOTO_REDIRECT_URI=http://localhost:8080/callback
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


def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    dependencies = [
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
        "keyring>=23.0.0"
    ]
    
    for dep in dependencies:
        if not run_command(f"{sys.executable} -m pip install '{dep}'", f"Installing {dep}"):
            return False
    
    return True


def main():
    """Main setup function."""
    print("🚀 GoTo Connect Authentication Library - Simple Setup")
    print("=" * 60)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Get your GoTo Connect API credentials from https://developer.goto.com/")
    print("2. Update the .env file with your credentials")
    print("3. Test your setup:")
    print("   python examples/simple_example.py")
    print("\n📚 For more information, see the README.md file")


if __name__ == "__main__":
    main()
