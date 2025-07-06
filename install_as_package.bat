@echo off
echo GitHub PR Analyzer - Package Installation Script
echo -------------------------------------------
echo.

echo Installing GitHub PR Analyzer as a package...
pip install .

echo.
echo Installation completed successfully!
echo.
echo You can now run the analyzer using:
echo   github-pr-analyzer [--token GITHUB_TOKEN] owner/repo
echo.
echo For more information, please refer to the README.md file.
echo.
echo Press any key to exit...
pause > nul
