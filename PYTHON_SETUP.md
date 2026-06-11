# Python Installation Guide for Windows

## Issue: Python Not Found

You're seeing this error because Python is not properly installed or configured on your system. The Windows Store shortcuts are placeholders that don't actually have Python installed.

## Solution: Install Python Properly

### Option 1: Install Python from Official Website (Recommended)

1. **Download Python:**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version)

2. **Install Python:**
   - Run the downloaded installer
   - ⚠️ **IMPORTANT**: Check the box "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Installation:**
   Open a NEW terminal (Git Bash or Command Prompt) and run:
   ```bash
   python --version
   ```
   You should see: `Python 3.x.x`

### Option 2: Install via Chocolatey (Windows Package Manager)

If you have Chocolatey installed:
```bash
choco install python
```

### Option 3: Install via Winget (Windows Package Manager)

```bash
winget install Python.Python.3.12
```

## After Installing Python

### Step 1: Verify Python Installation

Open a NEW terminal and run:
```bash
python --version
pip --version
```

Both commands should work without errors.

### Step 2: Install Project Dependencies

Navigate to the project directory and run:

**Using Command Prompt or PowerShell:**
```bash
cd C:\Users\GirishHiremath\Documents\codebase\pr_analyser
pip install requests python-dateutil
```

**Using Git Bash:**
```bash
cd ~/Documents/codebase/pr_analyser
pip install requests python-dateutil
```

### Step 3: Test the GitLab Analyzer

```bash
python gitlab_mr_analyzer.py --help
```

You should see the help message with all available options.

## Troubleshooting

### Issue: "python: command not found" after installation

**Solution:** Close ALL terminal windows and open a new one. The PATH changes only take effect in new terminals.

### Issue: Python installed but pip not found

**Solution:** Reinstall Python and make sure to check "Add Python to PATH" during installation.

### Issue: Multiple Python versions

**Solution:** Use the full path to the Python you want:
```bash
C:\Users\GirishHiremath\AppData\Local\Programs\Python\Python312\python.exe gitlab_mr_analyzer.py --help
```

### Issue: Permission errors when installing packages

**Solution:** Use the `--user` flag:
```bash
pip install --user requests python-dateutil
```

## Quick Start After Python Installation

Once Python is installed and working:

1. **Install dependencies:**
   ```bash
   pip install requests python-dateutil
   ```

2. **Get your GitLab token:**
   - Go to: https://gitlab.com/-/profile/personal_access_tokens
   - Create token with `read_api` and `read_repository` scopes

3. **Run the analyzer:**
   ```bash
   python gitlab_mr_analyzer.py --token glpat-YOUR-TOKEN mycomplianceoffice/mco
   ```

## Alternative: Use Python from Microsoft Store

If you prefer the Microsoft Store version:

1. Open Microsoft Store
2. Search for "Python 3.12" (or latest version)
3. Click "Get" or "Install"
4. After installation, open a NEW terminal
5. Run: `python --version`

**Note:** The Microsoft Store version may have some limitations. The official Python.org version is recommended for development.

## Need Help?

If you continue to have issues:
1. Make sure you've closed ALL terminal windows after installing Python
2. Restart your computer if PATH changes aren't taking effect
3. Check that Python is in your PATH: `echo $PATH` (Git Bash) or `echo %PATH%` (CMD)
4. Look for Python installation directory (usually `C:\Users\YourName\AppData\Local\Programs\Python\`)
