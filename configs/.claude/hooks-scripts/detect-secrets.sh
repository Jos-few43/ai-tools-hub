#!/bin/bash
# PreToolUse hook - Detect secrets before cloud transmission

TOOL_NAME="$1"
TOOL_PARAMS="$2"

# Only check cloud API calls
if [[ "$TOOL_NAME" =~ (gemini_research|codex_generate|grok_realtime) ]]; then
    # Check for common secret patterns
    if echo "$TOOL_PARAMS" | grep -qE "(sk-[a-zA-Z0-9]{32,}|xai-[a-zA-Z0-9]+|AIza[a-zA-Z0-9]{35})"; then
        echo "SECRET DETECTED - Blocking cloud transmission"
        echo "Use @ollama-codereview instead for local processing"
        exit 1  # Block the tool call
    fi

    # Check for credential keywords
    if echo "$TOOL_PARAMS" | grep -qiE "(password|secret|token|api.?key)"; then
        echo "Warning: Potential secret in prompt. Consider using @ollama-codereview"
    fi
fi

exit 0  # Allow the tool call
