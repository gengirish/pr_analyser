"""Thin wrappers over the GitLab REST API (v4)."""

import sys
import urllib.parse

import requests

DEFAULT_GITLAB_URL = 'https://gitlab.com'


def get_headers(token=None):
    """Build request headers, adding token auth when provided."""
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['PRIVATE-TOKEN'] = token
    return headers


def encode_project_path(project):
    """Return a value usable as ``:id`` in the API.

    Numeric project IDs pass through unchanged; ``owner/repo`` style paths are
    URL-encoded as GitLab requires.
    """
    try:
        int(project)
        return project
    except ValueError:
        return urllib.parse.quote(project, safe='')


def get_merge_requests(gitlab_url, project_id, headers, state='merged',
                       since_date=None, exit_on_error=True):
    """Fetch all merge requests for a project, following pagination."""
    all_mrs = []
    page = 1
    per_page = 100

    while True:
        url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests'
        params = {
            'state': state,
            'per_page': per_page,
            'page': page,
            'order_by': 'updated_at',
            'sort': 'desc',
        }
        if since_date:
            params['updated_after'] = since_date.isoformat()

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching MRs: {response.status_code}")
            if response.status_code == 404:
                print("Project not found. Please check the project ID/path and "
                      "your access permissions.")
            elif response.status_code == 401:
                print("Authentication failed. Please check your GitLab token.")
            else:
                try:
                    print(response.json().get('message', 'Unknown error'))
                except ValueError:
                    print(response.text)
            if exit_on_error:
                sys.exit(1)
            return []

        mrs = response.json()
        if not mrs:
            break

        all_mrs.extend(mrs)
        page += 1
        if len(mrs) < per_page:
            break

    return all_mrs


def get_mr_changes(gitlab_url, project_id, mr_iid, headers):
    """Return the list of changes for a merge request (empty list on error)."""
    url = f'{gitlab_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error fetching MR changes: {response.status_code}")
        return []
    data = response.json()
    return data.get('changes', [])


def change_path(change):
    """Return the relevant file path for a change (new_path, else old_path)."""
    return change.get('new_path') or change.get('old_path', '')
