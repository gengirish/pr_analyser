"""Interactive HTML report writer."""

import datetime

_STYLE = """
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2, h3 { color: #0366d6; }
        .header {
            border-bottom: 2px solid #0366d6;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        .summary {
            background-color: #f6f8fa;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .pr-card {
            border: 1px solid #e1e4e8;
            border-radius: 5px;
            padding: 15px;
            margin-bottom: 15px;
            transition: all 0.3s ease;
        }
        .pr-card:hover { box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); }
        .pr-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
        .pr-meta { color: #586069; font-size: 14px; }
        .pr-link {
            display: inline-block;
            margin-top: 10px;
            color: #0366d6;
            text-decoration: none;
        }
        .pr-link:hover { text-decoration: underline; }
        .search-box {
            width: 100%;
            padding: 10px;
            margin-bottom: 20px;
            border: 1px solid #e1e4e8;
            border-radius: 5px;
            font-size: 16px;
        }
        .filters { display: flex; gap: 10px; margin-bottom: 20px; }
        .filter-button {
            background-color: #0366d6;
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 5px;
            cursor: pointer;
        }
        .filter-button:hover { background-color: #0255b3; }
        .footer {
            margin-top: 30px;
            border-top: 1px solid #e1e4e8;
            padding-top: 15px;
            color: #586069;
            font-size: 14px;
        }
"""

_SCRIPT = """
        document.getElementById('searchBox').addEventListener('keyup', function() {
            const searchTerm = this.value.toLowerCase();
            document.querySelectorAll('.pr-card').forEach(card => {
                const text = card.textContent.toLowerCase();
                card.style.display = text.includes(searchTerm) ? 'block' : 'none';
            });
        });

        function sortByDate() { sortCards('date', true); }
        function sortByFiles() { sortCards('files', true); }
        function sortByAuthor() { sortCards('author', false); }

        function sortCards(attribute, isNumeric) {
            const prList = document.getElementById('pr-list');
            const prCards = Array.from(document.querySelectorAll('.pr-card'));
            prCards.sort((a, b) => {
                let aValue = a.getAttribute('data-' + attribute);
                let bValue = b.getAttribute('data-' + attribute);
                return isNumeric ? bValue.localeCompare(aValue) : aValue.localeCompare(bValue);
            });
            prList.innerHTML = '';
            prCards.forEach(card => prList.appendChild(card));
        }
"""


def generate_html_report(repo, filtered_prs, title):
    """Build the HTML report string for the given repo and PRs."""
    owner, repo_name = repo.split('/')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    cards = []
    for pr in filtered_prs:
        merged_at = pr['merged_at'].strftime('%Y-%m-%d %H:%M:%S')
        cards.append(f"""
        <div class="pr-card" data-author="{pr['author'].lower()}" data-files="{pr['files_changed']}" data-date="{pr['merged_at'].isoformat()}">
            <div class="pr-title">PR #{pr['number']}: {pr['title']}</div>
            <div class="pr-meta">
                <p>Author: {pr['author']}</p>
                <p>Merged: {merged_at}</p>
                <p>Files changed: {pr['files_changed']}</p>
            </div>
            <a href="{pr['url']}" class="pr-link" target="_blank">View on GitHub</a>
        </div>
""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{_STYLE}</style>
</head>
<body>
    <div class="header">
        <h1>{title}</h1>
        <p>Repository: <a href="https://github.com/{owner}/{repo_name}" target="_blank">{owner}/{repo_name}</a></p>
        <p>Generated on: {now}</p>
    </div>

    <div class="summary">
        <h2>Summary</h2>
        <p>Found <strong>{len(filtered_prs)}</strong> pull requests with 2+ file changes merged after November 2024.</p>
    </div>

    <input type="text" class="search-box" id="searchBox" placeholder="Search PRs by title, author, etc.">

    <div class="filters">
        <button class="filter-button" onclick="sortByDate()">Sort by Date</button>
        <button class="filter-button" onclick="sortByFiles()">Sort by Files Changed</button>
        <button class="filter-button" onclick="sortByAuthor()">Sort by Author</button>
    </div>

    <div id="pr-list">
{''.join(cards)}
    </div>

    <div class="footer">
        <p>Generated by GitHub PR Analyzer</p>
    </div>

    <script>{_SCRIPT}</script>
</body>
</html>
"""
