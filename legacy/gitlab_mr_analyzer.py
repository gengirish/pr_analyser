#!/usr/bin/env python3
"""
GitLab MR Analyzer

This script analyzes a GitLab repository to find merge requests that:
1. Have 2 to 4 file changes
2. Were merged after November 2024
3. Include both source code files and test classes

Usage:
    python gitlab_mr_analyzer.py [--token GITLAB_TOKEN] [--output OUTPUT_FILE] [--limit LIMIT] project_id

Arguments:
    project_id      GitLab project ID or URL-encoded path (e.g., "12345" or "mycomplianceoffice%2Fmco")
    --token         GitLab personal access token (optional but recommended to avoid rate limits)
    --output        Output file path to save results (optional)
    --limit         Maximum number of matching MRs to find (default: 20)
    --gitlab-url    GitLab instance URL (default: https://gitlab.com)

Examples:
    python gitlab_mr_analyzer.py --token glpat-abc123 mycomplianceoffice/mco
    python gitlab_mr_analyzer.py --token glpat-abc123 --output results.txt 12345
    python gitlab_mr_analyzer.py --token glpat-abc123 --limit 10 mycomplianceoffice/mco
"""

import argparse
import datetime
import requests
import sys
import urllib.parse
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Find GitLab MRs with 2-4 file changes that include both source code files and test classes, merged after Nov 2024'
    )
    parser.add_argument('project', help='GitLab project ID or path (e.g., "12345" or "mycomplianceoffice/mco")')
    parser.add_argument('--token', help='GitLab personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path to save results (optional)')
    parser.add_argument('--limit', type=int, default=20, help='Maximum number of matching MRs to find (default: 20)')
    parser.add_argument('--gitlab-url', default='https://gitlab.com', help='GitLab instance URL (default: https://gitlab.com)')
    return parser.parse_args()


def get_gitlab_api_headers(token=None):
    """Create headers for GitLab API requests."""
    headers = {
        'Content-Type': 'application/json',
    }
    if token:
        headers['PRIVATE-TOKEN'] = token
    return headers


def encode_project_path(project):
    """Encode project path for GitLab API."""
    # If it's already a number (project ID), return as is
    try:
        int(project)
        return project
    except ValueError:
        # URL-encode the project path
        return urllib.parse.quote(project, safe='')


def get_merge_requests(gitlab_url, project_id, headers, since_date=None):
    """Fetch all merge requests from a GitLab repository.
    
    Args:
        gitlab_url (str): GitLab instance URL
        project_id (str): Project ID or URL-encoded path
        headers (dict): API request headers
        since_date (datetime, optional): Filter MRs updated at or after this date
    """
    all_mrs = []
    page = 1
    per_page = 100
    
    while True:
        url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests'
        params = {
            'state': 'merged',  # Get only merged MRs
            'per_page': per_page,
            'page': page,
            'order_by': 'updated_at',
            'sort': 'desc'
        }
        
        # Add date filter if provided
        if since_date:
            # Convert datetime to ISO 8601 format for the GitLab API
            params['updated_after'] = since_date.isoformat()
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching MRs: {response.status_code}")
            if response.status_code == 404:
                print("Project not found. Please check the project ID/path and your access permissions.")
            elif response.status_code == 401:
                print("Authentication failed. Please check your GitLab token.")
            else:
                try:
                    print(response.json().get('message', 'Unknown error'))
                except:
                    print(response.text)
            sys.exit(1)
        
        mrs = response.json()
        if not mrs:
            break
            
        all_mrs.extend(mrs)
        page += 1
        
        # Check if we've reached the last page
        if len(mrs) < per_page:
            break
    
    return all_mrs


def get_mr_changes(gitlab_url, project_id, mr_iid, headers):
    """Get files changed in a specific MR."""
    url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching MR changes: {response.status_code}")
        return []
    
    data = response.json()
    return data.get('changes', [])


def main():
    """Main function to run the script."""
    args = parse_arguments()
    
    # Set up output file
    output_file = None
    output_filename = args.output
    
    # If no output file specified, create a default one with timestamp
    if not output_filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"mr_results_{timestamp}.txt"
    
    try:
        output_file = open(output_filename, 'w', encoding='utf-8')
        print(f"Results will be saved to {output_filename}")
    except Exception as e:
        print(f"Error opening output file: {e}")
        print("Results will only be displayed on screen")
    
    # Function to print to both console and file if specified
    def print_output(message):
        print(message)
        if output_file:
            print(message, file=output_file)
    
    # Encode project path for API
    project_id = encode_project_path(args.project)
    
    # Set up API headers
    headers = get_gitlab_api_headers(args.token)
    
    # Target date: November 1, 2024
    target_date = datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc)
    
    # Get merged MRs with date filter applied at the API level
    print(f"Fetching merged merge requests for project '{args.project}' updated after {target_date.strftime('%Y-%m-%d')}...")
    all_mrs = get_merge_requests(args.gitlab_url, project_id, headers, target_date)
    print(f"Found {len(all_mrs)} merge requests in total.")
    
    # Filter and analyze MRs
    filtered_mrs = []
    mr_limit = args.limit
    
    print(f"Analyzing merge requests (limit: {mr_limit} matching MRs)...")
    for mr in all_mrs:
        mr_iid = mr['iid']
        
        # Check merge date
        if not mr.get('merged_at'):
            continue
            
        merged_at = date_parser.parse(mr['merged_at'])
        if merged_at <= target_date:
            continue
        
        # Get files changed in this MR
        changes = get_mr_changes(args.gitlab_url, project_id, mr_iid, headers)
        
        # Check if MR has 2 to 4 file changes
        if 2 <= len(changes) <= 4:
            # Check if any of the files are test files and source code files
            has_test_files = False
            has_source_files = False
            test_files = []
            source_files = []
            
            for change in changes:
                # Get the file path (new_path for added/modified files, old_path for deleted)
                filepath = change.get('new_path') or change.get('old_path', '')
                filename = filepath.lower()
                
                # Check for common test file patterns
                if 'test' in filename or 'spec' in filename:
                    has_test_files = True
                    test_files.append(filepath)
                # Check for source code files (excluding test files, documentation, etc.)
                elif (filename.endswith(('.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rb', '.php', '.ts', '.swift', '.kt', '.scala')) and
                      not any(exclude in filename for exclude in ['readme', 'license', 'changelog', 'docs/', 'doc/', 'example'])):
                    has_source_files = True
                    source_files.append(filepath)
            
            # Only include MRs that have both test files and source code files
            if has_test_files and has_source_files:
                filtered_mrs.append({
                    'iid': mr_iid,
                    'title': mr['title'],
                    'merged_at': merged_at,
                    'url': mr['web_url'],
                    'files_changed': len(changes),
                    'author': mr['author']['username'],
                    'test_files': test_files,
                    'source_files': source_files
                })
                
                # Check if we've reached the limit of matching MRs
                if len(filtered_mrs) >= mr_limit:
                    print(f"Reached limit of {mr_limit} matching MRs. Stopping analysis.")
                    break
    
    # Display results
    print_output("\nResults:")
    print_output(f"Found {len(filtered_mrs)} MRs with 2-4 file changes that include both source code files and test classes, merged after November 2024:")
    print_output("\n" + "-" * 80)
    
    # Check if we need to break out of the main loop
    if len(filtered_mrs) >= mr_limit:
        print_output(f"Note: Analysis stopped after finding {mr_limit} matching MRs.")
    
    # Sort by merge date (newest first)
    filtered_mrs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    for mr in filtered_mrs:
        print_output(f"MR !{mr['iid']}: {mr['title']}")
        print_output(f"  Author: {mr['author']}")
        print_output(f"  Merged: {mr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print_output(f"  Files changed: {mr['files_changed']}")
        print_output(f"  Source files: {', '.join(mr['source_files'])}")
        print_output(f"  Test files: {', '.join(mr['test_files'])}")
        print_output(f"  URL: {mr['url']}")
        print_output("-" * 80)
    
    # Close output file if opened
    if output_file:
        output_file.close()
        print(f"\nResults have been saved to {output_filename}")


if __name__ == "__main__":
    main()
