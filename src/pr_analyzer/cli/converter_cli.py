"""Command-line interface for SWE-bench converter."""

import argparse
import sys
from datetime import datetime

from pr_analyzer.gitlab import GitLabAnalyzer, GitLabAPIClient
from pr_analyzer.converters import SWEBenchConverter
from pr_analyzer.utils import save_json


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert GitLab MR results to SWE-bench format'
    )
    parser.add_argument('--input', help='Input file with MR results (text format)')
    parser.add_argument('--output', default='swebench_format.json',
                       help='Output JSON file (default: swebench_format.json)')
    parser.add_argument('--token', required=True,
                       help='GitLab personal access token (required)')
    parser.add_argument('--gitlab-url', default='https://gitlab.com',
                       help='GitLab instance URL (default: https://gitlab.com)')
    parser.add_argument('--project', help='GitLab project ID or path (required if not using --input)')
    parser.add_argument('--limit', type=int, default=20,
                       help='Number of MRs to convert (default: 20)')
    
    return parser.parse_args()


def main():
    """Main entry point for SWE-bench converter CLI."""
    args = parse_arguments()
    
    # Create GitLab API client
    gitlab_client = GitLabAPIClient(token=args.token, base_url=args.gitlab_url)
    
    try:
        if args.input:
            # Parse MRs from input file
            print(f"Reading MR results from: {args.input}")
            from pr_analyzer.converters.swebench import SWEBenchConverter
            mr_data_list = SWEBenchConverter.parse_mr_results_file(args.input)
            
            # Extract project from first MR URL
            if mr_data_list and 'url' in mr_data_list[0]:
                url = mr_data_list[0]['url']
                # Extract project path from URL
                # Example: https://gitlab.com/mycomplianceoffice/mco/-/merge_requests/123
                parts = url.split('/-/merge_requests/')[0].split('/')
                project = '/'.join(parts[-2:])
            elif args.project:
                project = args.project
            else:
                print("Error: Could not determine project. Please provide --project argument.")
                sys.exit(1)
            
            print(f"Project: {project}")
            print(f"Found {len(mr_data_list)} MRs in input file")
            
            # Fetch full MR details
            analyzer = GitLabAnalyzer(token=args.token, base_url=args.gitlab_url)
            mrs = []
            
            for mr_data in mr_data_list[:args.limit]:
                print(f"Fetching details for MR !{mr_data['iid']}...")
                try:
                    mr_details = gitlab_client.get_merge_request(project, mr_data['iid'])
                    changes = gitlab_client.get_merge_request_changes(project, mr_data['iid'])
                    
                    # Convert to MergeRequest object
                    from pr_analyzer.core.models import MergeRequest, Author, FileChange
                    from dateutil import parser as date_parser
                    
                    author = Author(
                        username=mr_details['author']['username'],
                        name=mr_details['author'].get('name'),
                        email=mr_details['author'].get('email')
                    )
                    
                    file_changes = []
                    for change in changes.get('changes', []):
                        filepath = change.get('new_path') or change.get('old_path', '')
                        is_test, is_source = analyzer.classify_file(filepath)
                        
                        file_changes.append(FileChange(
                            path=filepath,
                            old_path=change.get('old_path'),
                            diff=change.get('diff', ''),
                            is_test=is_test,
                            is_source=is_source
                        ))
                    
                    mr = MergeRequest(
                        iid=mr_details['iid'],
                        title=mr_details['title'],
                        description=mr_details.get('description', ''),
                        author=author,
                        merged_at=date_parser.parse(mr_details['merged_at']),
                        created_at=date_parser.parse(mr_details['created_at']),
                        url=mr_details['web_url'],
                        source_branch=mr_details['source_branch'],
                        target_branch=mr_details['target_branch'],
                        files_changed=file_changes,
                        base_commit=mr_details.get('diff_refs', {}).get('base_sha', ''),
                        head_commit=mr_details.get('diff_refs', {}).get('head_sha', ''),
                        labels=mr_details.get('labels', [])
                    )
                    
                    mrs.append(mr)
                    
                except Exception as e:
                    print(f"Warning: Could not fetch MR !{mr_data['iid']}: {e}")
                    continue
        
        elif args.project:
            # Fetch MRs directly from GitLab
            print(f"Fetching MRs from project: {args.project}")
            analyzer = GitLabAnalyzer(token=args.token, base_url=args.gitlab_url)
            
            mrs = analyzer.analyze(
                project=args.project,
                limit=args.limit,
                min_files=2,
                max_files=4,
                require_tests=True,
                require_source=True
            )
            
            project = args.project
            print(f"Found {len(mrs)} matching MRs")
        
        else:
            print("Error: Either --input or --project must be provided")
            sys.exit(1)
        
        # Convert to SWE-bench format
        print(f"\nConverting {len(mrs)} MRs to SWE-bench format...")
        converter = SWEBenchConverter(gitlab_client, project)
        swebench_data = converter.convert_mrs(mrs)
        
        # Save results
        save_json(swebench_data, args.output)
        print(f"\nSuccessfully converted {len(swebench_data)} MRs")
        print(f"Results saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
