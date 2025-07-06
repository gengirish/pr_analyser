#!/usr/bin/env python3
"""
GitHub PR Analyzer

This script analyzes a GitHub repository to find pull requests that:
1. Have 2 to 4 file changes
2. Were merged after November 2024
3. Include test classes

Usage:
    python github_pr_analyzer.py [--token GITHUB_TOKEN] [--output OUTPUT_FILE] owner/repo

Arguments:
    owner/repo      GitHub repository in the format "owner/repo"
    --token         GitHub personal access token (optional but recommended to avoid rate limits)
    --output        Output file path to save results (optional)

Examples:
    python github_pr_analyzer.py --token ghp_abc123 octocat/hello-world
    python github_pr_analyzer.py --token ghp_abc123 --output results.txt octocat/hello-world
"""

import argparse
import datetime
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with 2-4 file changes that include test classes, merged after Nov 2024')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path to save results (optional)')
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


def get_pr_details(owner, repo, pr_number, headers):
    """Get detailed information about a specific PR."""
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR details: {response.status_code}")
        return None
        
    return response.json()


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
    
    # Set up output file if specified
    output_file = None
    if args.output:
        try:
            output_file = open(args.output, 'w')
            print(f"Results will be saved to {args.output}")
        except Exception as e:
            print(f"Error opening output file: {e}")
            print("Results will only be displayed on screen")
    
    # Function to print to both console and file if specified
    def print_output(message):
        print(message)
        if output_file:
            print(message, file=output_file)
    
    # Parse owner and repo from the repo argument
    try:
        owner, repo = args.repo.split('/')
    except ValueError:
        print("Error: Repository must be in the format 'owner/repo'")
        sys.exit(1)
    
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
    
    print("Analyzing pull requests...")
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
        
        # Check if PR has 2 to 4 file changes
        if 2 <= len(files) <= 4:
            # Check if any of the files are test files
            has_test_files = False
            test_files = []
            
            for file in files:
                filename = file['filename'].lower()
                # Check for common test file patterns
                if 'test' in filename or 'spec' in filename:
                    has_test_files = True
                    test_files.append(file['filename'])
            
            # Only include PRs that have test files
            if has_test_files:
                filtered_prs.append({
                    'number': pr_number,
                    'title': pr['title'],
                    'merged_at': merged_at,
                    'url': pr['html_url'],
                    'files_changed': len(files),
                    'author': pr['user']['login'],
                    'test_files': test_files
                })
    
    # Display results
    print_output("\nResults:")
    print_output(f"Found {len(filtered_prs)} PRs with 2-4 file changes that include test classes, merged after November 2024:")
    print_output("\n" + "-" * 80)
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    for pr in filtered_prs:
        print_output(f"PR #{pr['number']}: {pr['title']}")
        print_output(f"  Author: {pr['author']}")
        print_output(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print_output(f"  Files changed: {pr['files_changed']}")
        print_output(f"  Test files: {', '.join(pr['test_files'])}")
        print_output(f"  URL: {pr['url']}")
        print_output("-" * 80)
    
    # Close output file if opened
    if output_file:
        output_file.close()
        print(f"Results have been saved to {args.output}")


if __name__ == "__main__":
    main()
