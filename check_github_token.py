#!/usr/bin/env python3
"""
Check GitHub Token

This script checks if the GITHUB_TOKEN environment variable is set and tests its validity
by making a simple API request to GitHub.

Usage:
    python check_github_token.py
"""

import os
import requests
import sys

def check_token():
    """Check if GITHUB_TOKEN environment variable is set and valid."""
    # Check if token exists in environment
    token = os.environ.get('GITHUB_TOKEN')
    
    if not token:
        print("❌ GITHUB_TOKEN environment variable is not set.")
        print("\nTo set the token:")
        print("- Windows: set GITHUB_TOKEN=your_token_here")
        print("- Unix/Linux/Mac: export GITHUB_TOKEN=your_token_here")
        print("\nOr use the provided helper scripts:")
        print("- Windows: set_permanent_token_windows.bat your_token_here")
        print("- Unix/Linux/Mac: ./set_permanent_token_unix.sh your_token_here")
        return False
    
    # Mask token for display
    masked_token = token[:4] + "..." + token[-4:] if len(token) > 8 else "****"
    print(f"✓ GITHUB_TOKEN is set: {masked_token}")
    
    # Test token with a simple API request
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'Authorization': f'token {token}'
    }
    
    print("Testing token validity with GitHub API...")
    
    try:
        response = requests.get('https://api.github.com/user', headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✓ Token is valid! Authenticated as: {user_data.get('login')}")
            print(f"✓ Rate limit: {response.headers.get('X-RateLimit-Remaining', 'Unknown')}/{response.headers.get('X-RateLimit-Limit', 'Unknown')} requests remaining")
            return True
        elif response.status_code == 401:
            print("❌ Token is invalid or expired. Please generate a new token.")
            return False
        else:
            print(f"❌ Unexpected response from GitHub API: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

if __name__ == "__main__":
    print("Checking GitHub Token Configuration")
    print("==================================")
    
    if check_token():
        print("\n✓ Your GitHub token is properly configured!")
        print("You can now run the trending Java projects analyzer.")
    else:
        print("\n❌ GitHub token configuration issue detected.")
        print("Please set up your token correctly before running the analyzer.")
        sys.exit(1)
