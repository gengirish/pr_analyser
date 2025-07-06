# GitHub PR Analyzer

This Python script analyzes a GitHub repository to find pull requests that:
1. Have 2 or more file changes
2. Were merged after November 2024

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - `requests`
  - `python-dateutil`

## Installation

### Prerequisites

Install Python 3 from [python.org](https://www.python.org/downloads/) or using your system's package manager.

### Option 1: Using the installation scripts

The easiest way to install the required dependencies is to use the provided installation scripts:

- Windows: Run `install.bat`
- Linux/macOS: Run `./install.sh` (you may need to make it executable first with `chmod +x install.sh`)

### Option 2: Manual installation of dependencies

Install required packages:
   
```
pip install requests python-dateutil
```

Or using the provided requirements.txt file:
```
pip install -r requirements.txt
```

### Option 3: Install as a package

You can install the GitHub PR Analyzer as a package, which makes it available as a command-line tool.

Using the package installation scripts:
- Windows: Run `install_as_package.bat`
- Linux/macOS: Run `./install_as_package.sh` (you may need to make it executable first with `chmod +x install_as_package.sh`)

Or manually:
```
pip install .
```

This will install the `github-pr-analyzer` command, which you can run from anywhere on your system.

## Usage

### When running as a script:

```
python github_pr_analyzer.py [--token GITHUB_TOKEN] owner/repo
```

### When installed as a package:

```
github-pr-analyzer [--token GITHUB_TOKEN] owner/repo
```

### Arguments:
- `owner/repo`: GitHub repository in the format "owner/repo" (e.g., "octocat/hello-world")
- `--token`: GitHub personal access token (optional but recommended to avoid rate limits)

### Examples:

Basic usage as a script:
```
python github_pr_analyzer.py --token ghp_abc123 octocat/hello-world
```

Basic usage when installed as a package:
```
github-pr-analyzer --token ghp_abc123 octocat/hello-world
```

Using the provided example scripts:
- Windows: 
  - Run `example.bat` to analyze the TensorFlow repository without a token
  - Run `example_with_token.bat` to analyze the TensorFlow repository with a token (prompts for token input)
  - Run `save_results.bat` to save the analysis results to a file
- Linux/macOS: 
  - Run `./example.sh` to analyze the TensorFlow repository without a token
  - Run `./example_with_token.sh` to analyze the TensorFlow repository with a token (prompts for token input)
  - Run `./save_results.sh` to save the analysis results to a file
  - (You may need to make these executable first with `chmod +x example.sh example_with_token.sh save_results.sh`)

You can also save the results to a file manually using output redirection:
```
python github_pr_analyzer.py owner/repo > results.txt
```

## Creating a GitHub Personal Access Token

While the script can work without a token, GitHub API has rate limits that may prevent the script from completing for repositories with many PRs. To create a token:

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Click "Generate new token"
3. Give it a name and select the "repo" scope (to access repository data)
4. Click "Generate token" and copy the token value
5. Use this token with the `--token` parameter when running the script

## Output

The script will display a list of PRs that match the criteria, including:
- PR number and title
- Author username
- Merge date and time
- Number of files changed
- URL to the PR on GitHub

The results are sorted by merge date, with the most recently merged PRs shown first.

## Advanced Usage

### Custom Date Filter

A custom date filter script is included to demonstrate how to modify the GitHub PR Analyzer for specific needs:

```
python custom_date_filter.py --date YYYY-MM-DD owner/repo
```

This script allows you to specify a custom date filter instead of the hardcoded November 2024 date.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `custom_date_example.bat`
- Linux/macOS: Run `./custom_date_example.sh` (you may need to make it executable first with `chmod +x custom_date_example.sh`)

### JSON Output

A JSON output script is included to demonstrate how to output results in a machine-readable format:

```
python json_output.py [--token GITHUB_TOKEN] [--output FILE] owner/repo
```

This script outputs the results in JSON format, which is useful for programmatic processing or integration with other tools.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `json_output_example.bat`
- Linux/macOS: Run `./json_output_example.sh` (you may need to make it executable first with `chmod +x json_output_example.sh`)

### File Type Filter

A file type filter script is included to demonstrate how to filter PRs by specific file types:

```
python file_type_filter.py [--token GITHUB_TOKEN] [--file-types EXTENSIONS] owner/repo
```

This script filters PRs to only include those that have changes to files with the specified extensions.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `file_type_example.bat`
- Linux/macOS: Run `./file_type_example.sh` (you may need to make it executable first with `chmod +x file_type_example.sh`)

### Author Filter

An author filter script is included to demonstrate how to filter PRs by specific authors:

```
python author_filter.py [--token GITHUB_TOKEN] --authors USERNAMES owner/repo
```

This script filters PRs to only include those that were authored by the specified GitHub users.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `author_example.bat`
- Linux/macOS: Run `./author_example.sh` (you may need to make it executable first with `chmod +x author_example.sh`)

### Combined Filters

A combined filter script is included to demonstrate how to use multiple filters together:

```
python combined_filter.py [--token GITHUB_TOKEN] [--date DATE] [--authors USERNAMES] [--file-types EXTENSIONS] [--min-files N] owner/repo
```

This script allows you to combine multiple filters to create more complex queries:
- Custom date filter
- Author filter
- File type filter
- Minimum files changed filter

Example scripts are provided to demonstrate this functionality:
- Windows: Run `combined_example.bat`
- Linux/macOS: Run `./combined_example.sh` (you may need to make it executable first with `chmod +x combined_example.sh`)

### CSV Output

A CSV output script is included to demonstrate how to output results in CSV format:

```
python csv_output.py [--token GITHUB_TOKEN] [--output FILE] owner/repo
```

This script outputs the results in CSV format, which is useful for importing into spreadsheet software or other data analysis tools.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `csv_output_example.bat`
- Linux/macOS: Run `./csv_output_example.sh` (you may need to make it executable first with `chmod +x csv_output_example.sh`)

### Multi-Repository Analysis

A multi-repository script is included to demonstrate how to analyze multiple repositories in a single run:

```
python multi_repo.py [--token GITHUB_TOKEN] [--date DATE] [--min-files N] [--output FILE] "owner1/repo1,owner2/repo2,..."
```

This script allows you to analyze PRs across multiple repositories, which is useful for projects split across multiple repositories.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `multi_repo_example.bat`
- Linux/macOS: Run `./multi_repo_example.sh` (you may need to make it executable first with `chmod +x multi_repo_example.sh`)

### HTML Report Generation

An HTML report script is included to demonstrate how to generate interactive HTML reports:

```
python html_report.py [--token GITHUB_TOKEN] [--output FILE] [--title TITLE] owner/repo
```

This script generates an HTML report with interactive features like searching and sorting, which is useful for sharing results with team members or stakeholders.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `html_report_example.bat`
- Linux/macOS: Run `./html_report_example.sh` (you may need to make it executable first with `chmod +x html_report_example.sh`)

### Label Filter

A label filter script is included to demonstrate how to filter PRs by specific labels:

```
python label_filter.py [--token GITHUB_TOKEN] --labels LABELS owner/repo
```

This script filters PRs to only include those that have specific labels (e.g., "bug", "enhancement", "documentation").

Example scripts are provided to demonstrate this functionality:
- Windows: Run `label_example.bat`
- Linux/macOS: Run `./label_example.sh` (you may need to make it executable first with `chmod +x label_example.sh`)

### Directory Filter

A directory filter script is included to demonstrate how to filter PRs by specific directories or code areas:

```
python directory_filter.py [--token GITHUB_TOKEN] --directories DIRECTORIES owner/repo
```

This script filters PRs to only include those that have changes to files in specific directories or code areas.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `directory_example.bat`
- Linux/macOS: Run `./directory_example.sh` (you may need to make it executable first with `chmod +x directory_example.sh`)

### Review Analysis

A review analyzer script is included to demonstrate how to analyze PR review comments:

```
python review_analyzer.py [--token GITHUB_TOKEN] [--output FILE] owner/repo
```

This script analyzes PR review comments to provide insights into the review process, including sentiment analysis, common feedback themes, and reviewer statistics.

Example scripts are provided to demonstrate this functionality:
- Windows: Run `review_example.bat`
- Linux/macOS: Run `./review_example.sh` (you may need to make it executable first with `chmod +x review_example.sh`)

### Extending the Script

The GitHub PR Analyzer can be extended or modified to meet your specific requirements beyond the examples provided. Some additional ideas:
- Generate reports in additional formats (XML, etc.)
- Integrate with CI/CD pipelines or other development tools
- Create additional visualizations or dashboards of PR activity
- Analyze additional PR metrics like time to merge, size of changes, etc.
- Export data to databases for long-term analysis
- Add authentication for private repositories beyond personal access tokens
- Implement additional filtering criteria based on PR content or context
- Add support for other Git hosting platforms (GitLab, Bitbucket, etc.)

## Testing

A test script is included to verify the functionality of the GitHub PR Analyzer without making actual API calls:

```
python test_github_pr_analyzer.py
```

Or use the provided test runner scripts:
- Windows: Run `run_tests.bat`
- Linux/macOS: Run `./run_tests.sh` (you may need to make it executable first with `chmod +x run_tests.sh`)

This test script uses mock data to simulate GitHub API responses and verifies that the filtering logic works correctly. It's useful for:
- Testing the script without a GitHub token
- Avoiding GitHub API rate limits during development
- Verifying changes to the script's logic

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here are some ways you can contribute to this project:

1. Report bugs and request features by creating issues
2. Submit pull requests to fix bugs or add new features
3. Improve documentation
4. Share the project with others who might find it useful

When contributing code, please follow these guidelines:
- Write tests for new features
- Follow the existing code style
- Update documentation as needed
