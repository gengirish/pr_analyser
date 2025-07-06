#!/bin/bash

echo "GitHub PR Analyzer - Label Filter Example"
echo "-------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer to filter PRs by label."
echo
echo "Please enter GitHub labels to filter by (comma-separated, e.g., \"bug,enhancement,documentation\"):"
read -p "> " LABELS

if [ -z "$LABELS" ]; then
    echo "Error: At least one label must be specified."
    echo
    echo "Press Enter to exit..."
    read
    exit 1
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024"
echo "that have labels: $LABELS"
echo
echo "Press Enter to continue..."
read

python3 label_filter.py --labels "$LABELS" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
