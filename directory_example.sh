#!/bin/bash

echo "GitHub PR Analyzer - Directory Filter Example"
echo "----------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to filter PRs by directory."
echo
echo "Please enter directories to filter by (comma-separated, e.g., \"src,docs,tests\"):"
read -p "> " DIRECTORIES

if [ -z "$DIRECTORIES" ]; then
    echo "Error: At least one directory must be specified."
    echo
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024"
echo "that include changes to directories: $DIRECTORIES"
echo
echo "Press Enter to continue..."
read

python3 directory_filter.py --directories "$DIRECTORIES" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
