@echo off
echo GitHub PR Analyzer - CSV Output Example
echo -----------------------------------
echo.
echo This example shows how to use the GitHub PR Analyzer with CSV output format.
echo.
echo Please enter an output file name (or press Enter to use default pr_results.csv):
set /p OUTPUT_FILE="> "

if "%OUTPUT_FILE%"=="" (
    set OUTPUT_FILE=pr_results.csv
)

echo.
echo This example will analyze the tensorflow/tensorflow repository
echo to find PRs with 2+ file changes merged after November 2024,
echo and save the results in CSV format to: %OUTPUT_FILE%
echo.
echo Press any key to continue...
pause > nul

echo Running GitHub PR Analyzer with CSV output...
python csv_output.py --output %OUTPUT_FILE% tensorflow/tensorflow

echo.
echo Example completed. Press any key to exit...
pause > nul
