@echo off
echo GitHub PR Analyzer - Label Filter Example
echo -------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to filter PRs by label.
echo.
echo Please enter GitHub labels to filter by (comma-separated, e.g., "bug,enhancement,documentation"):
set /p LABELS="> "

if "%LABELS%"=="" (
    echo Error: At least one label must be specified.
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024
echo that have labels: %LABELS%
echo.
echo Press any key to continue...
pause > nul

python label_filter.py --labels %LABELS% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
