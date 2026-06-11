#!/bin/bash

echo "GitHub PR Analyzer - Multi-Repository Example"
echo "------------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to analyze multiple repositories."
echo
echo "Please enter repositories to analyze (comma-separated, e.g., \"owner1/repo1,owner2/repo2\"):"
read -p "> " REPOS

if [ -z "$REPOS" ]; then
    echo "Error: At least one repository must be specified."
    echo
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo
echo "Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):"
read -p "> " CUSTOM_DATE

if [ -z "$CUSTOM_DATE" ]; then
    CUSTOM_DATE="2024-11-01"
fi

echo
echo "Please enter minimum number of files changed (or press Enter to use default 2):"
read -p "> " MIN_FILES

if [ -z "$MIN_FILES" ]; then
    MIN_FILES="2"
fi

echo
echo "Please enter an output file name for JSON results (or press Enter to display in console):"
read -p "> " OUTPUT_FILE

echo
echo "This example will analyze the following repositories:"
echo "$REPOS"
echo "with the following criteria:"
echo "- Merged after: $CUSTOM_DATE"
echo "- Minimum files changed: $MIN_FILES"
if [ ! -z "$OUTPUT_FILE" ]; then
    echo "- Output file: $OUTPUT_FILE"
fi
echo
echo "Press Enter to continue..."
read

COMMAND="python3 multi_repo.py --date $CUSTOM_DATE --min-files $MIN_FILES"

if [ ! -z "$OUTPUT_FILE" ]; then
    COMMAND="$COMMAND --output $OUTPUT_FILE"
fi

COMMAND="$COMMAND \"$REPOS\""

echo "Running: $COMMAND"
eval $COMMAND

echo
echo "Example completed. Press Enter to exit..."
read
