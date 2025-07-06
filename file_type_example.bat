@echo off
echo GitHub PR Analyzer - File Type Filter Example
echo -----------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to filter PRs by file type.
echo.
echo Please enter file types to filter by (comma-separated, e.g., "py,js,html"):
set /p FILE_TYPES="> "

if "%FILE_TYPES%"=="" (
    set FILE_TYPES=py
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024
echo that include changes to files with extensions: %FILE_TYPES%
echo.
echo Press any key to continue...
pause > nul

python file_type_filter.py --file-types %FILE_TYPES% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
