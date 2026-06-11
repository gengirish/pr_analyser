"""pr_analyzer: shared library for analyzing GitHub PRs and GitLab MRs.

The top-level scripts in this repository (github_pr_analyzer.py, the *_filter.py
examples, gitlab_mr_analyzer.py, etc.) are thin entry points that wire command
line arguments to the reusable building blocks in this package:

    common/     provider-agnostic helpers (file classification, dates, output, CLI)
    github/     GitHub REST API client + analysis helpers
    gitlab/     GitLab REST API client
    formatters/ CSV / HTML report writers
"""

__version__ = "0.2.0"
