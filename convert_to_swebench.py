#!/usr/bin/env python3
"""
Convert GitLab MR results to SWE-bench format

This script converts the GitLab MR analyzer output to the SWE-bench_Lite format
used by the princeton-nlp/SWE-bench_Lite dataset.

Usage:
    python convert_to_swebench.py [--input INPUT_FILE] [--output OUTPUT_FILE] [--token GITLAB_TOKEN]

Arguments:
    --input         Input file with MR results (default: mr_results_20260610_131047.txt)
    --output        Output JSON file (default: swebench_format.json)
    --token         GitLab personal access token (required for fetching patches and commits)
    --gitlab-url    GitLab instance URL (default: https://gitlab.com)
"""

import argparse
import json
import re
import requests
import sys
from datetime import datetime


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Convert GitLab MR results to SWE-bench format'
    )
    parser.add_argument('--input', default='mr_results_20260610_131047.txt',
                        help='Input file with MR results')
    parser.add_argument('--output', default='swebench_format.json',
                        help='Output JSON file')
    parser.add_argument('--token', required=True,
                        help='GitLab personal access token (required)')
    parser.add_argument('--gitlab-url', default='https://gitlab.com',
                        help='GitLab instance URL (default: https://gitlab.com)')
    return parser.parse_args()


def get_gitlab_api_headers(token):
    """Create headers for GitLab API requests."""
    return {
        'Content-Type': 'application/json',
        'PRIVATE-TOKEN': token
    }


def parse_mr_results(input_file):
    """Parse the MR results file and extract MR information."""
    mrs = []
    current_mr = {}
    
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by the separator line
    mr_blocks = content.split('--------------------------------------------------------------------------------')
    
    for block in mr_blocks:
        if not block.strip() or 'Results:' in block or 'Note:' in block:
            continue
        
        lines = block.strip().split('\n')
        mr_data = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('MR !'):
                # Extract MR number and title
                match = re.match(r'MR !(\d+): (.+)', line)
                if match:
                    mr_data['iid'] = match.group(1)
                    mr_data['title'] = match.group(2)
            elif line.startswith('Author:'):
                mr_data['author'] = line.split('Author:')[1].strip()
            elif line.startswith('Merged:'):
                mr_data['merged_at'] = line.split('Merged:')[1].strip()
            elif line.startswith('Files changed:'):
                mr_data['files_changed'] = int(line.split('Files changed:')[1].strip())
            elif line.startswith('Source files:'):
                mr_data['source_files'] = [f.strip() for f in line.split('Source files:')[1].split(',')]
            elif line.startswith('Test files:'):
                mr_data['test_files'] = [f.strip() for f in line.split('Test files:')[1].split(',')]
            elif line.startswith('URL:'):
                mr_data['url'] = line.split('URL:')[1].strip()
        
        if mr_data and 'iid' in mr_data:
            mrs.append(mr_data)
    
    return mrs


def get_mr_details(gitlab_url, project_id, mr_iid, headers):
    """Get detailed MR information from GitLab API."""
    url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Warning: Could not fetch MR !{mr_iid} details: {response.status_code}")
        return None
    
    return response.json()


def get_mr_changes(gitlab_url, project_id, mr_iid, headers):
    """Get MR changes (diff) from GitLab API."""
    url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Warning: Could not fetch MR !{mr_iid} changes: {response.status_code}")
        return None
    
    return response.json()


def extract_patch_from_changes(changes):
    """Extract unified diff patch from GitLab changes."""
    if not changes or 'changes' not in changes:
        return ""
    
    patch_lines = []
    for change in changes['changes']:
        if 'diff' in change:
            patch_lines.append(change['diff'])
    
    return '\n'.join(patch_lines)


def separate_test_patch(changes, test_files):
    """Separate test-related changes from source code changes."""
    if not changes or 'changes' not in changes:
        return "", ""
    
    source_patch_lines = []
    test_patch_lines = []
    
    for change in changes['changes']:
        file_path = change.get('new_path') or change.get('old_path', '')
        diff = change.get('diff', '')
        
        # Check if this file is a test file
        is_test = any(test_file in file_path for test_file in test_files)
        
        if is_test:
            test_patch_lines.append(diff)
        else:
            source_patch_lines.append(diff)
    
    return '\n'.join(source_patch_lines), '\n'.join(test_patch_lines)


def convert_to_swebench_format(mrs, gitlab_url, project_id, headers):
    """Convert MR data to SWE-bench format."""
    swebench_data = []
    
    for i, mr in enumerate(mrs):
        print(f"Processing MR !{mr['iid']} ({i+1}/{len(mrs)})...")
        
        # Get detailed MR information
        mr_details = get_mr_details(gitlab_url, project_id, mr['iid'], headers)
        if not mr_details:
            continue
        
        # Get MR changes (diffs)
        mr_changes = get_mr_changes(gitlab_url, project_id, mr['iid'], headers)
        if not mr_changes:
            continue
        
        # Separate source and test patches
        source_patch, test_patch = separate_test_patch(mr_changes, mr.get('test_files', []))
        
        # Create SWE-bench format entry
        instance = {
            'repo': f"mycomplianceoffice/mco",  # Repository identifier
            'instance_id': f"mycomplianceoffice__mco-MR-{mr['iid']}",  # Unique instance ID
            'base_commit': mr_details.get('diff_refs', {}).get('base_sha', ''),  # Base commit before MR
            'patch': source_patch,  # Source code changes (excluding tests)
            'test_patch': test_patch,  # Test file changes
            'problem_statement': f"{mr['title']}\n\n{mr_details.get('description', '')}",  # Issue/MR description
            'hints_text': '',  # Comments/hints (would need additional API calls)
            'created_at': mr_details.get('created_at', ''),  # MR creation date
            'version': '',  # Version info (not available in GitLab MR)
            'FAIL_TO_PASS': '[]',  # Tests that should pass after fix (would need test execution)
            'PASS_TO_PASS': '[]',  # Tests that should continue passing (would need test execution)
            'environment_setup_commit': mr_details.get('diff_refs', {}).get('start_sha', ''),  # Setup commit
        }
        
        swebench_data.append(instance)
    
    return swebench_data


def main():
    """Main function to run the conversion."""
    args = parse_arguments()
    
    print(f"Reading MR results from: {args.input}")
    
    # Parse the input file
    try:
        mrs = parse_mr_results(args.input)
        print(f"Found {len(mrs)} MRs to convert")
    except Exception as e:
        print(f"Error parsing input file: {e}")
        sys.exit(1)
    
    if not mrs:
        print("No MRs found in input file")
        sys.exit(1)
    
    # Set up GitLab API
    headers = get_gitlab_api_headers(args.token)
    project_id = 'mycomplianceoffice%2Fmco'  # URL-encoded project path
    
    # Convert to SWE-bench format
    print("\nFetching detailed MR information from GitLab API...")
    swebench_data = convert_to_swebench_format(mrs, args.gitlab_url, project_id, headers)
    
    # Save to JSON file
    print(f"\nSaving {len(swebench_data)} entries to: {args.output}")
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(swebench_data, f, indent=2, ensure_ascii=False)
        print(f"✓ Successfully saved to {args.output}")
    except Exception as e:
        print(f"Error saving output file: {e}")
        sys.exit(1)
    
    # Print summary
    print("\n" + "="*80)
    print("Conversion Summary:")
    print("="*80)
    print(f"Total MRs processed: {len(swebench_data)}")
    print(f"Output format: SWE-bench_Lite compatible JSON")
    print(f"Output file: {args.output}")
    print("\nSWE-bench format fields included:")
    print("  ✓ repo")
    print("  ✓ instance_id")
    print("  ✓ base_commit")
    print("  ✓ patch (source code changes)")
    print("  ✓ test_patch (test file changes)")
    print("  ✓ problem_statement (MR title + description)")
    print("  ✓ created_at")
    print("  ✓ environment_setup_commit")
    print("\nNote: Some fields (hints_text, FAIL_TO_PASS, PASS_TO_PASS) require")
    print("      additional data that would need test execution or comment analysis.")
    print("="*80)


if __name__ == "__main__":
    main()
