#!/bin/bash

echo "GitHub PR Analyzer - File Type Filter Example"
echo "-----------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to filter PRs by file type."
echo
echo "Please enter file types to filter by (comma-separated, e.g., \"py,js,html\"):"
read -p "> " FILE_TYPES

if [ -z "$FILE_TYPES" ]; then
    FILE_TYPES="py"
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024"
echo "that include changes to files with extensions: $FILE_TYPES"
echo
echo "Press Enter to continue..."
read

python3 file_type_filter.py --file-types "$FILE_TYPES" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
