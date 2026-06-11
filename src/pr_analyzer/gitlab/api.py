"""GitLab API client for fetching merge request data."""

import urllib.parse
from datetime import datetime
from typing import Dict, List, Optional
import requests


class GitLabAPIClient:
    """Client for interacting with GitLab API."""
    
    def __init__(self, token: Optional[str] = None, base_url: str = "https://gitlab.com"):
        """
        Initialize GitLab API client.
        
        Args:
            token: GitLab personal access token
            base_url: GitLab instance URL
        """
        self.token = token
        self.base_url = base_url.rstrip('/')
        self._headers = self._create_headers()
    
    def _create_headers(self) -> Dict[str, str]:
        """Create headers for API requests."""
        headers = {'Content-Type': 'application/json'}
        if self.token:
            headers['PRIVATE-TOKEN'] = self.token
        return headers
    
    @staticmethod
    def encode_project_path(project: str) -> str:
        """
        Encode project path for GitLab API.
        
        Args:
            project: Project ID or path
            
        Returns:
            Encoded project identifier
        """
        # If it's already a number (project ID), return as is
        try:
            int(project)
            return project
        except ValueError:
            # URL-encode the project path
            return urllib.parse.quote(project, safe='')
    
    def get_merge_requests(
        self,
        project: str,
        state: str = 'merged',
        since_date: Optional[datetime] = None,
        per_page: int = 100
    ) -> List[Dict]:
        """
        Fetch merge requests from a GitLab project.
        
        Args:
            project: Project ID or path
            state: MR state (merged, opened, closed, all)
            since_date: Only fetch MRs updated after this date
            per_page: Number of results per page
            
        Returns:
            List of merge request dictionaries
        """
        project_id = self.encode_project_path(project)
        all_mrs = []
        page = 1
        
        while True:
            url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests'
            params = {
                'state': state,
                'per_page': per_page,
                'page': page,
                'order_by': 'updated_at',
                'sort': 'desc'
            }
            
            if since_date:
                params['updated_after'] = since_date.isoformat()
            
            response = requests.get(url, headers=self._headers, params=params)
            
            if response.status_code != 200:
                self._handle_error(response)
            
            mrs = response.json()
            if not mrs:
                break
            
            all_mrs.extend(mrs)
            page += 1
            
            # Check if we've reached the last page
            if len(mrs) < per_page:
                break
        
        return all_mrs
    
    def get_merge_request(self, project: str, mr_iid: int) -> Dict:
        """
        Get details of a specific merge request.
        
        Args:
            project: Project ID or path
            mr_iid: Merge request IID
            
        Returns:
            Merge request dictionary
        """
        project_id = self.encode_project_path(project)
        url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}'
        
        response = requests.get(url, headers=self._headers)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        return response.json()
    
    def get_merge_request_changes(self, project: str, mr_iid: int) -> Dict:
        """
        Get file changes for a specific merge request.
        
        Args:
            project: Project ID or path
            mr_iid: Merge request IID
            
        Returns:
            Dictionary containing changes
        """
        project_id = self.encode_project_path(project)
        url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes'
        
        response = requests.get(url, headers=self._headers)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        return response.json()
    
    def get_merge_request_commits(self, project: str, mr_iid: int) -> List[Dict]:
        """
        Get commits for a specific merge request.
        
        Args:
            project: Project ID or path
            mr_iid: Merge request IID
            
        Returns:
            List of commit dictionaries
        """
        project_id = self.encode_project_path(project)
        url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/commits'
        
        response = requests.get(url, headers=self._headers)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        return response.json()
    
    def get_merge_request_discussions(self, project: str, mr_iid: int) -> List[Dict]:
        """
        Get discussions/comments for a specific merge request.
        
        Args:
            project: Project ID or path
            mr_iid: Merge request IID
            
        Returns:
            List of discussion dictionaries
        """
        project_id = self.encode_project_path(project)
        url = f'{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/discussions'
        
        response = requests.get(url, headers=self._headers)
        
        if response.status_code != 200:
            self._handle_error(response)
        
        return response.json()
    
    def _handle_error(self, response: requests.Response):
        """
        Handle API error responses.
        
        Args:
            response: Response object
            
        Raises:
            Exception with appropriate error message
        """
        status_code = response.status_code
        
        if status_code == 404:
            raise Exception("Project not found. Please check the project ID/path and your access permissions.")
        elif status_code == 401:
            raise Exception("Authentication failed. Please check your GitLab token.")
        else:
            try:
                message = response.json().get('message', 'Unknown error')
            except:
                message = response.text
            raise Exception(f"API error ({status_code}): {message}")
