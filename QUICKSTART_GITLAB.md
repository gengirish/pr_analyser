# GitLab MR Analyzer - Quick Start Guide

Get started analyzing your GitLab repository in 3 simple steps!

## Step 1: Install Dependencies

### Windows
```bash
install.bat
```

### Linux/macOS
```bash
chmod +x install.sh
./install.sh
```

## Step 2: Get Your GitLab Token

1. Go to: https://gitlab.com/-/profile/personal_access_tokens
2. Click **"Add new token"**
3. Name it: `MR Analyzer`
4. Select scopes:
   - ✅ `read_api`
   - ✅ `read_repository`
5. Click **"Create personal access token"**
6. **Copy the token** (starts with `glpat-`)

## Step 3: Run the Analyzer

### For mycomplianceoffice/mco repository:

**Windows:**
```bash
python gitlab_mr_analyzer.py --token glpat-YOUR-TOKEN-HERE mycomplianceoffice/mco
```

**Linux/macOS:**
```bash
python3 gitlab_mr_analyzer.py --token glpat-YOUR-TOKEN-HERE mycomplianceoffice/mco
```

### Or use the example script:

**Windows:**
```bash
gitlab_example.bat
```

**Linux/macOS:**
```bash
chmod +x gitlab_example.sh
./gitlab_example.sh
```

## What You'll Get

The analyzer will find merge requests that:
- ✅ Have 2-4 file changes
- ✅ Were merged after November 2024
- ✅ Include both source code AND test files

Results are saved to a timestamped file like `mr_results_20250610_123045.txt`

## Example Output

```
MR !1234: Add user authentication feature
  Author: john.doe
  Merged: 2024-12-15 14:30:00
  Files changed: 3
  Source files: src/auth/login.py, src/auth/session.py
  Test files: tests/test_auth.py
  URL: https://gitlab.com/mycomplianceoffice/mco/-/merge_requests/1234
```

## Common Options

### Save to specific file:
```bash
python gitlab_mr_analyzer.py --token YOUR-TOKEN --output my_results.txt mycomplianceoffice/mco
```

### Limit results to 10 MRs:
```bash
python gitlab_mr_analyzer.py --token YOUR-TOKEN --limit 10 mycomplianceoffice/mco
```

### Use with self-hosted GitLab:
```bash
python gitlab_mr_analyzer.py --token YOUR-TOKEN --gitlab-url https://gitlab.yourcompany.com mycomplianceoffice/mco
```

## Troubleshooting

### "Project not found"
- Check the project path: `mycomplianceoffice/mco`
- Ensure your token has access to the project

### "Authentication failed"
- Verify your token is correct
- Check token hasn't expired
- Ensure token has `read_api` and `read_repository` scopes

### No results found
- Try `--limit 50` to search more MRs
- Check if your repo has MRs matching the criteria
- Verify MRs were merged after November 2024

## Need More Help?

See the full documentation: [GITLAB_README.md](GITLAB_README.md)

## What's Next?

Once you're comfortable with the basic analyzer, you can:
- Modify the date filter (edit line 180 in `gitlab_mr_analyzer.py`)
- Adjust file count criteria (edit line 213)
- Customize file type detection (edit lines 220-230)
- Integrate with CI/CD pipelines

Happy analyzing! 🚀
