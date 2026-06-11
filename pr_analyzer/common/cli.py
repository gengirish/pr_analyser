"""Small argparse / argument-parsing helpers shared by the scripts."""

import sys


def add_repo_argument(parser):
    """Add the positional ``repo`` argument (owner/repo)."""
    parser.add_argument('repo', help='GitHub repository in the format "owner/repo"')


def add_token_argument(parser):
    """Add the optional ``--token`` argument."""
    parser.add_argument(
        '--token',
        help='GitHub personal access token (optional but recommended)',
    )


def parse_owner_repo(repo):
    """Split 'owner/repo' into (owner, repo), exiting on a bad format."""
    try:
        owner, name = repo.split('/')
    except ValueError:
        print("Error: Repository must be in the format 'owner/repo'")
        sys.exit(1)
    return owner, name


def split_csv(value, lower=True):
    """Split a comma-separated argument into a clean list of tokens."""
    items = [item.strip() for item in value.split(',') if item.strip()]
    if lower:
        items = [item.lower() for item in items]
    return items
