#!/bin/bash

echo "GitHub PR Analyzer - CSV Output Example"
echo "-----------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer with CSV output format."
echo
echo "Please enter an output file name (or press Enter to use default pr_results.csv):"
read -p "> " OUTPUT_FILE

if [ -z "$OUTPUT_FILE" ]; then
    OUTPUT_FILE="pr_results.csv"
fi

echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024,"
echo "and save the results in CSV format to: $OUTPUT_FILE"
echo
echo "Press Enter to continue..."
read

echo "Running GitHub PR Analyzer with CSV output..."
python3 csv_output.py --output "$OUTPUT_FILE" tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
