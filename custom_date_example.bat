@echo off
echo GitHub PR Analyzer - Custom Date Filter Example
echo -------------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer with a custom date filter.
echo.
echo Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):
set /p CUSTOM_DATE="> "

if "%CUSTOM_DATE%"=="" (
    set CUSTOM_DATE=2024-11-01
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after %CUSTOM_DATE%.
echo.
echo Press any key to continue...
pause > nul

python custom_date_filter.py --date %CUSTOM_DATE% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
