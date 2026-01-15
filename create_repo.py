#!/usr/bin/env python3
"""Create new GitHub repository JC_AGENT-V2."""
from jc.key_locker import KeyLocker
import requests
import sys

def main():
    # Get token from KeyLocker
    kl = KeyLocker()
    keys = kl.list_keys()
    github = [k for k in keys if k['name'] == 'GITHUB_TOKEN'][0]
    token = kl.get_secret(github['id'])
    
    # Validate token
    if not token or len(token) < 10:
        print(f"ERROR: Invalid token (length: {len(token) if token else 0})")
        return 1
    
    print(f"Token retrieved: {len(token)} characters")
    
    # Create repository
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': 'JC_AGENT-V2',
        'description': 'JC Agent Version 2 - AI-powered agent with enhanced capabilities',
        'private': False,
        'auto_init': False
    }
    
    print("Creating repository...")
    r = requests.post('https://api.github.com/user/repos', headers=headers, json=data)
    
    print(f"Status: {r.status_code}")
    
    if r.status_code == 201:
        result = r.json()
        print(f"✓ Repository created: {result['html_url']}")
        print(f"  Clone URL: {result['clone_url']}")
        return 0
    else:
        print(f"ERROR: {r.text}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
