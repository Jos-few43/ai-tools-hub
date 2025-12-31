#!/bin/bash
# Launch Qwen CLI with AI hub context

cd "$HOME/Projects/ai/workspaces/qwen"
source "$HOME/Projects/ai/scripts/load-env.sh"

# Qwen CLI
echo "Qwen launcher - workspace: $HOME/Projects/ai/workspaces/qwen"
echo "Config directory: ~/.qwen"
echo ""

# Check if qwen CLI exists
if command -v qwen &> /dev/null; then
    qwen "$@"
else
    echo "Qwen CLI not found in PATH"
    echo "Install with: pip install qwen-cli"
    exit 1
fi
