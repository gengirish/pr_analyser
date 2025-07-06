#!/usr/bin/env python3
"""
PR Review Analyzer Example for GitHub PR Analyzer

This script demonstrates how to analyze PR review comments for GitHub pull requests.
In this example, we'll find PRs with 2+ file changes merged after November 2024 and
analyze their review comments to provide insights into the review process.
"""

import argparse
import datetime
import requests
import sys
from dateutil import parser as date_parser
from collections import Counter


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Analyze PR review comments for GitHub pull requests')
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')
    parser.add_argument('--token', help='GitHub personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path for results (optional)')
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


def get_pr_reviews(owner, repo, pr_number, headers):
    """Get reviews for a specific PR."""
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR reviews: {response.status_code}")
        return []
        
    return response.json()


def get_pr_review_comments(owner, repo, pr_number, headers):
    """Get review comments for a specific PR."""
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/comments'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error fetching PR review comments: {response.status_code}")
        return []
        
    return response.json()


def analyze_review_comments(comments):
    """Analyze review comments to extract insights."""
    # Count comments by user
    users = Counter([comment['user']['login'] for comment in comments])
    
    # Analyze comment length
    comment_lengths = [len(comment['body']) for comment in comments]
    avg_comment_length = sum(comment_lengths) / len(comment_lengths) if comment_lengths else 0
    
    # Analyze comment sentiment (simple keyword-based approach)
    positive_keywords = ['good', 'great', 'nice', 'well done', 'excellent', 'awesome', 'perfect', 'thanks']
    negative_keywords = ['bad', 'wrong', 'incorrect', 'error', 'issue', 'problem', 'fix', 'bug']
    
    positive_count = 0
    negative_count = 0
    
    for comment in comments:
        body = comment['body'].lower()
        for keyword in positive_keywords:
            if keyword in body:
                positive_count += 1
                break
        
        for keyword in negative_keywords:
            if keyword in body:
                negative_count += 1
                break
    
    # Extract common feedback themes (simple keyword-based approach)
    code_style = 0
    performance = 0
    security = 0
    documentation = 0
    
    for comment in comments:
        body = comment['body'].lower()
        if any(kw in body for kw in ['style', 'format', 'indent', 'spacing', 'naming']):
            code_style += 1
        if any(kw in body for kw in ['performance', 'slow', 'fast', 'optimize', 'efficient']):
            performance += 1
        if any(kw in body for kw in ['security', 'vulnerability', 'secure', 'auth', 'permission']):
            security += 1
        if any(kw in body for kw in ['doc', 'comment', 'documentation', 'explain']):
            documentation += 1
    
    return {
        'total_comments': len(comments),
        'users': dict(users.most_common()),
        'avg_comment_length': avg_comment_length,
        'sentiment': {
            'positive': positive_count,
            'negative': negative_count
        },
        'themes': {
            'code_style': code_style,
            'performance': performance,
            'security': security,
            'documentation': documentation
        }
    }


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
    
    print("Analyzing pull requests and their reviews...")
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
        
        # Get PR reviews
        reviews = get_pr_reviews(owner, repo, pr_number, headers)
        
        # Get PR review comments
        comments = get_pr_review_comments(owner, repo, pr_number, headers)
        
        # Analyze review comments
        review_analysis = analyze_review_comments(comments)
        
        # Add PR to filtered list
        filtered_prs.append({
            'number': pr_number,
            'title': pr['title'],
            'merged_at': merged_at,
            'url': pr['html_url'],
            'files_changed': len(files),
            'author': pr['user']['login'],
            'reviews': len(reviews),
            'review_analysis': review_analysis
        })
    
    # Display results
    print("\nResults:")
    print(f"Found {len(filtered_prs)} PRs with 2+ file changes merged after November 2024")
    print("\n" + "-" * 80)
    
    # Sort by merge date (newest first)
    filtered_prs.sort(key=lambda x: x['merged_at'], reverse=True)
    
    # Calculate overall statistics
    total_comments = sum(pr['review_analysis']['total_comments'] for pr in filtered_prs)
    avg_comments_per_pr = total_comments / len(filtered_prs) if filtered_prs else 0
    
    # Combine user statistics
    all_users = Counter()
    for pr in filtered_prs:
        for user, count in pr['review_analysis']['users'].items():
            all_users[user] += count
    
    # Combine sentiment statistics
    total_positive = sum(pr['review_analysis']['sentiment']['positive'] for pr in filtered_prs)
    total_negative = sum(pr['review_analysis']['sentiment']['negative'] for pr in filtered_prs)
    
    # Combine theme statistics
    total_code_style = sum(pr['review_analysis']['themes']['code_style'] for pr in filtered_prs)
    total_performance = sum(pr['review_analysis']['themes']['performance'] for pr in filtered_prs)
    total_security = sum(pr['review_analysis']['themes']['security'] for pr in filtered_prs)
    total_documentation = sum(pr['review_analysis']['themes']['documentation'] for pr in filtered_prs)
    
    # Print overall statistics
    print("Overall Review Statistics:")
    print(f"Total PRs analyzed: {len(filtered_prs)}")
    print(f"Total review comments: {total_comments}")
    print(f"Average comments per PR: {avg_comments_per_pr:.2f}")
    print("\nTop commenters:")
    for user, count in all_users.most_common(5):
        print(f"  {user}: {count} comments")
    
    print("\nSentiment analysis:")
    print(f"  Positive comments: {total_positive}")
    print(f"  Negative comments: {total_negative}")
    
    print("\nCommon feedback themes:")
    print(f"  Code style: {total_code_style}")
    print(f"  Performance: {total_performance}")
    print(f"  Security: {total_security}")
    print(f"  Documentation: {total_documentation}")
    
    print("\n" + "-" * 80)
    
    # Print individual PR statistics
    for pr in filtered_prs:
        print(f"PR #{pr['number']}: {pr['title']}")
        print(f"  Author: {pr['author']}")
        print(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Files changed: {pr['files_changed']}")
        print(f"  Reviews: {pr['reviews']}")
        print(f"  Review comments: {pr['review_analysis']['total_comments']}")
        
        if pr['review_analysis']['total_comments'] > 0:
            print("  Comment statistics:")
            print(f"    Average comment length: {pr['review_analysis']['avg_comment_length']:.2f} characters")
            print(f"    Positive comments: {pr['review_analysis']['sentiment']['positive']}")
            print(f"    Negative comments: {pr['review_analysis']['sentiment']['negative']}")
            
            if pr['review_analysis']['users']:
                print("    Top commenters:")
                for user, count in Counter(pr['review_analysis']['users']).most_common(3):
                    print(f"      {user}: {count} comments")
        
        print(f"  URL: {pr['url']}")
        print("-" * 80)
    
    # Write results to file if output is specified
    if args.output:
        with open(args.output, 'w') as f:
            f.write("GitHub PR Review Analysis\n")
            f.write("=========================\n\n")
            
            f.write(f"Repository: {owner}/{repo}\n")
            f.write(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("Overall Review Statistics:\n")
            f.write(f"Total PRs analyzed: {len(filtered_prs)}\n")
            f.write(f"Total review comments: {total_comments}\n")
            f.write(f"Average comments per PR: {avg_comments_per_pr:.2f}\n\n")
            
            f.write("Top commenters:\n")
            for user, count in all_users.most_common(5):
                f.write(f"  {user}: {count} comments\n")
            
            f.write("\nSentiment analysis:\n")
            f.write(f"  Positive comments: {total_positive}\n")
            f.write(f"  Negative comments: {total_negative}\n")
            
            f.write("\nCommon feedback themes:\n")
            f.write(f"  Code style: {total_code_style}\n")
            f.write(f"  Performance: {total_performance}\n")
            f.write(f"  Security: {total_security}\n")
            f.write(f"  Documentation: {total_documentation}\n\n")
            
            f.write("Individual PR Statistics:\n")
            f.write("------------------------\n\n")
            
            for pr in filtered_prs:
                f.write(f"PR #{pr['number']}: {pr['title']}\n")
                f.write(f"  Author: {pr['author']}\n")
                f.write(f"  Merged: {pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  Files changed: {pr['files_changed']}\n")
                f.write(f"  Reviews: {pr['reviews']}\n")
                f.write(f"  Review comments: {pr['review_analysis']['total_comments']}\n")
                
                if pr['review_analysis']['total_comments'] > 0:
                    f.write("  Comment statistics:\n")
                    f.write(f"    Average comment length: {pr['review_analysis']['avg_comment_length']:.2f} characters\n")
                    f.write(f"    Positive comments: {pr['review_analysis']['sentiment']['positive']}\n")
                    f.write(f"    Negative comments: {pr['review_analysis']['sentiment']['negative']}\n")
                    
                    if pr['review_analysis']['users']:
                        f.write("    Top commenters:\n")
                        for user, count in Counter(pr['review_analysis']['users']).most_common(3):
                            f.write(f"      {user}: {count} comments\n")
                
                f.write(f"  URL: {pr['url']}\n\n")
            
            print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
