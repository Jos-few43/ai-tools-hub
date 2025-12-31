#!/bin/bash
# Launch Gemini CLI from AI Hub

cd "$HOME/Projects/ai/workspaces/gemini"
source "$HOME/Projects/ai/scripts/load-env.sh"

# Launch Gemini CLI
exec gemini "$@"
