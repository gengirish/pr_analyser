#!/bin/bash
# Set GitHub Token and Run Analysis
# This shell script sets the GITHUB_TOKEN environment variable and runs the analysis

echo "Setting up GitHub token and running analysis..."

# Check if a GitHub token was provided
if [ -z "$1" ]; then
    echo "Error: No GitHub token provided."
    echo "Usage: ./set_github_token.sh your_github_token_here"
    exit 1
fi

# Set the GITHUB_TOKEN environment variable for the current session
export GITHUB_TOKEN="$1"
echo "Set GITHUB_TOKEN environment variable for current session."

# Run the analysis
./analyze_trending_java.sh

echo ""
echo "To set the GITHUB_TOKEN permanently, add the following line to your shell profile:"
echo "export GITHUB_TOKEN=$1"
echo ""
echo "For bash users:"
echo "echo 'export GITHUB_TOKEN=$1' >> ~/.bashrc"
echo "source ~/.bashrc"
echo ""
echo "For zsh users:"
echo "echo 'export GITHUB_TOKEN=$1' >> ~/.zshrc"
echo "source ~/.zshrc"
