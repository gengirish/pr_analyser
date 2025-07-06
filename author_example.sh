#!/bin/bash

echo "GitHub PR Analyzer - Author Filter Example"
echo "---------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to filter PRs by author."
echo
echo "Please enter GitHub usernames to filter by (comma-separated, e.g., \"user1,user2\"):"
read -p "> " AUTHORS

if [ -z "$AUTHORS" ]; then
    echo "Error: At least one author must be specified."
    echo
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024"
echo "that were authored by: $AUTHORS"
echo
echo "Press Enter to continue..."
read

python3 author_filter.py --authors "$AUTHORS" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
