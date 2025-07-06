#!/bin/bash

echo "GitHub PR Analyzer - JSON Output Example"
echo "------------------------------------"
echo

echo "This example shows how to use the GitHub PR Analyzer with JSON output format."
echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024,"
echo "and save the results in JSON format to a file named \"pr_results.json\"."
echo
echo "Press Enter to continue..."
read

echo "Running GitHub PR Analyzer with JSON output..."
python3 json_output.py --output pr_results.json tensorflow/tensorflow

echo
echo "Results have been saved to pr_results.json"
echo
echo "Press Enter to exit..."
read
