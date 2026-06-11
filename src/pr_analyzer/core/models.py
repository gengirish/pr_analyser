"""Data models for PR/MR analysis."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class FileChange:
    """Represents a file change in a PR/MR."""
    
    path: str
    old_path: Optional[str] = None
    additions: int = 0
    deletions: int = 0
    diff: str = ""
    is_test: bool = False
    is_source: bool = False


@dataclass
class Author:
    """Represents an author of a PR/MR."""
    
    username: str
    name: Optional[str] = None
    email: Optional[str] = None


@dataclass
class MergeRequest:
    """Represents a GitLab merge request."""
    
    iid: int
    title: str
    description: str
    author: Author
    merged_at: datetime
    created_at: datetime
    url: str
    source_branch: str
    target_branch: str
    files_changed: List[FileChange] = field(default_factory=list)
    base_commit: str = ""
    head_commit: str = ""
    labels: List[str] = field(default_factory=list)
    
    @property
    def file_count(self) -> int:
        """Get the number of files changed."""
        return len(self.files_changed)
    
    @property
    def source_files(self) -> List[FileChange]:
        """Get only source code files."""
        return [f for f in self.files_changed if f.is_source]
    
    @property
    def test_files(self) -> List[FileChange]:
        """Get only test files."""
        return [f for f in self.files_changed if f.is_test]
    
    @property
    def has_tests(self) -> bool:
        """Check if MR includes test files."""
        return len(self.test_files) > 0
    
    @property
    def has_source(self) -> bool:
        """Check if MR includes source files."""
        return len(self.source_files) > 0


@dataclass
class PullRequest:
    """Represents a GitHub pull request."""
    
    number: int
    title: str
    description: str
    author: Author
    merged_at: datetime
    created_at: datetime
    url: str
    source_branch: str
    target_branch: str
    files_changed: List[FileChange] = field(default_factory=list)
    base_commit: str = ""
    head_commit: str = ""
    labels: List[str] = field(default_factory=list)
    
    @property
    def file_count(self) -> int:
        """Get the number of files changed."""
        return len(self.files_changed)
    
    @property
    def source_files(self) -> List[FileChange]:
        """Get only source code files."""
        return [f for f in self.files_changed if f.is_source]
    
    @property
    def test_files(self) -> List[FileChange]:
        """Get only test files."""
        return [f for f in self.files_changed if f.is_test]
    
    @property
    def has_tests(self) -> bool:
        """Check if PR includes test files."""
        return len(self.test_files) > 0
    
    @property
    def has_source(self) -> bool:
        """Check if PR includes source files."""
        return len(self.source_files) > 0
