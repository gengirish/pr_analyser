@echo off
REM Analyze Trending Projects for Any Language
REM This batch file runs the find_trending_java_projects.py script with optional GitHub token, language, and PR limit

REM Usage:
REM   analyze_trending_java.bat [GITHUB_TOKEN] [LANGUAGE] [LIMIT]
REM   - GITHUB_TOKEN: GitHub personal access token (optional)
REM   - LANGUAGE: Programming language to search for (default: java)
REM   - LIMIT: Max PRs per repo (default: 20)

setlocal

REM Set defaults
set "LANGUAGE=java"
set "LIMIT=20"

REM Parse arguments
if not "%1"=="" set "TOKEN=%1"
if not "%2"=="" set "LANGUAGE=%2"
if not "%3"=="" set "LIMIT=%3"

echo Analyzing top %LIMIT% trending %LANGUAGE% projects on GitHub...

REM Build the command
set "CMD=python find_trending_java_projects.py --language %LANGUAGE% --limit %LIMIT%"

REM Add token if provided
if defined TOKEN (
    echo Running with provided GitHub token from command line...
    set "CMD=%CMD% --token %TOKEN%"
) else if defined GITHUB_TOKEN (
    echo Using GitHub token from GITHUB_TOKEN environment variable...
) else (
    echo No GitHub token provided. Running without token ^(may hit rate limits^)...
    echo To set a permanent token, use: setx GITHUB_TOKEN your_token_here
)

REM Run the command
%CMD%

:end
echo.
echo Analysis complete!
endlocal
