#!/usr/bin/env python3
"""
JSON Output Example for GitHub PR Analyzer

This script demonstrates how to modify the GitHub PR Analyzer to output results in JSON format.
This is useful for programmatic processing of the results or integration with other tools.
"""

import argparse
import datetime
import json
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with 2+ file changes merged after Nov 2024 (JSON output)')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path for JSON results (optional, defaults to stdout)')
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
    
    # Set up API headers
    headers = get_github_api_headers(args.token)
    
    # Get all PRs
    print(f"Fetching pull requests for {owner}/{repo}...", file=sys.stderr)
    all_prs = get_pull_requests(owner, repo, headers)
    print(f"Found {len(all_prs)} pull requests in total.", file=sys.stderr)
    
    # Target date: November 1, 2024
    target_date = datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc)
    
    # Filter and analyze PRs
    filtered_prs = []
    
    print("Analyzing pull requests...", file=sys.stderr)
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
        if len(files) >= 2:
            filtered_prs.append({
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at.isoformat(),
                'url': pr['html_url'],
                'files_changed': len(files),
                'author': pr['user']['login']
            })
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    # Create result object
    result = {
        'repository': f"{owner}/{repo}",
        'date_filter': "2024-11-01",
        'total_prs_found': len(all_prs),
        'filtered_prs_count': len(filtered_prs),
        'filtered_prs': filtered_prs
    }
    
    # Output JSON result
    json_result = json.dumps(result, indent=2)
    
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json_result)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(json_result)


if __name__ == "__main__":
    main()
