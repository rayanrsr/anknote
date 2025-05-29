#!/bin/bash

# Setup git configuration for conventional commits
echo "Setting up git configuration for conventional commits..."

# Set the commit message template
git config commit.template .gitmessage

echo "✅ Git commit template configured!"
echo "Now when you run 'git commit', you'll see the conventional commit template."
echo ""
echo "Example usage:"
echo "  git commit -m 'feat: add new feature'"
echo "  git commit -m 'fix: resolve bug in authentication'"
echo "  git commit -m 'docs: update README'"
