#!/bin/bash

echo "GitHub PR Analyzer - Combined Filter Example"
echo "-----------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer with multiple combined filters."
echo
echo "Please enter a date in YYYY-MM-DD format (or press Enter to use default 2024-11-01):"
read -p "> " CUSTOM_DATE

if [ -z "$CUSTOM_DATE" ]; then
    CUSTOM_DATE="2024-11-01"
fi

echo
echo "Please enter file types to filter by (comma-separated, e.g., \"py,js,html\") or press Enter to skip:"
read -p "> " FILE_TYPES

echo
echo "Please enter GitHub usernames to filter by (comma-separated, e.g., \"user1,user2\") or press Enter to skip:"
read -p "> " AUTHORS

echo
echo "Please enter minimum number of files changed (or press Enter to use default 2):"
read -p "> " MIN_FILES

if [ -z "$MIN_FILES" ]; then
    MIN_FILES="2"
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with the following criteria:"
echo "- Merged after: $CUSTOM_DATE"
echo "- Minimum files changed: $MIN_FILES"
if [ ! -z "$AUTHORS" ]; then
    echo "- Authored by: $AUTHORS"
fi
if [ ! -z "$FILE_TYPES" ]; then
    echo "- Including file types: $FILE_TYPES"
fi
echo
echo "Press Enter to continue..."
read

COMMAND="python3 combined_filter.py --date $CUSTOM_DATE --min-files $MIN_FILES"

if [ ! -z "$AUTHORS" ]; then
    COMMAND="$COMMAND --authors \"$AUTHORS\""
fi

if [ ! -z "$FILE_TYPES" ]; then
    COMMAND="$COMMAND --file-types \"$FILE_TYPES\""
fi

COMMAND="$COMMAND tensorflow/tensorflow"

echo "Running: $COMMAND"
eval $COMMAND

echo
echo "Example completed. Press Enter to exit..."
read
