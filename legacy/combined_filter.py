#!/usr/bin/env python3
"""
Combined Filter Example for GitHub PR Analyzer

This script demonstrates how to combine multiple filters in the GitHub PR Analyzer.
In this example, we'll find PRs with 2+ file changes merged after a custom date
that were authored by specific users and include changes to specific file types.
"""

import argparse
import datetime
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with combined filters')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--date', help='Custom date filter in YYYY-MM-DD format (default: 2024-11-01)', 
                        default='2024-11-01')
    parser.add_argument('--authors', help='Comma-separated list of GitHub usernames to filter by (optional)')
    parser.add_argument('--file-types', help='Comma-separated list of file extensions to filter by (optional)')
    parser.add_argument('--min-files', type=int, help='Minimum number of files changed (default: 2)', 
                        default=2)
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
    
    # Parse the custom date filter
    try:
        target_date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        target_date = target_date.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        print("Error: Date must be in the format YYYY-MM-DD")
        sys.exit(1)
    
    # Parse authors to filter by (if provided)
    authors = None
    if args.authors:
        authors = [a.strip().lower() for a in args.authors.split(',') if a.strip()]
    
    # Parse file types to filter by (if provided)
    file_types = None
    if args.file_types:
        file_types = [f.strip().lower() for f in args.file_types.split(',') if f.strip()]
        # Add leading dot to file types if not present
        file_types = [f if f.startswith('.') else f'.{f}' for f in file_types]
    
    # Set up API headers
    headers = get_github_api_headers(args.token)
    
    # Get all PRs
    print(f"Fetching pull requests for {owner}/{repo}...")
    all_prs = get_pull_requests(owner, repo, headers)
    print(f"Found {len(all_prs)} pull requests in total.")
    
    # Build filter description for output
    filter_desc = [f"merged after {args.date}", f"with {args.min_files}+ file changes"]
    if authors:
        filter_desc.append(f"authored by: {', '.join(authors)}")
    if file_types:
        filter_desc.append(f"including changes to files with extensions: {', '.join(file_types)}")
    
    # Filter and analyze PRs
    filtered_prs = []
    
    print(f"Analyzing pull requests ({' and '.join(filter_desc)})...")
    for pr in all_prs:
        pr_number = pr['number']
        
        # Skip if PR is not merged
        if not pr['merged_at']:
            continue
        
        # Check merge date
        merged_at = date_parser.parse(pr['merged_at'])
        if merged_at <= target_date:
            continue
        
        # Check if PR is authored by one of the specified authors (if filter is active)
        if authors:
            pr_author = pr['user']['login'].lower()
            if pr_author not in authors:
                continue
        
        # Get files changed in this PR
        files = get_pr_files(owner, repo, pr_number, headers)
        
        # Check if PR has minimum number of file changes
        if len(files) < args.min_files:
            continue
        
        # Check if PR includes changes to specified file types (if filter is active)
        if file_types:
            matching_files = []
            for file in files:
                filename = file['filename']
                for file_type in file_types:
                    if filename.lower().endswith(file_type):
                        matching_files.append(filename)
                        break
            
            # Skip if no matching files found
            if not matching_files:
                continue
            
            # Add matching files to PR data
            pr_data = {
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at,
                'url': pr['html_url'],
                'files_changed': len(files),
                'matching_files': matching_files,
                'author': pr['user']['login']
            }
        else:
            # No file type filter active
            pr_data = {
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at,
                'url': pr['html_url'],
                'files_changed': len(files),
                'author': pr['user']['login']
            }
        
        filtered_prs.append(pr_data)
    
    # Display results
    print("\nResults:")
    print(f"Found {len(filtered_prs)} PRs {' and '.join(filter_desc)}")
    print("\n" + "-" * 80)
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    for pr in filtered_prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['author']}")
        print(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Files changed: {pr['files_changed']}")
        
        if 'matching_files' in pr:
            print(f"  Matching files: {len(pr['matching_files'])}")
            print(f"  Matching file examples: {', '.join(pr['matching_files'][:3])}")
            if len(pr['matching_files']) > 3:
                print(f"    ... and {len(pr['matching_files']) - 3} more")
        
        print(f"  URL: {pr['url']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
