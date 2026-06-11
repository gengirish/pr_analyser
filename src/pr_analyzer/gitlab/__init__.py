"""GitLab-specific modules for MR analysis."""

from pr_analyzer.gitlab.api import GitLabAPIClient
from pr_analyzer.gitlab.analyzer import GitLabAnalyzer

__all__ = [
    "GitLabAPIClient",
    "GitLabAnalyzer",
]
