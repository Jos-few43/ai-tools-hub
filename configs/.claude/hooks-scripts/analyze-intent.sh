#!/bin/bash
# UserPromptSubmit hook - Suggest relevant agents

PROMPT="$1"

# Simple keyword matching
if echo "$PROMPT" | grep -qiE "(research|search|find|what is|explain|fact)"; then
    echo "Suggestion: Try @gemini-research for deep research"
fi

if echo "$PROMPT" | grep -qiE "(review|audit|check|security|private|proprietary)"; then
    echo "Suggestion: Try @ollama-codereview for local code review"
fi

if echo "$PROMPT" | grep -qiE "(generate|create|scaffold|boilerplate|implement)"; then
    echo "Suggestion: Try @codex-generator for code generation"
fi

if echo "$PROMPT" | grep -qiE "(real-time|current|now|status|trending|twitter|x\.com)"; then
    echo "Suggestion: Try @grok-realtime for real-time info"
fi
