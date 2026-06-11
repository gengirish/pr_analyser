"""Filtering logic for PR/MR analysis."""

from datetime import datetime
from typing import List, Optional, Callable
from pr_analyzer.core.models import MergeRequest, PullRequest, FileChange


class BaseFilter:
    """Base class for filters."""
    
    def apply(self, items: List) -> List:
        """Apply the filter to a list of items."""
        raise NotImplementedError


class DateFilter(BaseFilter):
    """Filter items by date."""
    
    def __init__(self, since_date: Optional[datetime] = None, until_date: Optional[datetime] = None):
        self.since_date = since_date
        self.until_date = until_date
    
    def apply(self, items: List) -> List:
        """Filter items by date range."""
        filtered = items
        
        if self.since_date:
            filtered = [item for item in filtered if item.merged_at >= self.since_date]
        
        if self.until_date:
            filtered = [item for item in filtered if item.merged_at <= self.until_date]
        
        return filtered


class FileCountFilter(BaseFilter):
    """Filter items by number of file changes."""
    
    def __init__(self, min_files: int = 2, max_files: int = 4):
        self.min_files = min_files
        self.max_files = max_files
    
    def apply(self, items: List) -> List:
        """Filter items by file count."""
        return [
            item for item in items
            if self.min_files <= item.file_count <= self.max_files
        ]


class TestRequirementFilter(BaseFilter):
    """Filter items that require test files."""
    
    def __init__(self, require_tests: bool = True):
        self.require_tests = require_tests
    
    def apply(self, items: List) -> List:
        """Filter items by test requirement."""
        if not self.require_tests:
            return items
        
        return [item for item in items if item.has_tests]


class SourceRequirementFilter(BaseFilter):
    """Filter items that require source files."""
    
    def __init__(self, require_source: bool = True):
        self.require_source = require_source
    
    def apply(self, items: List) -> List:
        """Filter items by source requirement."""
        if not self.require_source:
            return items
        
        return [item for item in items if item.has_source]


class AuthorFilter(BaseFilter):
    """Filter items by author."""
    
    def __init__(self, authors: List[str]):
        self.authors = [a.lower() for a in authors]
    
    def apply(self, items: List) -> List:
        """Filter items by author."""
        return [
            item for item in items
            if item.author.username.lower() in self.authors
        ]


class LabelFilter(BaseFilter):
    """Filter items by labels."""
    
    def __init__(self, labels: List[str], match_all: bool = False):
        self.labels = [l.lower() for l in labels]
        self.match_all = match_all
    
    def apply(self, items: List) -> List:
        """Filter items by labels."""
        filtered = []
        
        for item in items:
            item_labels = [l.lower() for l in item.labels]
            
            if self.match_all:
                # All specified labels must be present
                if all(label in item_labels for label in self.labels):
                    filtered.append(item)
            else:
                # At least one specified label must be present
                if any(label in item_labels for label in self.labels):
                    filtered.append(item)
        
        return filtered


class FileTypeFilter(BaseFilter):
    """Filter items by file types."""
    
    def __init__(self, extensions: List[str]):
        self.extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}' 
                          for ext in extensions]
    
    def apply(self, items: List) -> List:
        """Filter items by file extensions."""
        filtered = []
        
        for item in items:
            has_matching_file = any(
                any(change.path.lower().endswith(ext) for ext in self.extensions)
                for change in item.files_changed
            )
            
            if has_matching_file:
                filtered.append(item)
        
        return filtered


class DirectoryFilter(BaseFilter):
    """Filter items by directory paths."""
    
    def __init__(self, directories: List[str]):
        self.directories = [d.lower() for d in directories]
    
    def apply(self, items: List) -> List:
        """Filter items by directory paths."""
        filtered = []
        
        for item in items:
            has_matching_dir = any(
                any(dir_path in change.path.lower() for dir_path in self.directories)
                for change in item.files_changed
            )
            
            if has_matching_dir:
                filtered.append(item)
        
        return filtered


class FilterChain:
    """Chain multiple filters together."""
    
    def __init__(self, filters: Optional[List[BaseFilter]] = None):
        self.filters = filters or []
    
    def add_filter(self, filter_obj: BaseFilter):
        """Add a filter to the chain."""
        self.filters.append(filter_obj)
    
    def apply(self, items: List) -> List:
        """Apply all filters in sequence."""
        result = items
        
        for filter_obj in self.filters:
            result = filter_obj.apply(result)
        
        return result


# Convenience aliases
MRFilter = FilterChain
PRFilter = FilterChain
