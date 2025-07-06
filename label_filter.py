#!/usr/bin/env python3
"""
Label Filter Example for GitHub PR Analyzer

This script demonstrates how to modify the GitHub PR Analyzer to filter PRs by specific labels.
In this example, we'll find PRs with 2+ file changes merged after November 2024 that have
specific labels (e.g., "bug", "enhancement", "documentation").
"""

import argparse
import datetime
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with specific labels')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--labels', help='Comma-separated list of labels to filter by (e.g., "bug,enhancement")',
                        required=True)
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


def get_pr_labels(owner, repo, pr_number, headers):
    """Get labels for a specific PR."""
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR labels: {response.status_code}")
        return []
    
    issue_data = response.json()
    return [label['name'] for label in issue_data.get('labels', [])]


def main():
    """Main function to run the script."""
    args = parse_arguments()
    
    # Parse owner and repo from the repo argument
    try:
        owner, repo = args.repo.split('/')
    except ValueError:
        print("Error: Repository must be in the format 'owner/repo'")
        sys.exit(1)
    
    # Parse labels to filter by
    labels = [label.strip().lower() for label in args.labels.split(',') if label.strip()]
    if not labels:
        print("Error: At least one label must be specified")
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
    
    print(f"Analyzing pull requests (labels: {', '.join(labels)})...")
    for pr in all_prs:
        pr_number = pr['number']
        
        # Skip if PR is not merged
        if not pr['merged_at']:
            continue
        
        # Check merge date
        merged_at = date_parser.parse(pr['merged_at'])
        if merged_at <= target_date:
            continue
        
        # Get PR labels
        pr_labels = get_pr_labels(owner, repo, pr_number, headers)
        pr_labels_lower = [label.lower() for label in pr_labels]
        
        # Check if PR has any of the specified labels
        matching_labels = [label for label in labels if label in pr_labels_lower]
        if not matching_labels:
            continue
        
        # Get files changed in this PR
        files = get_pr_files(owner, repo, pr_number, headers)
        
        # Check if PR has 2 or more file changes
        if len(files) >= 2:
            filtered_prs.append({
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at,
                'url': pr['html_url'],
                'files_changed': len(files),
                'author': pr['user']['login'],
                'labels': pr_labels
            })
    
    # Display results
    print("\nResults:")
    print(f"Found {len(filtered_prs)} PRs with 2+ file changes merged after November 2024")
    print(f"that have labels: {', '.join(labels)}")
    print("\n" + "-" * 80)
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    for pr in filtered_prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['author']}")
        print(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Files changed: {pr['files_changed']}")
        print(f"  Labels: {', '.join(pr['labels'])}")
        print(f"  URL: {pr['url']}")
        print("-" * 80)


if __name__ == "__main__":
    main()
