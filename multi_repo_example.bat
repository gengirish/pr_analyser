@echo off
echo GitHub PR Analyzer - Multi-Repository Example
echo ------------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to analyze multiple repositories.
echo.
echo Please enter repositories to analyze (comma-separated, e.g., "owner1/repo1,owner2/repo2"):
set /p REPOS="> "

if "%REPOS%"=="" (
    echo Error: At least one repository must be specified.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo.
echo Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):
set /p CUSTOM_DATE="> "

if "%CUSTOM_DATE%"=="" (
    set CUSTOM_DATE=2024-11-01
)

echo.
echo Please enter minimum number of files changed (or press Enter to use default 2):
set /p MIN_FILES="> "

if "%MIN_FILES%"=="" (
    set MIN_FILES=2
)

echo.
echo Please enter an output file name for JSON results (or press Enter to display in console):
set /p OUTPUT_FILE="> "

echo.
echo This example will analyze the following repositories:
echo %REPOS%
echo with the following criteria:
echo - Merged after: %CUSTOM_DATE%
echo - Minimum files changed: %MIN_FILES%
if not "%OUTPUT_FILE%"=="" (
    echo - Output file: %OUTPUT_FILE%
)
echo.
echo Press any key to continue...
pause > nul

set COMMAND=python multi_repo.py --date %CUSTOM_DATE% --min-files %MIN_FILES%

if not "%OUTPUT_FILE%"=="" (
    set COMMAND=%COMMAND% --output %OUTPUT_FILE%
)

set COMMAND=%COMMAND% "%REPOS%"

echo Running: %COMMAND%
%COMMAND%

echo.
echo Example completed. Press any key to exit...
pause > nul
