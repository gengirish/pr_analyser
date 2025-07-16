#!/bin/bash
# Set Permanent GitHub Token for Unix/Linux/Mac
# This shell script sets the GITHUB_TOKEN environment variable permanently in the user's shell profile

echo "Setting up permanent GitHub token for Unix/Linux/Mac..."

# Check if a GitHub token was provided
if [ -z "$1" ]; then
    echo "Error: No GitHub token provided."
    echo "Usage: ./set_permanent_token_unix.sh your_github_token_here"
    exit 1
fi

# Detect shell type
SHELL_TYPE=$(basename "$SHELL")
PROFILE_FILE=""

case "$SHELL_TYPE" in
    "bash")
        PROFILE_FILE="$HOME/.bashrc"
        ;;
    "zsh")
        PROFILE_FILE="$HOME/.zshrc"
        ;;
    *)
        echo "Unsupported shell: $SHELL_TYPE"
        echo "Please manually add the following line to your shell profile:"
        echo "export GITHUB_TOKEN=$1"
        exit 1
        ;;
esac

# Check if token already exists in profile
if grep -q "export GITHUB_TOKEN=" "$PROFILE_FILE"; then
    # Update existing token
    sed -i "s|export GITHUB_TOKEN=.*|export GITHUB_TOKEN=$1|" "$PROFILE_FILE"
    echo "Updated existing GITHUB_TOKEN in $PROFILE_FILE."
else
    # Add new token
    echo "" >> "$PROFILE_FILE"
    echo "# GitHub Personal Access Token for PR Analyzer" >> "$PROFILE_FILE"
    echo "export GITHUB_TOKEN=$1" >> "$PROFILE_FILE"
    echo "Added GITHUB_TOKEN to $PROFILE_FILE."
fi

# Set for current session as well
export GITHUB_TOKEN="$1"
echo "Set GITHUB_TOKEN for current session."
echo ""
echo "Important: For the permanent change to take effect in new terminals, run:"
echo "source $PROFILE_FILE"
echo ""
echo "To verify the token is set, run:"
echo "echo \$GITHUB_TOKEN"
