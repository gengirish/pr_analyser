@echo off
REM Run All Steps
REM This batch file sets the GitHub token, verifies it, and runs the analysis for any language

echo GitHub PR Analyzer - Complete Workflow
echo =====================================
echo.

REM Usage info
if "%1"=="" (
    echo Error: No GitHub token provided.
    echo Usage: run_all.bat your_github_token_here [language] [limit]
    exit /b 1
)

setlocal

set "TOKEN=%1"
set "LANGUAGE=java"
set "LIMIT=20"

if not "%2"=="" set "LANGUAGE=%2"
if not "%3"=="" set "LIMIT=%3"

REM Step 1: Set the GitHub token for the current session
echo Step 1: Setting GitHub token...
set GITHUB_TOKEN=%TOKEN%
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
echo Step 3: Running analysis on trending %LANGUAGE% projects...
call analyze_trending_java.bat %TOKEN% %LANGUAGE% %LIMIT%
echo.

echo All steps completed successfully!
echo.
echo To set the token permanently, run:
echo set_permanent_token_windows.bat %TOKEN%

endlocal
