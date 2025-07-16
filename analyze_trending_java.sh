#!/bin/bash
# Analyze Trending Java Projects
# This shell script runs the find_trending_java_projects.py script with a GitHub token

echo "Analyzing top 10 trending Java projects on GitHub..."

# Check if a GitHub token was provided as argument
if [ ! -z "$1" ]; then
    echo "Running with provided GitHub token from command line..."
    python3 find_trending_java_projects.py --token "$1" --limit 10
    exit 0
fi

# Check if GITHUB_TOKEN environment variable is set
if [ ! -z "$GITHUB_TOKEN" ]; then
    echo "Using GitHub token from GITHUB_TOKEN environment variable..."
    python3 find_trending_java_projects.py --limit 10
else
    echo "No GitHub token provided. Running without token (may hit rate limits)..."
    echo "To set a permanent token, use: export GITHUB_TOKEN=your_token_here"
    echo "To make it persistent, add the above line to your ~/.bashrc or ~/.zshrc file"
    python3 find_trending_java_projects.py --limit 10
fi

echo ""
echo "Analysis complete!"
