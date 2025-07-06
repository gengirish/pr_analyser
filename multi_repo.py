#!/usr/bin/env python3
"""
Multi-Repository Example for GitHub PR Analyzer

This script demonstrates how to use the GitHub PR Analyzer to analyze multiple repositories
in a single run. This is useful for analyzing PRs across multiple related repositories.
"""

import argparse
import datetime
import json
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs across multiple repositories')
    parser.add_argument('repos', help='Comma-separated list of repositories in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path for JSON results (optional)')
    parser.add_argument('--date', help='Custom date filter in YYYY-MM-DD format (default: 2024-11-01)', 
                        default='2024-11-01')
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
            print(f"Error fetching PRs for {owner}/{repo}: {response.status_code}")
            print(response.json().get('message', 'Unknown error'))
            return []
        
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


def analyze_repository(owner, repo, headers, target_date, min_files):
    """Analyze a single repository and return filtered PRs."""
    print(f"Fetching pull requests for {owner}/{repo}...")
    all_prs = get_pull_requests(owner, repo, headers)
    print(f"Found {len(all_prs)} pull requests in total.")
    
    # Filter and analyze PRs
    filtered_prs = []
    
    print(f"Analyzing pull requests...")
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
        
        # Check if PR has minimum number of file changes
        if len(files) >= min_files:
            filtered_prs.append({
                'repository': f"{owner}/{repo}",
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at.isoformat(),
                'url': pr['html_url'],
                'files_changed': len(files),
                'author': pr['user']['login']
            })
    
    return filtered_prs


def main():
    """Main function to run the script."""
    args = parse_arguments()
    
    # Parse repositories
    repos = [repo.strip() for repo in args.repos.split(',') if repo.strip()]
    if not repos:
        print("Error: At least one repository must be specified")
        sys.exit(1)
    
    # Validate repository format
    for repo in repos:
        if '/' not in repo:
            print(f"Error: Repository '{repo}' must be in the format 'owner/repo'")
            sys.exit(1)
    
    # Parse the custom date filter
    try:
        target_date = datetime.datetime.strptime(args.date, '%Y-%m-%d')
        target_date = target_date.replace(tzinfo=datetime.timezone.utc)
    except ValueError:
        print("Error: Date must be in the format YYYY-MM-DD")
        sys.exit(1)
    
    # Set up API headers
    headers = get_github_api_headers(args.token)
    
    # Analyze each repository
    all_filtered_prs = []
    
    for repo in repos:
        owner, repo_name = repo.split('/')
        filtered_prs = analyze_repository(owner, repo_name, headers, target_date, args.min_files)
        all_filtered_prs.extend(filtered_prs)
        print(f"Found {len(filtered_prs)} matching PRs in {owner}/{repo_name}")
        print("-" * 80)
    
    # Sort by merge date (newest first)
    all_filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    # Create result object
    result = {
        'repositories': repos,
        'date_filter': args.date,
        'min_files': args.min_files,
        'total_prs_found': len(all_filtered_prs),
        'prs': all_filtered_prs
    }
    
    # Output results
    if args.output:
        # Write to file
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to {args.output}")
    else:
        # Display results
        print("\nResults:")
        print(f"Found {len(all_filtered_prs)} PRs across {len(repos)} repositories")
        print(f"with {args.min_files}+ file changes merged after {args.date}")
        print("\n" + "-" * 80)
        
        for pr in all_filtered_prs:
            print(f"Repository: {pr['repository']}")
            print(f"PR #{pr['number']}: {pr['title']}")
            print(f"  Author: {pr['author']}")
            print(f"  Merged: {pr['merged_at']}")
            print(f"  Files changed: {pr['files_changed']}")
            print(f"  URL: {pr['url']}")
            print("-" * 80)


if __name__ == "__main__":
    main()
