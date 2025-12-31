#!/bin/bash
# Launch OpenCode with AI hub context

cd "$HOME/Projects/ai/workspaces/opencode"
source "$HOME/Projects/ai/scripts/load-env.sh"

# OpenCode CLI
echo "OpenCode launcher - workspace: $HOME/Projects/ai/workspaces/opencode"
echo "Config directory: ~/.opencode"
echo ""

# Check if opencode CLI exists
if [ -x "$HOME/.opencode/bin/opencode" ]; then
    "$HOME/.opencode/bin/opencode" "$@"
elif command -v opencode &> /dev/null; then
    opencode "$@"
else
    echo "OpenCode CLI not found"
    echo "Install from: https://github.com/yourorg/opencode"
    exit 1
fi
