@echo off
REM Example script to analyze a GitLab repository
REM This script demonstrates how to use the GitLab MR Analyzer

echo GitLab MR Analyzer - Example Usage
echo ===================================
echo.

REM Prompt for GitLab token
set /p GITLAB_TOKEN="Enter your GitLab Personal Access Token (or press Enter to skip): "

echo.
echo Analyzing mycomplianceoffice/mco repository...
echo.

if "%GITLAB_TOKEN%"=="" (
    python gitlab_mr_analyzer.py mycomplianceoffice/mco
) else (
    python gitlab_mr_analyzer.py --token %GITLAB_TOKEN% mycomplianceoffice/mco
)

echo.
echo Analysis complete!
pause
