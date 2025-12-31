#!/bin/bash
# Source shared API keys for AI tools

if [ -f "$HOME/Projects/ai/configs/.env" ]; then
    export $(cat "$HOME/Projects/ai/configs/.env" | grep -v '^#' | xargs)
    echo "Loaded AI tool environment variables"
else
    echo "Warning: .env file not found at $HOME/Projects/ai/configs/.env"
fi
