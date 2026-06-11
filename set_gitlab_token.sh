#!/bin/bash
# Script to set GitLab Personal Access Token as an environment variable
# This sets the token for the current session only

echo "GitLab Token Setup"
echo "=================="
echo ""
echo "This script will set your GitLab Personal Access Token as an environment variable"
echo "for the current session. You'll need to run this each time you open a new terminal."
echo ""
echo "To create a GitLab Personal Access Token:"
echo "1. Go to https://gitlab.com/-/profile/personal_access_tokens"
echo "2. Click 'Add new token'"
echo "3. Give it a name (e.g., 'MR Analyzer')"
echo "4. Select scopes: read_api, read_repository"
echo "5. Click 'Create personal access token'"
echo "6. Copy the token (you won't see it again!)"
echo ""

read -p "Enter your GitLab Personal Access Token: " GITLAB_TOKEN

if [ -z "$GITLAB_TOKEN" ]; then
    echo ""
    echo "Error: No token provided."
    exit 1
fi

# Export the environment variable for the current session
export GITLAB_TOKEN="$GITLAB_TOKEN"

echo ""
echo "Success! GitLab token has been set for this session."
echo ""
echo "You can now use the analyzer without the --token parameter:"
echo "  python3 gitlab_mr_analyzer.py mycomplianceoffice/mco"
echo ""
echo "Note: This token is only available in this terminal session."
echo "For permanent setup, add this line to your ~/.bashrc or ~/.zshrc:"
echo "  export GITLAB_TOKEN='your-token-here'"
echo ""
