#!/bin/bash

echo "GitHub PR Analyzer - Installation Script"
echo "--------------------------------------"
echo

echo "Installing required packages..."
pip install -r requirements.txt

echo
echo "Installation completed successfully!"
echo
echo "You can now run the analyzer using:"
echo "  python github_pr_analyzer.py [--token GITHUB_TOKEN] owner/repo"
echo
echo "For more information, please refer to the README.md file."
echo
echo "Press Enter to exit..."
read
