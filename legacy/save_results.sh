#!/bin/bash

echo "GitHub PR Analyzer - Save Results Example"
echo "--------------------------------------"
echo

echo "This example shows how to save the results of the GitHub PR Analyzer to a file."
echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024,"
echo "and save the results to a file named \"pr_results.txt\"."
echo
echo "Press Enter to continue..."
read

echo "Running GitHub PR Analyzer and saving results to pr_results.txt..."
python3 github_pr_analyzer.py tensorflow/tensorflow > pr_results.txt

echo
echo "Results have been saved to pr_results.txt"
echo
echo "Press Enter to view the results..."
read

cat pr_results.txt

echo
echo "Example completed. Press Enter to exit..."
read
