#!/usr/bin/env python3
"""
File Type Filter Example for GitHub PR Analyzer

This script demonstrates how to modify the GitHub PR Analyzer to filter PRs by specific file types.
In this example, we'll find PRs with 2+ file changes merged after November 2024 that include
changes to specific file types (e.g., .py, .js, .html).
"""

import argparse
import datetime
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with specific file types changed')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--file-types', help='Comma-separated list of file extensions to filter by (e.g., "py,js,html")',
                        default='py')
    return parser.parse_args()


def get_github_api_headers(token=None):
    """Create headers for GitHub API requests."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def get_pull_requests(owner, repo, headers):
    """Fetch all pull requests from a GitHub repository."""
    all_prs = []
    page = 1
    per_page = 100
    
    while True:
        url = f'https://api.github.com/repos/{owner}/{repo}/pulls'
        params = {
            'state': 'all',  # Get all PRs (open, closed, merged)
            'per_page': per_page,
            'page': page
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching PRs: {response.status_code}")
            print(response.json().get('message', 'Unknown error'))
            sys.exit(1)
        
        prs = response.json()
        if not prs:
            break
            
        all_prs.extend(prs)
        page += 1
        
        # Check if we've reached the last page
        if len(prs) < per_page:
            break
    
    return all_prs


def get_pr_files(owner, repo, pr_number, headers):
    """Get files changed in a specific PR."""
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR files: {response.status_code}")
        return []
        
    return response.json()


def main():
    """Main function to run the script."""
    args = parse_arguments()
    
    # Parse owner and repo from the repo argument
    try:
        owner, repo = args.repo.split('/')
    except ValueError:
        print("Error: Repository must be in the format 'owner/repo'")
        sys.exit(1)
    
    # Parse file types to filter by
    file_types = [f.strip().lower() for f in args.file_types.split(',')]
    if not file_types:
        print("Error: At least one file type must be specified")
        sys.exit(1)
    
    # Add leading dot to file types if not present
    file_types = [f if f.startswith('.') else f'.{f}' for f in file_types]
    
    # Set up API headers
    headers = get_github_api_headers(args.token)
    
    # Get all PRs
    print(f"Fetching pull requests for {owner}/{repo}...")
    all_prs = get_pull_requests(owner, repo, headers)
    print(f"Found {len(all_prs)} pull requests in total.")
    
    # Target date: November 1, 2024
    target_date = datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc)
    
    # Filter and analyze PRs
    filtered_prs = []
    
    print(f"Analyzing pull requests (file types: {', '.join(file_types)})...")
    for pr in all_prs:
        pr_number = pr['number']
        
        # Skip if PR is not merged
        if not pr['merged_at']:
            continue
        
        # Check merge date
        merged_at = date_parser.parse(pr['merged_at'])
        if merged_at <= target_date:
            continue
        
        # Get files changed in this PR
        files = get_pr_files(owner, repo, pr_number, headers)
        
        # Check if PR has 2 or more file changes
        if len(files) < 2:
            continue
        
        # Check if PR includes changes to specified file types
        matching_files = []
        for file in files:
            filename = file['filename']
            for file_type in file_types:
                if filename.lower().endswith(file_type):
                    matching_files.append(filename)
                    break
        
        # Only include PR if it has changes to specified file types
        if matching_files:
            filtered_prs.append({
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at,
                'url': pr['html_url'],
                'files_changed': len(files),
                'matching_files': matching_files,
                'author': pr['user']['login']
            })
    
    # Display results
    print("\nResults:")
    print(f"Found {len(filtered_prs)} PRs with 2+ file changes merged after November 2024")
    print(f"that include changes to files with extensions: {', '.join(file_types)}")
    print("\n" + "-" * 80)
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    for pr in filtered_prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['author']}")
        print(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Files changed: {pr['files_changed']} (total)")
        print(f"  Matching files: {len(pr['matching_files'])}")
        print(f"  Matching file examples: {', '.join(pr['matching_files'][:3])}")
        if len(pr['matching_files']) > 3:
            print(f"    ... and {len(pr['matching_files']) - 3} more")
        print(f"  URL: {pr['url']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
