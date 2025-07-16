@echo off
REM Set GitHub Token and Run Analysis
REM This batch file sets the GITHUB_TOKEN environment variable and runs the analysis

echo Setting up GitHub token and running analysis...

REM Check if a GitHub token was provided
if "%1"=="" (
    echo Error: No GitHub token provided.
    echo Usage: set_github_token.bat your_github_token_here
    exit /b 1
)

REM Set the GITHUB_TOKEN environment variable for the current session
set GITHUB_TOKEN=%1
echo Set GITHUB_TOKEN environment variable for current session.

REM Run the analysis
call analyze_trending_java.bat

echo.
echo To set the GITHUB_TOKEN permanently, run:
echo setx GITHUB_TOKEN %1
echo.
echo Note: After using setx, you'll need to open a new command prompt for the change to take effect.
