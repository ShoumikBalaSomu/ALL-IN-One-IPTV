#!/bin/bash
# ALL-IN-One-IPTV — Push to GitHub
# Stage, commit, and push all changes

set -e

REPO_URL="git@github.com:ShoumikBalaSomu/ALL-IN-One-IPTV.git"
HTTPS_URL="https://github.com/ShoumikBalaSomu/ALL-IN-One-IPTV.git"

echo "🚀 ALL-IN-One-IPTV — Push to GitHub"
echo "===================================="

# Check if git repo
if [ ! -d ".git" ]; then
    echo "Not a git repository. Initializing..."
    git init
    git remote add origin $HTTPS_URL
fi

# Check remote
if ! git remote get-url origin &>/dev/null; then
    git remote add origin $HTTPS_URL 2>/dev/null || true
fi

# Stage changes
echo "📦 Staging changes..."
git add -A

# Get status
CHANGES=$(git status --short | wc -l)
if [ "$CHANGES" -eq 0 ]; then
    echo "No changes to commit."
    exit 0
fi

echo "📝 $CHANGES file(s) changed"

# Commit message
if [ -n "$1" ]; then
    MSG="$1"
else
    MSG="Auto-update: $(date +%Y-%m-%d_%H-%M)"
fi

# Commit
echo "💾 Committing: $MSG"
git commit -m "$MSG" || echo "Nothing to commit"

# Push
echo "📤 Pushing to GitHub..."
git push origin main 2>/dev/null || git push origin master 2>/dev/null || {
    echo "⚠ Push failed. Make sure you have write access."
    echo "Manual push command:"
    echo "  git push origin main"
}

echo ""
echo "✅ Done!"