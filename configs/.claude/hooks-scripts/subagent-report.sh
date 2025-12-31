#!/bin/bash
# SubagentStop hook - Log agent activity

AGENT_NAME="$1"
DURATION="$2"
TOKENS_USED="$3"

# Determine if cloud or local
if [[ "$AGENT_NAME" =~ ollama ]]; then
    PRIVACY="local"
    COST=0
else
    PRIVACY="cloud"
    # Estimate cost (rough approximation)
    COST=$(echo "scale=4; $TOKENS_USED * 0.000002" | bc 2>/dev/null || echo "0.0000")
fi

# Append to audit log
LOG_DIR="/home/yish/Projects/claude-workspace/.claude/logs"
mkdir -p "$LOG_DIR"

echo "{\"timestamp\":\"$(date -Iseconds)\",\"agent\":\"$AGENT_NAME\",\"duration\":$DURATION,\"tokens\":$TOKENS_USED,\"privacy\":\"$PRIVACY\",\"cost\":$COST}" >> "$LOG_DIR/audit.jsonl"

echo "Agent completed: $AGENT_NAME ($PRIVACY, ~\$${COST})"
