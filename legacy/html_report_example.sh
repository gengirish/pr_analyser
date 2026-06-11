#!/bin/bash

echo "GitHub PR Analyzer - HTML Report Example"
echo "------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to generate an HTML report."
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
echo "Please enter an output file name (or press Enter to use default pr_report.html):"
read -p "> " OUTPUT_FILE

if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="pr_report.html"
fi

echo
echo "Please enter a title for the report (or press Enter to use default):"
read -p "> " REPORT_TITLE

echo
echo "This example will analyze the repository: $REPO"
echo "and generate an HTML report at: $OUTPUT_FILE"
if [ ! -z "$REPORT_TITLE" ]; then
    echo "with title: $REPORT_TITLE"
fi
echo
echo "Press Enter to continue..."
read

COMMAND="python3 html_report.py --output $OUTPUT_FILE"

if [ ! -z "$REPORT_TITLE" ]; then
    COMMAND="$COMMAND --title \"$REPORT_TITLE\""
fi

COMMAND="$COMMAND $REPO"

echo "Running: $COMMAND"
eval $COMMAND

echo
echo "Example completed. Press Enter to exit..."
read
