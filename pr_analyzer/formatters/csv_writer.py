"""CSV report writer."""

import csv

FIELDNAMES = ['PR Number', 'Title', 'Author', 'Merged At', 'Files Changed', 'URL']


def write_csv(path, prs):
    """Write filtered PRs to a CSV file.

    Each PR is a dict with ``number``, ``title``, ``author``, ``merged_at``
    (datetime), ``files_changed`` and ``url`` keys.
    """
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        for pr in prs:
            writer.writerow({
                'PR Number': pr['number'],
                'Title': pr['title'],
                'Author': pr['author'],
                'Merged At': pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S'),
                'Files Changed': pr['files_changed'],
                'URL': pr['url'],
            })
