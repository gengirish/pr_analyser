"""Thin wrappers over the GitHub REST API.

These functions centralize the request/pagination/error handling that used to
be copy-pasted into every script.
"""

import sys

import requests

API_ROOT = 'https://api.github.com'


def get_headers(token=None):
    """Build request headers, adding token auth when provided."""
    headers = {'Accept': 'application/vnd.github.v3+json'}
    if token:
        headers['Authorization'] = f'token {token}'
    return headers


def get_pull_requests(owner, repo, headers, state='all', since_date=None,
                      exit_on_error=True):
    """Fetch all pull requests for a repo, following pagination.

    Args:
        state: PR state to request ('all', 'closed', 'open').
        since_date: optional datetime; when set, only PRs updated at or after
            this time are returned (GitHub's ``since`` parameter).
        exit_on_error: when True (the default) a non-200 response exits the
            process; when False an empty list is returned so callers analyzing
            multiple repos can continue.
    """
    all_prs = []
    page = 1
    per_page = 100

    while True:
        url = f'{API_ROOT}/repos/{owner}/{repo}/pulls'
        params = {'state': state, 'per_page': per_page, 'page': page}
        if since_date:
            params['since'] = since_date.isoformat()

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching PRs for {owner}/{repo}: {response.status_code}")
            print(response.json().get('message', 'Unknown error'))
            if exit_on_error:
                sys.exit(1)
            return []

        prs = response.json()
        if not prs:
            break

        all_prs.extend(prs)
        page += 1
        if len(prs) < per_page:
            break

    return all_prs


def get_pr_files(owner, repo, pr_number, headers):
    """Return the list of files changed in a PR (empty list on error)."""
    url = f'{API_ROOT}/repos/{owner}/{repo}/pulls/{pr_number}/files'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR files: {response.status_code}")
        return []
    return response.json()


def get_pr_details(owner, repo, pr_number, headers):
    """Return detailed information for a single PR (None on error)."""
    url = f'{API_ROOT}/repos/{owner}/{repo}/pulls/{pr_number}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR details: {response.status_code}")
        return None
    return response.json()


def get_pr_labels(owner, repo, pr_number, headers):
    """Return label names for a PR (uses the issues endpoint)."""
    url = f'{API_ROOT}/repos/{owner}/{repo}/issues/{pr_number}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR labels: {response.status_code}")
        return []
    issue_data = response.json()
    return [label['name'] for label in issue_data.get('labels', [])]


def get_pr_reviews(owner, repo, pr_number, headers):
    """Return the reviews submitted on a PR (empty list on error)."""
    url = f'{API_ROOT}/repos/{owner}/{repo}/pulls/{pr_number}/reviews'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR reviews: {response.status_code}")
        return []
    return response.json()


def get_pr_review_comments(owner, repo, pr_number, headers):
    """Return inline review comments on a PR (empty list on error)."""
    url = f'{API_ROOT}/repos/{owner}/{repo}/pulls/{pr_number}/comments'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching PR review comments: {response.status_code}")
        return []
    return response.json()


def search_repositories(headers, query, sort='stars', order='desc', per_page=10):
    """Search repositories, returning the list of ``full_name`` strings."""
    url = f'{API_ROOT}/search/repositories'
    params = {'q': query, 'sort': sort, 'order': order, 'per_page': per_page}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f"Error fetching trending projects: {response.status_code}")
        print(response.json().get('message', 'Unknown error'))
        sys.exit(1)
    data = response.json()
    return [repo['full_name'] for repo in data.get('items', [])]


def get_authenticated_user(headers):
    """Return the raw ``GET /user`` response (for token validation)."""
    return requests.get(f'{API_ROOT}/user', headers=headers)
