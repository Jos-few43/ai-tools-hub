#!/bin/bash
# Launch Gemini CLI with AI hub context

cd "$HOME/Projects/ai/workspaces/gemini"
source "$HOME/Projects/ai/scripts/load-env.sh"

# Gemini CLI with workspace context
gemini --workspace "$HOME/Projects/ai/workspaces/gemini" "$@"
