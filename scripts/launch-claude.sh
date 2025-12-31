#!/bin/bash
# Launch Claude Code from AI Hub

cd "/home/yish/Projects/ai/workspaces/claude"
source "/home/yish/Projects/ai/scripts/load-env.sh"

# Launch Claude Code
# Note: Claude Code doesn't have --context flag, it uses the current directory
exec claude "$@"
