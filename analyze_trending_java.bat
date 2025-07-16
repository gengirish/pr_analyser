@echo off
REM Analyze Trending Java Projects
REM This batch file runs the find_trending_java_projects.py script with a GitHub token

echo Analyzing top 20 trending Java projects on GitHub...

REM Check if a GitHub token was provided as argument
if not "%1"=="" (
    echo Running with provided GitHub token from command line...
    python find_trending_java_projects.py --token %1 --limit 20
    goto :end
)

REM Check if GITHUB_TOKEN environment variable is set
if defined GITHUB_TOKEN (
    echo Using GitHub token from GITHUB_TOKEN environment variable...
    python find_trending_java_projects.py --limit 20
) else (
    echo No GitHub token provided. Running without token ^(may hit rate limits^)...
    echo To set a permanent token, use: setx GITHUB_TOKEN your_token_here
    python find_trending_java_projects.py --limit 20
)

:end
echo.
echo Analysis complete!
