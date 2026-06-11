@echo off
echo GitHub PR Analyzer Example
echo -------------------------
echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024.
echo.
echo Press any key to continue...
pause > nul

python github_pr_analyzer.py tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
