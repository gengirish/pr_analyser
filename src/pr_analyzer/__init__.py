"""
PR/MR Analyzer - A tool for analyzing pull requests and merge requests

This package provides tools to analyze GitHub pull requests and GitLab merge requests,
with support for various output formats including SWE-bench format.
"""

__version__ = "2.0.0"
__author__ = "PR Analyzer Team"

from pr_analyzer.core.analyzer import BaseAnalyzer
from pr_analyzer.gitlab.analyzer import GitLabAnalyzer

__all__ = [
    "BaseAnalyzer",
    "GitLabAnalyzer",
]
