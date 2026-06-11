@echo off
echo GitHub PR Analyzer - Combined Filter Example
echo -----------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer with multiple combined filters.
echo.
echo Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):
set /p CUSTOM_DATE="> "

if "%CUSTOM_DATE%"=="" (
    set CUSTOM_DATE=2024-11-01
)

echo.
echo Please enter file types to filter by (comma-separated, e.g., "py,js,html") or press Enter to skip:
set /p FILE_TYPES="> "

echo.
echo Please enter GitHub usernames to filter by (comma-separated, e.g., "user1,user2") or press Enter to skip:
set /p AUTHORS="> "

echo.
echo Please enter minimum number of files changed (or press Enter to use default 2):
set /p MIN_FILES="> "

if "%MIN_FILES%"=="" (
    set MIN_FILES=2
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with the following criteria:
echo - Merged after: %CUSTOM_DATE%
echo - Minimum files changed: %MIN_FILES%
if not "%AUTHORS%"=="" (
    echo - Authored by: %AUTHORS%
)
if not "%FILE_TYPES%"=="" (
    echo - Including file types: %FILE_TYPES%
)
echo.
echo Press any key to continue...
pause > nul

set COMMAND=python combined_filter.py --date %CUSTOM_DATE% --min-files %MIN_FILES%

if not "%AUTHORS%"=="" (
    set COMMAND=%COMMAND% --authors %AUTHORS%
)

if not "%FILE_TYPES%"=="" (
    set COMMAND=%COMMAND% --file-types %FILE_TYPES%
)

set COMMAND=%COMMAND% tensorflow/tensorflow

echo Running: %COMMAND%
%COMMAND%

echo.
echo Example completed. Press any key to exit...
pause > nul
