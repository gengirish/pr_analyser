@echo off
echo GitHub PR Analyzer Example with Token
echo ----------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer with a GitHub token.
echo.
echo Please enter your GitHub Personal Access Token:
set /p TOKEN="> "

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024.
echo.
echo Press any key to continue...
pause > nul

python github_pr_analyzer.py --token %TOKEN% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
