@echo off
REM List Available Scripts
REM This batch file lists all available scripts and their purposes

echo Available Scripts for GitHub PR Analyzer
echo =======================================
echo.
echo Quick Start:
echo -----------
echo run_all.bat your_github_token_here
echo   - All-in-one script: sets token, verifies it, and runs analysis
echo.
echo Token Management:
echo ---------------
echo set_permanent_token_windows.bat your_github_token_here
echo   - Sets GITHUB_TOKEN environment variable permanently
echo.
echo set_github_token.bat your_github_token_here
echo   - Sets GITHUB_TOKEN for current session and runs analysis
echo.
echo check_token.bat
echo   - Verifies if GITHUB_TOKEN is set and valid
echo.
echo Analysis:
echo --------
echo analyze_trending_java.bat [your_github_token_here]
echo   - Analyzes top 10 trending Java projects on GitHub
echo   - Token is optional if GITHUB_TOKEN environment variable is set
echo.
echo Python Scripts:
echo -------------
echo python find_trending_java_projects.py [--token TOKEN] [--limit LIMIT]
echo   - Main script to find and analyze trending Java projects
echo.
echo python check_github_token.py
echo   - Checks if GITHUB_TOKEN is set and valid
echo.
echo python github_pr_analyzer.py owner/repo [--token TOKEN] [--output FILE] [--limit LIMIT]
echo   - Analyzes a specific GitHub repository for PRs
