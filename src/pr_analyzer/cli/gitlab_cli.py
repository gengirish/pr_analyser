"""Command-line interface for GitLab MR analyzer."""

import argparse
import sys
from datetime import datetime, timedelta
from typing import Optional

from pr_analyzer.gitlab import GitLabAnalyzer
from pr_analyzer.utils import save_json, format_mr_output, print_progress, print_summary
from pr_analyzer.utils.files import save_text


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Analyze GitLab merge requests and find suitable candidates for SWE-bench'
    )
    parser.add_argument('project', help='GitLab project ID or path (e.g., mycomplianceoffice/mco)')
    parser.add_argument('--token', help='GitLab personal access token (optional but recommended)')
    parser.add_argument('--output', help='Output file path to save results (optional)')
    parser.add_argument('--limit', type=int, default=20, 
                       help='Maximum number of matching MRs to find (default: 20)')
    parser.add_argument('--gitlab-url', default='https://gitlab.com',
                       help='GitLab instance URL (default: https://gitlab.com)')
    parser.add_argument('--min-files', type=int, default=2,
                       help='Minimum number of files changed (default: 2)')
    parser.add_argument('--max-files', type=int, default=4,
                       help='Maximum number of files changed (default: 4)')
    parser.add_argument('--since-days', type=int, default=365,
                       help='Only analyze MRs from the last N days (default: 365)')
    parser.add_argument('--require-tests', action='store_true', default=True,
                       help='Require test files (default: True)')
    parser.add_argument('--require-source', action='store_true', default=True,
                       help='Require source files (default: True)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    
    return parser.parse_args()


def main():
    """Main entry point for GitLab MR analyzer CLI."""
    args = parse_arguments()
    
    # Calculate since_date with timezone awareness
    from datetime import timezone
    since_date = datetime.now(timezone.utc) - timedelta(days=args.since_days)
    
    print(f"Analyzing GitLab project: {args.project}")
    print(f"GitLab URL: {args.gitlab_url}")
    print(f"Looking for MRs since: {since_date.strftime('%Y-%m-%d')}")
    print(f"File count range: {args.min_files}-{args.max_files}")
    print(f"Require tests: {args.require_tests}")
    print(f"Require source: {args.require_source}")
    print(f"Limit: {args.limit}")
    print()
    
    # Create analyzer
    analyzer = GitLabAnalyzer(token=args.token, base_url=args.gitlab_url)
    
    try:
        # Analyze MRs
        print("Fetching and analyzing merge requests...")
        mrs = analyzer.analyze(
            project=args.project,
            since_date=since_date,
            limit=args.limit,
            min_files=args.min_files,
            max_files=args.max_files,
            require_tests=args.require_tests,
            require_source=args.require_source
        )
        
        # Print summary
        print_summary(mrs, "matching MRs")
        
        # Format output
        if args.format == 'json':
            output = [
                {
                    'iid': mr.iid,
                    'title': mr.title,
                    'author': mr.author.username,
                    'merged_at': mr.merged_at.isoformat(),
                    'url': mr.url,
                    'files_changed': mr.file_count,
                    'source_files': [f.path for f in mr.source_files],
                    'test_files': [f.path for f in mr.test_files]
                }
                for mr in mrs
            ]
            
            if args.output:
                save_json(output, args.output)
                print(f"Results saved to: {args.output}")
            else:
                import json
                print(json.dumps(output, indent=2))
        else:
            # Text format
            output_lines = []
            for mr in mrs:
                output_lines.append(format_mr_output(mr))
            
            output_text = '\n'.join(output_lines)
            
            if args.output:
                save_text(output_text, args.output)
                print(f"Results saved to: {args.output}")
            else:
                print(output_text)
        
        print(f"\nNote: Found {len(mrs)} MRs matching the criteria")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
