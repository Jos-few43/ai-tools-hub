#!/bin/bash
# Launch Ollama with AI hub context

cd "$HOME/Projects/ai/workspaces/ollama"
source "$HOME/Projects/ai/scripts/load-env.sh"

# Ollama CLI
# For interactive chat: ollama run <model>
# For API server: ollama serve
echo "Ollama launcher - workspace: $HOME/Projects/ai/workspaces/ollama"
echo "Usage:"
echo "  Interactive: ollama run llama2"
echo "  API server:  ollama serve"
echo "  List models: ollama list"
echo ""
ollama "$@"
