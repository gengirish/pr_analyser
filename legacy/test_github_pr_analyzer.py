#!/usr/bin/env python3
"""
Test script for GitHub PR Analyzer

This script tests the GitHub PR Analyzer by mocking GitHub API responses.
It doesn't make actual API calls, so it can be used without a GitHub token
and without hitting API rate limits.

Tests the functionality to ensure PRs have both source code files and test files.
"""

import datetime
import json
import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys

# Import the main script
import github_pr_analyzer


class MockResponse:
    """Mock response object for requests."""
    def __init__(self, json_data, status_code=200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestGitHubPRAnalyzer(unittest.TestCase):
    """Test cases for GitHub PR Analyzer."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample PR data
        self.sample_prs = [
            # PR with 3 files, merged in December 2024 (should be included)
            {
                "number": 101,
                "title": "Feature: Add new component",
                "merged_at": "2024-12-15T10:30:00Z",
                "html_url": "https://github.com/test/repo/pull/101",
                "user": {"login": "user1"}
            },
            # PR with 1 file, merged in December 2024 (should be excluded - too few files)
            {
                "number": 102,
                "title": "Fix: Update README",
                "merged_at": "2024-12-20T14:45:00Z",
                "html_url": "https://github.com/test/repo/pull/102",
                "user": {"login": "user2"}
            },
            # PR with 5 files, merged in October 2024 (should be excluded - too early)
            {
                "number": 103,
                "title": "Feature: Refactor API",
                "merged_at": "2024-10-05T09:15:00Z",
                "html_url": "https://github.com/test/repo/pull/103",
                "user": {"login": "user3"}
            },
            # PR with 2 files, merged in November 2024 (should be included - edge case)
            {
                "number": 104,
                "title": "Fix: Update dependencies",
                "merged_at": "2024-11-02T16:20:00Z",
                "html_url": "https://github.com/test/repo/pull/104",
                "user": {"login": "user4"}
            },
            # PR not merged (should be excluded)
            {
                "number": 105,
                "title": "WIP: New feature",
                "merged_at": None,
                "html_url": "https://github.com/test/repo/pull/105",
                "user": {"login": "user5"}
            }
        ]

        # Sample PR files data
        self.pr_files = {
            101: [{"filename": "src/component.js"}, {"filename": "src/utils.js"}, {"filename": "tests/component.test.js"}],
            102: [{"filename": "README.md"}],
            103: [{"filename": "src/api.js"}, {"filename": "tests/api.test.js"}, {"filename": "src/models/user.js"}, 
                  {"filename": "src/controllers/user.js"}, {"filename": "src/routes/user.js"}],
            104: [{"filename": "package.json"}, {"filename": "package-lock.json"}],
            105: [{"filename": "src/feature.js"}, {"filename": "tests/feature.test.js"}]
        }

    def mock_get_pull_requests(self, *args, **kwargs):
        """Mock the get_pull_requests function."""
        return self.sample_prs

    def mock_get_pr_files(self, owner, repo, pr_number, headers):
        """Mock the get_pr_files function."""
        return self.pr_files.get(pr_number, [])

    @patch('sys.stdout', new_callable=StringIO)
    @patch('github_pr_analyzer.get_pull_requests')
    @patch('github_pr_analyzer.get_pr_files')
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_function(self, mock_args, mock_get_pr_files, mock_get_prs, mock_stdout):
        """Test the main function with mock data."""
        # Mock command line arguments
        mock_args.return_value = MagicMock(repo='test/repo', token=None, limit=20, output=None)
        
        # Mock API functions
        mock_get_prs.side_effect = self.mock_get_pull_requests
        mock_get_pr_files.side_effect = self.mock_get_pr_files
        
        # Run the main function
        github_pr_analyzer.main()
        
        # Get the output
        output = mock_stdout.getvalue()
        
        # Check that the correct PRs were identified
        self.assertIn("Found 1 PRs with 2-4 file changes that include both source code files and test classes, merged after November 2024", output)
        self.assertIn("PR #101: Feature: Add new component", output)
        self.assertNotIn("PR #104: Fix: Update dependencies", output)
        
        # Check that excluded PRs are not in the output
        self.assertNotIn("PR #102: Fix: Update README", output)  # Too few files
        self.assertNotIn("PR #103: Feature: Refactor API", output)  # Too early date
        self.assertNotIn("PR #104: Fix: Update dependencies", output)  # No source code and test files
        self.assertNotIn("PR #105: WIP: New feature", output)  # Not merged


if __name__ == '__main__':
    unittest.main()
