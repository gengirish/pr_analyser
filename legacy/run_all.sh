#!/bin/bash
# Run All Steps
# This shell script sets the GitHub token, verifies it, and runs the analysis for any language

echo "GitHub PR Analyzer - Complete Workflow"
echo "====================================="
echo ""

# Usage info
if [ -z "$1" ]; then
    echo "Error: No GitHub token provided."
    echo "Usage: ./run_all.sh your_github_token_here [language] [limit]"
    exit 1
fi

TOKEN="$1"
LANGUAGE="java"
LIMIT="20"

if [ ! -z "$2" ]; then
    LANGUAGE="$2"
fi

if [ ! -z "$3" ]; then
    LIMIT="$3"
fi

# Step 1: Set the GitHub token for the current session
echo "Step 1: Setting GitHub token..."
export GITHUB_TOKEN="$TOKEN"
echo "Set GITHUB_TOKEN environment variable for current session."
echo ""

# Step 2: Verify the token
echo "Step 2: Verifying GitHub token..."
./check_token.sh
if [ $? -ne 0 ]; then
    echo "Token verification failed. Please check your token and try again."
    exit 1
fi
echo ""

# Step 3: Run the analysis
echo "Step 3: Running analysis on trending $LANGUAGE projects..."
./analyze_trending_java.sh "$TOKEN" "$LANGUAGE" "$LIMIT"
echo ""

echo "All steps completed successfully!"
echo ""
echo "To set the token permanently, run:"
echo "./set_permanent_token_unix.sh $TOKEN"
