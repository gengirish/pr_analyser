# Trending Java Projects PR Analyzer

This tool finds the top 10 trending Java projects on GitHub and analyzes their pull requests using the GitHub PR Analyzer script.

## Features

- Automatically finds the top 10 trending Java projects on GitHub (sorted by stars)
- Analyzes each project's pull requests to find those that:
  - Have 2 to 4 file changes
  - Were merged after November 2024
  - Include both source code files and test classes
- Creates output files with the analysis results for each repository

## Requirements

- Python 3.6 or higher
- Required Python packages (install with `pip install -r requirements.txt`):
  - requests
  - python-dateutil

## Usage

### Getting Started

To see all available scripts and their purposes, run:

```
# Windows
list_scripts.bat

# Unix/Linux/Mac
./list_scripts.sh
```

### Quick Start (Recommended)

Use the all-in-one scripts that handle token setup, verification, and analysis in one step:

```
# Windows
run_all.bat your_github_token_here

# Unix/Linux/Mac
./run_all.sh your_github_token_here
```

### Individual Scripts

#### Windows

```
analyze_trending_java.bat [GITHUB_TOKEN]
```

#### Unix/Linux/Mac

```
./analyze_trending_java.sh [GITHUB_TOKEN]
```

#### Direct Python Usage

```
python find_trending_java_projects.py [--token GITHUB_TOKEN] [--limit PR_LIMIT]
```

Arguments:
- `--token`: GitHub personal access token (optional but recommended to avoid rate limits)
- `--limit`: Maximum number of matching PRs to find per repository (default: 20)

## Output

The script creates output files for each analyzed repository in the format:
```
owner-repo-pr-[limit].txt
```

For example:
```
spring-projects-spring-boot-pr-10.txt
```

Each output file contains information about the matching pull requests, including:
- PR number and title
- Author
- Merge date
- Files changed (both source and test files)
- URL to the PR

## GitHub Rate Limits

Without a GitHub token, you may hit API rate limits. It's recommended to use a personal access token when running the script.

To create a GitHub token:
1. Go to GitHub Settings > Developer settings > Personal access tokens
2. Generate a new token with the `repo` scope
3. Use the token in one of the following ways:

### Setting Up a GitHub Token

#### Option 1: Set Permanent Token (Recommended)

We've provided scripts to set the GITHUB_TOKEN environment variable permanently:

```
# Windows
set_permanent_token_windows.bat your_github_token_here

# Unix/Linux/Mac
./set_permanent_token_unix.sh your_github_token_here
```

These scripts will:
- Set the token permanently in your user environment or shell profile
- Provide instructions on how to verify the token is set
- Set the token for the current session as well

#### Verifying Your Token

To verify that your GitHub token is correctly set up, run:

```
# Windows
check_token.bat

# Unix/Linux/Mac
./check_token.sh

# Or directly with Python
python check_github_token.py
```

This will:
- Check if the GITHUB_TOKEN environment variable is set
- Test the token's validity by making a request to the GitHub API
- Display your GitHub username and API rate limit if the token is valid

#### Option 2: Using Helper Scripts (For Current Session)

These scripts set the GITHUB_TOKEN environment variable for the current session only and run the analysis:

```
# Windows
set_github_token.bat your_github_token_here

# Unix/Linux/Mac
./set_github_token.sh your_github_token_here
```

#### Option 3: Pass as Command Line Argument (Temporary)

```
# Windows
analyze_trending_java.bat your_github_token_here

# Unix/Linux/Mac
./analyze_trending_java.sh your_github_token_here
```

#### Option 4: Set as Environment Variable Manually

##### Windows

```
# Set for current session only
set GITHUB_TOKEN=your_github_token_here

# Set permanently for your user account
setx GITHUB_TOKEN your_github_token_here
```

After using `setx`, you'll need to open a new command prompt for the change to take effect.

##### Unix/Linux/Mac

```
# Set for current session only
export GITHUB_TOKEN=your_github_token_here

# Set permanently (add to your shell profile)
echo 'export GITHUB_TOKEN=your_github_token_here' >> ~/.bashrc
# or for Zsh
echo 'export GITHUB_TOKEN=your_github_token_here' >> ~/.zshrc
```

After adding to your shell profile, run `source ~/.bashrc` (or `source ~/.zshrc`) or restart your terminal for the changes to take effect.

## Example

```
./analyze_trending_java.sh ghp_your_github_token_here
```

This will:
1. Find the top 10 trending Java projects on GitHub
2. Analyze each project's PRs (up to 10 matching PRs per project)
3. Create output files with the results
