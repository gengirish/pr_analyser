"""Output utility functions."""

from typing import List, Any
from pr_analyzer.core.models import MergeRequest, PullRequest


def print_progress(message: str, current: int = 0, total: int = 0):
    """
    Print progress message.
    
    Args:
        message: Progress message
        current: Current item number
        total: Total items
    """
    if total > 0:
        print(f"{message} ({current}/{total})")
    else:
        print(message)


def print_summary(items: List[Any], item_type: str = "items"):
    """
    Print summary of analyzed items.
    
    Args:
        items: List of items
        item_type: Type of items (e.g., "MRs", "PRs")
    """
    print(f"\n{'='*80}")
    print(f"Summary: Found {len(items)} {item_type}")
    print(f"{'='*80}\n")


def format_mr_output(mr: MergeRequest) -> str:
    """
    Format a merge request for text output.
    
    Args:
        mr: MergeRequest object
        
    Returns:
        Formatted string
    """
    lines = [
        f"MR !{mr.iid}: {mr.title}",
        f"  Author: {mr.author.username}",
        f"  Merged: {mr.merged_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Files changed: {mr.file_count}",
        f"  Source files: {', '.join([f.path for f in mr.source_files])}",
        f"  Test files: {', '.join([f.path for f in mr.test_files])}",
        f"  URL: {mr.url}",
        "-" * 80
    ]
    return "\n".join(lines)


def format_pr_output(pr: PullRequest) -> str:
    """
    Format a pull request for text output.
    
    Args:
        pr: PullRequest object
        
    Returns:
        Formatted string
    """
    lines = [
        f"PR #{pr.number}: {pr.title}",
        f"  Author: {pr.author.username}",
        f"  Merged: {pr.merged_at.strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Files changed: {pr.file_count}",
        f"  Source files: {', '.join([f.path for f in pr.source_files])}",
        f"  Test files: {', '.join([f.path for f in pr.test_files])}",
        f"  URL: {pr.url}",
        "-" * 80
    ]
    return "\n".join(lines)
