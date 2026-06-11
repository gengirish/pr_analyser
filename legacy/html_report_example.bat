@echo off
echo GitHub PR Analyzer - HTML Report Example
echo ------------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer to generate an HTML report.
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
echo Please enter an output file name (or press Enter to use default pr_report.html):
set /p OUTPUT_FILE="> "

if "%OUTPUT_FILE%"=="" (
    set OUTPUT_FILE=pr_report.html
)

echo.
echo Please enter a title for the report (or press Enter to use default):
set /p REPORT_TITLE="> "

echo.
echo This example will analyze the repository: %REPO%
echo and generate an HTML report at: %OUTPUT_FILE%
if not "%REPORT_TITLE%"=="" (
    echo with title: %REPORT_TITLE%
)
echo.
echo Press any key to continue...
pause > nul

set COMMAND=python html_report.py --output %OUTPUT_FILE%

if not "%REPORT_TITLE%"=="" (
    set COMMAND=%COMMAND% --title "%REPORT_TITLE%"
)

set COMMAND=%COMMAND% %REPO%

echo Running: %COMMAND%
%COMMAND%

echo.
echo Example completed. Press any key to exit...
pause > nul
