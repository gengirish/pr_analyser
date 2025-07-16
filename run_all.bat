@echo off
REM Run All Steps
REM This batch file sets the GitHub token, verifies it, and runs the analysis

echo GitHub PR Analyzer - Complete Workflow
echo =====================================
echo.

REM Check if a GitHub token was provided
if "%1"=="" (
    echo Error: No GitHub token provided.
    echo Usage: run_all.bat your_github_token_here
    exit /b 1
)

REM Step 1: Set the GitHub token for the current session
echo Step 1: Setting GitHub token...
set GITHUB_TOKEN=%1
echo Set GITHUB_TOKEN environment variable for current session.
echo.

REM Step 2: Verify the token
echo Step 2: Verifying GitHub token...
call check_token.bat
if %ERRORLEVEL% neq 0 (
    echo Token verification failed. Please check your token and try again.
    exit /b 1
)
echo.

REM Step 3: Run the analysis
echo Step 3: Running analysis on trending Java projects...
call analyze_trending_java.bat
echo.

echo All steps completed successfully!
echo.
echo To set the token permanently, run:
echo set_permanent_token_windows.bat %1
