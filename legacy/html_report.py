#!/usr/bin/env python3
"""
HTML Report Example for GitHub PR Analyzer

This script demonstrates how to modify the GitHub PR Analyzer to output results in HTML format.
This is useful for creating visually appealing and interactive reports of PR analysis results.
"""

import argparse
import datetime
import os
import requests
import sys
from dateutil import parser as date_parser


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Find GitHub PRs with 2+ file changes merged after Nov 2024 (HTML output)')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path for HTML results (optional, defaults to pr_report.html)',
                        default='pr_report.html')
    parser.add_argument('--title', help='Title for the HTML report (optional)',
                        default='GitHub PR Analysis Report')
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


def generate_html_report(repo, filtered_prs, title):
    """Generate HTML report from filtered PRs."""
    owner, repo_name = repo.split('/')
    
    # Get current date and time for the report
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Start building HTML content
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3 {{
            color: #0366d6;
        }}
        .header {{
            border-bottom: 2px solid #0366d6;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .summary {{
            background-color: #f6f8fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .pr-card {{
            border: 1px solid #e1e4e8;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }}
        .pr-card:hover {{
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }}
        .pr-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .pr-meta {{
            color: #586069;
            font-size: 14px;
        }}
        .pr-link {{
            display: inline-block;
            margin-top: 10px;
            color: #0366d6;
            text-decoration: none;
        }}
        .pr-link:hover {{
            text-decoration: underline;
        }}
        .search-box {{
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #e1e4e8;
            border-radius: 5px;
            font-size: 16px;
        }}
        .filters {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        .filter-button {{
            background-color: #0366d6;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
        }}
        .filter-button:hover {{
            background-color: #0255b3;
        }}
        .footer {{
            margin-top: 30px;
            border-top: 1px solid #e1e4e8;
            padding-top: 15px;
            color: #586069;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Repository: <a href="https://github.com/{owner}/{repo_name}" target="_blank">{owner}/{repo_name}</a></p>
        <p>Generated on: {now}</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <p>Found <strong>{len(filtered_prs)}</strong> pull requests with 2+ file changes merged after November 2024.</p>
    </div>
    
    <input type="text" class="search-box" id="searchBox" placeholder="Search PRs by title, author, etc.">
    
    <div class="filters">
        <button class="filter-button" onclick="sortByDate()">Sort by Date</button>
        <button class="filter-button" onclick="sortByFiles()">Sort by Files Changed</button>
        <button class="filter-button" onclick="sortByAuthor()">Sort by Author</button>
    </div>
    
    <div id="pr-list">
"""
    
    # Add PR cards
    for pr in filtered_prs:
        merged_at = pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')
        html += f"""
        <div class="pr-card" data-author="{pr['author'].lower()}" data-files="{pr['files_changed']}" data-date="{pr['merged_at'].isoformat()}">
            <div class="pr-title">PR #{pr['number']}: {pr['title']}</div>
            <div class="pr-meta">
                <p>Author: {pr['author']}</p>
                <p>Merged: {merged_at}</p>
                <p>Files changed: {pr['files_changed']}</p>
            </div>
            <a href="{pr['url']}" class="pr-link" target="_blank">View on GitHub</a>
        </div>
"""
    
    # Add JavaScript for search and sorting
    html += """
    </div>
    
    <div class="footer">
        <p>Generated by GitHub PR Analyzer</p>
    </div>
    
    <script>
        // Search functionality
        document.getElementById('searchBox').addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            const prCards = document.querySelectorAll('.pr-card');
            
            prCards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
        
        // Sorting functions
        function sortByDate() {
            sortCards('date', true);
        }
        
        function sortByFiles() {
            sortCards('files', true);
        }
        
        function sortByAuthor() {
            sortCards('author', false);
        }
        
        function sortCards(attribute, isNumeric) {
            const prList = document.getElementById('pr-list');
            const prCards = Array.from(document.querySelectorAll('.pr-card'));
            
            prCards.sort((a, b) => {
                let aValue = a.getAttribute('data-' + attribute);
                let bValue = b.getAttribute('data-' + attribute);
                
                if (isNumeric) {
                    return bValue.localeCompare(aValue); // Descending order
                } else {
                    return aValue.localeCompare(bValue); // Ascending order for text
                }
            });
            
            // Clear and re-append sorted cards
            prList.innerHTML = '';
            prCards.forEach(card => prList.appendChild(card));
        }
    </script>
</body>
</html>
"""
    
    return html


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
        
        # Check if PR has 2 or more file changes
        if len(files) >= 2:
            filtered_prs.append({
                'number': pr_number,
                'title': pr['title'],
                'merged_at': merged_at,
                'url': pr['html_url'],
                'files_changed': len(files),
                'author': pr['user']['login']
            })
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    # Generate HTML report
    html_content = generate_html_report(args.repo, filtered_prs, args.title)
    
    # Write HTML report to file
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"\nHTML report successfully generated: {args.output}")
    print(f"Found {len(filtered_prs)} PRs with 2+ file changes merged after November 2024.")
    
    # Try to open the HTML report in the default browser
    try:
        print("\nAttempting to open the HTML report in your default browser...")
        if sys.platform == 'win32':
            os.system(f'start {args.output}')
        elif sys.platform == 'darwin':  # macOS
            os.system(f'open {args.output}')
        else:  # Linux
            os.system(f'xdg-open {args.output}')
    except Exception as e:
        print(f"Could not open the HTML report automatically: {e}")
        print(f"Please open {args.output} manually in your browser.")


if __name__ == "__main__":
    main()
