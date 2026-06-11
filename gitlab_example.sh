#!/bin/bash
# Example script to analyze a GitLab repository
# This script demonstrates how to use the GitLab MR Analyzer

echo "GitLab MR Analyzer - Example Usage"
echo "==================================="
echo ""

# Prompt for GitLab token
read -p "Enter your GitLab Personal Access Token (or press Enter to skip): " GITLAB_TOKEN

echo ""
echo "Analyzing mycomplianceoffice/mco repository..."
echo ""

if [ -z "$GITLAB_TOKEN" ]; then
    python3 gitlab_mr_analyzer.py mycomplianceoffice/mco
else
    python3 gitlab_mr_analyzer.py --token "$GITLAB_TOKEN" mycomplianceoffice/mco
fi

echo ""
echo "Analysis complete!"
