@echo off
echo GitHub PR Analyzer - Review Analysis Example
echo ---------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to analyze PR review comments.
echo.
echo Please enter a repository to analyze (in the format "owner/repo"):
set /p REPO="> "

if "%REPO%"=="" (
    echo Error: Repository must be specified.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo.
echo Please enter an output file name (or press Enter to display in console only):
set /p OUTPUT_FILE="> "

echo.
echo This example will analyze the repository: %REPO%
echo to find PRs with 2+ file changes merged after November 2024
echo and analyze their review comments.
if not "%OUTPUT_FILE%"=="" (
    echo Results will be saved to: %OUTPUT_FILE%
)
echo.
echo Press any key to continue...
pause > nul

set COMMAND=python review_analyzer.py

if not "%OUTPUT_FILE%"=="" (
    set COMMAND=%COMMAND% --output %OUTPUT_FILE%
)

set COMMAND=%COMMAND% %REPO%

echo Running: %COMMAND%
%COMMAND%

echo.
echo Example completed. Press any key to exit...
pause > nul
