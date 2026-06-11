"""Base analyzer class for PR/MR analysis."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any
from pr_analyzer.core.models import MergeRequest, PullRequest, FileChange


class BaseAnalyzer(ABC):
    """Base class for analyzing pull requests and merge requests."""
    
    def __init__(self, token: Optional[str] = None, base_url: Optional[str] = None):
        """
        Initialize the analyzer.
        
        Args:
            token: API authentication token
            base_url: Base URL for the API
        """
        self.token = token
        self.base_url = base_url
        self._headers = self._create_headers()
    
    @abstractmethod
    def _create_headers(self) -> Dict[str, str]:
        """Create API request headers."""
        pass
    
    @abstractmethod
    def fetch_merged_items(
        self,
        project: str,
        since_date: Optional[datetime] = None,
        limit: Optional[int] = None
    ) -> List[Any]:
        """
        Fetch merged PRs/MRs from the repository.
        
        Args:
            project: Project identifier
            since_date: Only fetch items merged after this date
            limit: Maximum number of items to fetch
            
        Returns:
            List of merged items
        """
        pass
    
    @abstractmethod
    def get_item_changes(self, project: str, item_id: str) -> List[FileChange]:
        """
        Get file changes for a specific PR/MR.
        
        Args:
            project: Project identifier
            item_id: PR/MR identifier
            
        Returns:
            List of file changes
        """
        pass
    
    def classify_file(self, filepath: str) -> tuple[bool, bool]:
        """
        Classify a file as test or source code.
        
        Args:
            filepath: Path to the file
            
        Returns:
            Tuple of (is_test, is_source)
        """
        filepath_lower = filepath.lower()
        
        # Check if it's a test file
        is_test = any(pattern in filepath_lower for pattern in [
            'test', 'spec', '__tests__', 'tests/'
        ])
        
        # Check if it's a source code file
        source_extensions = (
            '.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', 
            '.go', '.rb', '.php', '.ts', '.swift', '.kt', '.scala'
        )
        
        # Exclude documentation and config files
        exclude_patterns = [
            'readme', 'license', 'changelog', 'docs/', 'doc/', 
            'example', '.md', '.txt', '.json', '.yaml', '.yml'
        ]
        
        is_source = (
            filepath_lower.endswith(source_extensions) and
            not any(pattern in filepath_lower for pattern in exclude_patterns)
        )
        
        return is_test, is_source
    
    def filter_by_criteria(
        self,
        items: List[Any],
        min_files: int = 2,
        max_files: int = 4,
        require_tests: bool = True,
        require_source: bool = True
    ) -> List[Any]:
        """
        Filter items by specified criteria.
        
        Args:
            items: List of items to filter
            min_files: Minimum number of file changes
            max_files: Maximum number of file changes
            require_tests: Require test files
            require_source: Require source files
            
        Returns:
            Filtered list of items
        """
        filtered = []
        
        for item in items:
            file_count = len(item.files_changed)
            
            # Check file count
            if not (min_files <= file_count <= max_files):
                continue
            
            # Check for tests and source
            has_tests = item.has_tests
            has_source = item.has_source
            
            if require_tests and not has_tests:
                continue
            
            if require_source and not has_source:
                continue
            
            filtered.append(item)
        
        return filtered
    
    def analyze(
        self,
        project: str,
        since_date: Optional[datetime] = None,
        limit: int = 20,
        min_files: int = 2,
        max_files: int = 4,
        require_tests: bool = True,
        require_source: bool = True
    ) -> List[Any]:
        """
        Analyze a repository and return filtered PRs/MRs.
        
        Args:
            project: Project identifier
            since_date: Only analyze items merged after this date
            limit: Maximum number of matching items to return
            min_files: Minimum number of file changes
            max_files: Maximum number of file changes
            require_tests: Require test files
            require_source: Require source files
            
        Returns:
            List of filtered PRs/MRs
        """
        # Fetch merged items
        items = self.fetch_merged_items(project, since_date)
        
        # Filter by criteria
        filtered = self.filter_by_criteria(
            items,
            min_files=min_files,
            max_files=max_files,
            require_tests=require_tests,
            require_source=require_source
        )
        
        # Apply limit
        return filtered[:limit]
