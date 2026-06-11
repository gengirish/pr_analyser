@echo off
echo GitHub PR Analyzer - Author Filter Example
echo ---------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to filter PRs by author.
echo.
echo Please enter GitHub usernames to filter by (comma-separated, e.g., "user1,user2"):
set /p AUTHORS="> "

if "%AUTHORS%"=="" (
    echo Error: At least one author must be specified.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024
echo that were authored by: %AUTHORS%
echo.
echo Press any key to continue...
pause > nul

python author_filter.py --authors %AUTHORS% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
