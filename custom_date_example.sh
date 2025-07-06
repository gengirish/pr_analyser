#!/bin/bash

echo "GitHub PR Analyzer - Custom Date Filter Example"
echo "-------------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer with a custom date filter."
echo
echo "Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):"
read -p "> " CUSTOM_DATE

if [ -z "$CUSTOM_DATE" ]; then
    CUSTOM_DATE="2024-11-01"
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after $CUSTOM_DATE."
echo
echo "Press Enter to continue..."
read

python3 custom_date_filter.py --date "$CUSTOM_DATE" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
