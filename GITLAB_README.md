# GitLab MR Analyzer

This Python script analyzes a GitLab repository to find merge requests that:

1. Have 2 to 4 file changes
2. Were merged after November 2024
3. Include both source code files and test classes

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `python-dateutil`

## Installation

### Prerequisites

Install Python 3 from [python.org](https://www.python.org/downloads/) or using your system's package manager.

### Install Dependencies

Use the existing installation scripts from the main project:

- Windows: Run `install.bat`
- Linux/macOS: Run `./install.sh` (you may need to make it executable first with `chmod +x install.sh`)

Or install manually:

```bash
pip install requests python-dateutil
```

## Creating a GitLab Personal Access Token

To avoid rate limits and access private repositories, you'll need a GitLab Personal Access Token:

1. Go to [GitLab Settings > Access Tokens](https://gitlab.com/-/profile/personal_access_tokens)
2. Click "Add new token"
3. Give it a name (e.g., "MR Analyzer")
4. Select the following scopes:
   - `read_api` - Read access to the API
   - `read_repository` - Read access to repositories
5. Set an expiration date (optional but recommended)
6. Click "Create personal access token"
7. **Copy the token immediately** - you won't be able to see it again!

## Usage

### Basic Usage

```bash
python gitlab_mr_analyzer.py [--token GITLAB_TOKEN] [--output OUTPUT_FILE] [--limit LIMIT] project_path
```

### Arguments

- `project_path`: GitLab project path (e.g., "mycomplianceoffice/mco") or project ID (e.g., "12345")
- `--token`: GitLab personal access token (optional but recommended to avoid rate limits)
- `--output`: Output file path to save results (optional, defaults to timestamped file)
- `--limit`: Maximum number of matching MRs to find (default: 20)
- `--gitlab-url`: GitLab instance URL (default: https://gitlab.com) - use this for self-hosted GitLab

### Examples

**Analyze your repository (mycomplianceoffice/mco):**

```bash
python gitlab_mr_analyzer.py --token glpat-your-token-here mycomplianceoffice/mco
```

**Save results to a specific file:**

```bash
python gitlab_mr_analyzer.py --token glpat-your-token-here --output mco_results.txt mycomplianceoffice/mco
```

**Limit results to 10 MRs:**

```bash
python gitlab_mr_analyzer.py --token glpat-your-token-here --limit 10 mycomplianceoffice/mco
```

**Use with self-hosted GitLab:**

```bash
python gitlab_mr_analyzer.py --token glpat-your-token-here --gitlab-url https://gitlab.yourcompany.com mycomplianceoffice/mco
```

**Using project ID instead of path:**

```bash
python gitlab_mr_analyzer.py --token glpat-your-token-here 12345
```

### Using the Example Scripts

Quick start scripts are provided for convenience:

- **Windows**: Run `gitlab_example.bat`
- **Linux/macOS**: Run `./gitlab_example.sh` (make it executable first: `chmod +x gitlab_example.sh`)

These scripts will prompt you for your GitLab token and analyze the mycomplianceoffice/mco repository.

## Output

The script will display a list of MRs that match the criteria, including:

- MR number (IID) and title
- Author username
- Merge date and time
- Number of files changed
- List of source code files
- List of test files
- URL to the MR on GitLab

Results are automatically saved to a timestamped file (e.g., `mr_results_20250610_123045.txt`) unless you specify a custom output file.

The results are sorted by merge date, with the most recently merged MRs shown first.

## Finding Your Project Path or ID

### Method 1: From GitLab URL
Your project path is visible in the URL:
- URL: `https://gitlab.com/mycomplianceoffice/mco`
- Path: `mycomplianceoffice/mco`

### Method 2: From Project Settings
1. Go to your project on GitLab
2. Click "Settings" > "General"
3. The project ID is shown at the top of the page
4. You can use either the path or the ID with this tool

## Troubleshooting

### Error: "Project not found"
- Check that the project path is correct
- Ensure your token has access to the project
- For private projects, make sure your token has the `read_api` scope

### Error: "Authentication failed"
- Verify your GitLab token is correct
- Check that the token hasn't expired
- Ensure the token has the required scopes (`read_api`, `read_repository`)

### Rate Limiting
- Always use a personal access token to avoid rate limits
- GitLab.com has rate limits even with tokens (10,000 requests per hour for authenticated users)
- For self-hosted GitLab, rate limits may vary

### No Results Found
- Try increasing the `--limit` parameter
- Check if your repository has MRs that meet the criteria:
  - Merged after November 1, 2024
  - Have 2-4 file changes
  - Include both source code files AND test files
- Verify the date filter is appropriate for your repository

## Differences from GitHub Version

This GitLab version has been adapted from the GitHub PR Analyzer with the following changes:

1. **API Endpoints**: Uses GitLab API v4 instead of GitHub API v3
2. **Authentication**: Uses `PRIVATE-TOKEN` header instead of `Authorization: token`
3. **Terminology**: Uses "Merge Requests (MRs)" instead of "Pull Requests (PRs)"
4. **Project Identification**: Supports both project path and project ID
5. **URL Structure**: Adapted for GitLab's URL structure
6. **File Changes API**: Uses GitLab's `/changes` endpoint instead of `/files`

## Advanced Usage

### Custom Date Filter

You can modify the script to use a different date filter by editing line 180:

```python
# Change this line:
target_date = datetime.datetime(2024, 11, 1, tzinfo=datetime.timezone.utc)

# To your desired date:
target_date = datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)
```

### Custom File Filters

You can modify the file type detection logic (lines 220-230) to:
- Add more file extensions
- Change test file detection patterns
- Add custom exclusion patterns

### Integration with CI/CD

You can integrate this script into your GitLab CI/CD pipeline:

```yaml
analyze_mrs:
  script:
    - pip install requests python-dateutil
    - python gitlab_mr_analyzer.py --token $GITLAB_TOKEN --output mr_analysis.txt $CI_PROJECT_PATH
  artifacts:
    paths:
      - mr_analysis.txt
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to:
- Report bugs and request features by creating issues
- Submit pull requests to fix bugs or add new features
- Improve documentation
- Share the project with others

## Related Tools

- **GitHub PR Analyzer**: The original version for GitHub repositories (`github_pr_analyzer.py`)
- **Multi-Repository Analysis**: See `multi_repo.py` for analyzing multiple repositories
- **Various Output Formats**: Check out `json_output.py`, `csv_output.py`, and `html_report.py`
