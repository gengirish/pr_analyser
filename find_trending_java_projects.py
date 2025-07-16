#!/usr/bin/env python3
"""
Find Trending Java Projects and Analyze PRs

This script:
1. Finds the top 10 trending Java projects on GitHub
2. Runs the github_pr_analyzer.py script on each project
3. Creates output files with PR data

Usage:
    python find_trending_java_projects.py [--token GITHUB_TOKEN] [--limit PR_LIMIT]

Arguments:
    --token         GitHub personal access token (optional but recommended to avoid rate limits)
    --limit         Maximum number of matching PRs to find per repository (default: 20)

Examples:
    python find_trending_java_projects.py --token ghp_abc123
    python find_trending_java_projects.py --token ghp_abc123 --limit 10
"""

import argparse
import datetime
import os
import requests
import subprocess
import sys

# Check for GitHub token in environment variable
DEFAULT_GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find trending Java projects and analyze their PRs')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended, defaults to GITHUB_TOKEN environment variable if set)')
    parser.add_argument('--limit', type=int, default=20, help='Maximum number of matching PRs to find per repository (default: 20)')
    args = parser.parse_args()
    
    # Use environment variable for token if not provided as argument
    if not args.token and DEFAULT_GITHUB_TOKEN:
        print("Using GitHub token from GITHUB_TOKEN environment variable")
        args.token = DEFAULT_GITHUB_TOKEN
        
    return args


def get_github_api_headers(token=None):
    """Create headers for GitHub API requests."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def get_trending_java_projects(headers, count=10):
    """Get trending Java projects from GitHub.
    
    Args:
        headers (dict): API request headers
        count (int): Number of trending projects to retrieve
    
    Returns:
        list: List of trending Java repositories in the format [owner/repo, ...]
    """
    # GitHub search API to find popular Java repositories
    # Sorted by stars and limited to Java language
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': 'language:java',
        'sort': 'stars',
        'order': 'desc',
        'per_page': count
    }
    
    print(f"Fetching top {count} trending Java projects from GitHub...")
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"Error fetching trending projects: {response.status_code}")
        print(response.json().get('message', 'Unknown error'))
        sys.exit(1)
    
    data = response.json()
    trending_repos = []
    
    for repo in data.get('items', []):
        repo_full_name = repo['full_name']  # Format: owner/repo
        trending_repos.append(repo_full_name)
        
    return trending_repos


def analyze_repository(repo, token=None, pr_limit=20):
    """Run github_pr_analyzer.py on a repository.
    
    Args:
        repo (str): Repository in the format "owner/repo"
        token (str, optional): GitHub personal access token
        pr_limit (int): Maximum number of matching PRs to find
    
    Returns:
        str: Path to the output file, or None if analysis failed
    """
    # Create a unique output filename for this repository
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"pr-output/{repo.replace('/', '-')}-pr-{pr_limit}.txt"
    
    # Build the command to run github_pr_analyzer.py
    cmd = [sys.executable, 'github_pr_analyzer.py']
    
    if token:
        cmd.extend(['--token', token])
    
    cmd.extend(['--output', output_filename, '--limit', str(pr_limit), repo])
    
    print(f"\nAnalyzing repository: {repo}")
    print(f"Output will be saved to: {output_filename}")
    
    try:
        # Run the github_pr_analyzer.py script
        process = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(process.stdout)
        
        # Check if the output file was created
        if os.path.exists(output_filename):
            print(f"Successfully analyzed {repo} and saved results to {output_filename}")
            return output_filename
        else:
            print(f"Warning: Output file {output_filename} was not created")
            return None
    
    except subprocess.CalledProcessError as e:
        print(f"Error analyzing repository {repo}:")
        print(f"Exit code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return None
    
    except Exception as e:
        print(f"Unexpected error analyzing repository {repo}: {e}")
        return None


def main():
    """Main function to run the script."""
    args = parse_arguments()
    
    # Set up API headers
    headers = get_github_api_headers(args.token)
    
    # Get trending Java projects
    trending_repos = get_trending_java_projects(headers)
    
    print(f"\nFound {len(trending_repos)} trending Java projects:")
    for i, repo in enumerate(trending_repos, 1):
        print(f"{i}. {repo}")
    
    # Analyze each repository
    successful_analyses = 0
    output_files = []
    
    for repo in trending_repos:
        output_file = analyze_repository(repo, args.token, args.limit)
        
        if output_file:
            successful_analyses += 1
            output_files.append(output_file)
    
    # Print summary
    print("\nAnalysis Summary:")
    print(f"Total repositories analyzed: {len(trending_repos)}")
    print(f"Successful analyses: {successful_analyses}")
    print(f"Failed analyses: {len(trending_repos) - successful_analyses}")
    
    if output_files:
        print("\nOutput files created:")
        for file in output_files:
            print(f"- {file}")
    else:
        print("\nNo output files were created.")


if __name__ == "__main__":
    main()
