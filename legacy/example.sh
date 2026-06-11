#!/bin/bash

echo "GitHub PR Analyzer Example"
echo "-------------------------"
echo
echo "This example will analyze the tensorflow/tensorflow repository"
echo "to find PRs with 2+ file changes merged after November 2024."
echo
echo "Press Enter to continue..."
read

python3 github_pr_analyzer.py tensorflow/tensorflow

echo
echo "Example completed. Press Enter to exit..."
read
