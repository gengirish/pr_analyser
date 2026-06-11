"""GitLab merge request analyzer."""

from datetime import datetime
from dateutil import parser as date_parser
from typing import List, Optional, Dict, Any

from pr_analyzer.core.analyzer import BaseAnalyzer
from pr_analyzer.core.models import MergeRequest, FileChange, Author
from pr_analyzer.gitlab.api import GitLabAPIClient


class GitLabAnalyzer(BaseAnalyzer):
    """Analyzer for GitLab merge requests."""
    
    def __init__(self, token: Optional[str] = None, base_url: str = "https://gitlab.com"):
        """
        Initialize GitLab analyzer.
        
        Args:
            token: GitLab personal access token
            base_url: GitLab instance URL
        """
        self.api_client = GitLabAPIClient(token, base_url)
        super().__init__(token, base_url)
    
    def _create_headers(self) -> Dict[str, str]:
        """Create API request headers."""
        return self.api_client._headers
    
    def fetch_merged_items(
        self,
        project: str,
        since_date: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[MergeRequest]:
        """
        Fetch merged MRs from GitLab.
        
        Args:
            project: Project ID or path
            since_date: Only fetch MRs merged after this date
            limit: Maximum number of MRs to fetch
            
        Returns:
            List of MergeRequest objects
        """
        # Fetch raw MR data from API
        raw_mrs = self.api_client.get_merge_requests(
            project=project,
            state='merged',
            since_date=since_date
        )
        
        # Convert to MergeRequest objects
        merge_requests = []
        
        for raw_mr in raw_mrs:
            # Skip if not merged
            if not raw_mr.get('merged_at'):
                continue
            
            # Parse dates
            merged_at = date_parser.parse(raw_mr['merged_at'])
            created_at = date_parser.parse(raw_mr['created_at'])
            
            # Skip if merged before since_date
            if since_date and merged_at <= since_date:
                continue
            
            # Get file changes
            try:
                changes_data = self.api_client.get_merge_request_changes(
                    project=project,
                    mr_iid=raw_mr['iid']
                )
                file_changes = self._parse_file_changes(changes_data.get('changes', []))
            except Exception as e:
                print(f"Warning: Could not fetch changes for MR !{raw_mr['iid']}: {e}")
                continue
            
            # Create Author object
            author = Author(
                username=raw_mr['author']['username'],
                name=raw_mr['author'].get('name'),
                email=raw_mr['author'].get('email')
            )
            
            # Create MergeRequest object
            mr = MergeRequest(
                iid=raw_mr['iid'],
                title=raw_mr['title'],
                description=raw_mr.get('description', ''),
                author=author,
                merged_at=merged_at,
                created_at=created_at,
                url=raw_mr['web_url'],
                source_branch=raw_mr['source_branch'],
                target_branch=raw_mr['target_branch'],
                files_changed=file_changes,
                base_commit=raw_mr.get('diff_refs', {}).get('base_sha', ''),
                head_commit=raw_mr.get('diff_refs', {}).get('head_sha', ''),
                labels=raw_mr.get('labels', [])
            )
            
            merge_requests.append(mr)
            
            # Apply limit if specified
            if limit and len(merge_requests) >= limit:
                break
        
        return merge_requests
    
    def get_item_changes(self, project: str, item_id: str) -> List[FileChange]:
        """
        Get file changes for a specific MR.
        
        Args:
            project: Project ID or path
            item_id: MR IID
            
        Returns:
            List of FileChange objects
        """
        changes_data = self.api_client.get_merge_request_changes(
            project=project,
            mr_iid=int(item_id)
        )
        
        return self._parse_file_changes(changes_data.get('changes', []))
    
    def _parse_file_changes(self, changes: List[Dict]) -> List[FileChange]:
        """
        Parse raw change data into FileChange objects.
        
        Args:
            changes: List of change dictionaries from API
            
        Returns:
            List of FileChange objects
        """
        file_changes = []
        
        for change in changes:
            filepath = change.get('new_path') or change.get('old_path', '')
            old_path = change.get('old_path')
            
            # Classify file
            is_test, is_source = self.classify_file(filepath)
            
            file_change = FileChange(
                path=filepath,
                old_path=old_path if old_path != filepath else None,
                diff=change.get('diff', ''),
                is_test=is_test,
                is_source=is_source
            )
            
            file_changes.append(file_change)
        
        return file_changes
