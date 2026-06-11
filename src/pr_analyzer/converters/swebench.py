"""SWE-bench format converter for merge requests."""

import re
from typing import List, Dict, Any
from datetime import datetime

from pr_analyzer.core.models import MergeRequest
from pr_analyzer.gitlab.api import GitLabAPIClient


class SWEBenchConverter:
    """Convert merge requests to SWE-bench format."""
    
    def __init__(self, gitlab_client: GitLabAPIClient, project: str):
        """
        Initialize SWE-bench converter.
        
        Args:
            gitlab_client: GitLab API client
            project: Project ID or path
        """
        self.gitlab_client = gitlab_client
        self.project = project
    
    def convert_mr(self, mr: MergeRequest) -> Dict[str, Any]:
        """
        Convert a single merge request to SWE-bench format.
        
        Args:
            mr: MergeRequest object
            
        Returns:
            Dictionary in SWE-bench format
        """
        # Fetch additional details from API
        try:
            mr_details = self.gitlab_client.get_merge_request(self.project, mr.iid)
            changes = self.gitlab_client.get_merge_request_changes(self.project, mr.iid)
            commits = self.gitlab_client.get_merge_request_commits(self.project, mr.iid)
        except Exception as e:
            print(f"Warning: Could not fetch details for MR !{mr.iid}: {e}")
            return None
        
        # Extract repo name from project path
        repo_parts = self.project.split('/')
        repo = f"{repo_parts[-2]}/{repo_parts[-1]}" if len(repo_parts) >= 2 else self.project
        
        # Create instance ID
        instance_id = f"{repo.replace('/', '__')}-{mr.iid}"
        
        # Get patch content
        patch = self._generate_patch(changes.get('changes', []))
        
        # Get test patch (changes to test files only)
        test_patch = self._generate_test_patch(changes.get('changes', []))
        
        # Build SWE-bench entry
        swebench_entry = {
            "instance_id": instance_id,
            "repo": repo,
            "base_commit": mr.base_commit,
            "patch": patch,
            "test_patch": test_patch,
            "problem_statement": self._format_problem_statement(mr),
            "hints_text": "",
            "created_at": mr.created_at.isoformat(),
            "version": mr.head_commit,
            "FAIL_TO_PASS": self._extract_test_info(mr, "fail_to_pass"),
            "PASS_TO_PASS": self._extract_test_info(mr, "pass_to_pass"),
            "environment_setup_commit": mr.base_commit
        }
        
        return swebench_entry
    
    def convert_mrs(self, mrs: List[MergeRequest]) -> List[Dict[str, Any]]:
        """
        Convert multiple merge requests to SWE-bench format.
        
        Args:
            mrs: List of MergeRequest objects
            
        Returns:
            List of dictionaries in SWE-bench format
        """
        swebench_entries = []
        
        for i, mr in enumerate(mrs, 1):
            print(f"Converting MR !{mr.iid} ({i}/{len(mrs)})...")
            entry = self.convert_mr(mr)
            if entry:
                swebench_entries.append(entry)
        
        return swebench_entries
    
    def _generate_patch(self, changes: List[Dict]) -> str:
        """
        Generate unified diff patch from changes.
        
        Args:
            changes: List of file changes
            
        Returns:
            Unified diff patch string
        """
        patch_lines = []
        
        for change in changes:
            diff = change.get('diff', '')
            if diff:
                patch_lines.append(diff)
        
        return '\n'.join(patch_lines)
    
    def _generate_test_patch(self, changes: List[Dict]) -> str:
        """
        Generate patch for test files only.
        
        Args:
            changes: List of file changes
            
        Returns:
            Unified diff patch string for test files
        """
        patch_lines = []
        
        for change in changes:
            filepath = change.get('new_path') or change.get('old_path', '')
            
            # Check if it's a test file
            if self._is_test_file(filepath):
                diff = change.get('diff', '')
                if diff:
                    patch_lines.append(diff)
        
        return '\n'.join(patch_lines)
    
    def _is_test_file(self, filepath: str) -> bool:
        """Check if a file is a test file."""
        filepath_lower = filepath.lower()
        return any(pattern in filepath_lower for pattern in [
            'test', 'spec', '__tests__', 'tests/'
        ])
    
    def _format_problem_statement(self, mr: MergeRequest) -> str:
        """
        Format the problem statement from MR description.
        
        Args:
            mr: MergeRequest object
            
        Returns:
            Formatted problem statement
        """
        lines = [
            f"# {mr.title}",
            "",
            mr.description or "No description provided.",
            "",
            f"**Author:** {mr.author.username}",
            f"**Merged:** {mr.merged_at.strftime('%Y-%m-%d')}",
            f"**Files Changed:** {mr.file_count}",
        ]
        
        return '\n'.join(lines)
    
    def _extract_test_info(self, mr: MergeRequest, test_type: str) -> List[str]:
        """
        Extract test information from MR.
        
        Args:
            mr: MergeRequest object
            test_type: Type of test info to extract
            
        Returns:
            List of test identifiers
        """
        # This is a placeholder - in a real implementation, you would
        # parse test files to extract actual test names
        test_files = [f.path for f in mr.test_files]
        
        if not test_files:
            return []
        
        # Extract test names from file paths
        test_names = []
        for test_file in test_files:
            # Remove extension and convert to test identifier
            test_name = test_file.replace('/', '.').replace('.py', '')
            test_names.append(test_name)
        
        return test_names[:5]  # Limit to 5 tests
    
    @staticmethod
    def parse_mr_results_file(filepath: str) -> List[Dict[str, Any]]:
        """
        Parse MR results from text file.
        
        Args:
            filepath: Path to results file
            
        Returns:
            List of MR data dictionaries
        """
        mrs = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by separator
        mr_blocks = content.split('-' * 80)
        
        for block in mr_blocks:
            if not block.strip() or 'Results:' in block:
                continue
            
            lines = block.strip().split('\n')
            mr_data = {}
            
            for line in lines:
                line = line.strip()
                if line.startswith('MR !'):
                    match = re.match(r'MR !(\d+): (.+)', line)
                    if match:
                        mr_data['iid'] = int(match.group(1))
                        mr_data['title'] = match.group(2)
                elif line.startswith('Author:'):
                    mr_data['author'] = line.split('Author:')[1].strip()
                elif line.startswith('URL:'):
                    mr_data['url'] = line.split('URL:')[1].strip()
            
            if mr_data and 'iid' in mr_data:
                mrs.append(mr_data)
        
        return mrs
