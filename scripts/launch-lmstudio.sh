#!/bin/bash
# Launch LM Studio CLI with AI hub context

cd "$HOME/Projects/ai/workspaces/lmstudio"
source "$HOME/Projects/ai/scripts/load-env.sh"

# LM Studio CLI
# Note: LM Studio is primarily a GUI app, but has CLI capabilities
echo "LM Studio launcher - workspace: $HOME/Projects/ai/workspaces/lmstudio"
echo "Config directory: ~/.lmstudio"
echo ""

# Check if lms CLI exists
if command -v lms &> /dev/null; then
    lms "$@"
else
    echo "LM Studio CLI (lms) not found. Opening GUI instead..."
    lmstudio "$@" 2>/dev/null &
fi
