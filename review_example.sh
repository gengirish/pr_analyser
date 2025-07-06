#!/bin/bash

echo "GitHub PR Analyzer - Review Analysis Example"
echo "---------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to analyze PR review comments."
echo
echo "Please enter a repository to analyze (in the format \"owner/repo\"):"
read -p "> " REPO

if [ -z "$REPO" ]; then
    echo "Error: Repository must be specified."
    echo
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo
echo "Please enter an output file name (or press Enter to display in console only):"
read -p "> " OUTPUT_FILE

echo
echo "This example will analyze the repository: $REPO"
echo "to find PRs with 2+ file changes merged after November 2024"
echo "and analyze their review comments."
if [ ! -z "$OUTPUT_FILE" ]; then
    echo "Results will be saved to: $OUTPUT_FILE"
fi
echo
echo "Press Enter to continue..."
read

COMMAND="python3 review_analyzer.py"

if [ ! -z "$OUTPUT_FILE" ]; then
    COMMAND="$COMMAND --output $OUTPUT_FILE"
fi

COMMAND="$COMMAND $REPO"

echo "Running: $COMMAND"
eval $COMMAND

echo
echo "Example completed. Press Enter to exit..."
read
