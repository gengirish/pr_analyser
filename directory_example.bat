@echo off
echo GitHub PR Analyzer - Directory Filter Example
echo ----------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to filter PRs by directory.
echo.
echo Please enter directories to filter by (comma-separated, e.g., "src,docs,tests"):
set /p DIRECTORIES="> "

if "%DIRECTORIES%"=="" (
    echo Error: At least one directory must be specified.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024
echo that include changes to directories: %DIRECTORIES%
echo.
echo Press any key to continue...
pause > nul

python directory_filter.py --directories %DIRECTORIES% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
