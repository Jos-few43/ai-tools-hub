#!/bin/bash
# Stop hook - Generate session summary

LOG_FILE="/home/yish/Projects/claude-workspace/.claude/logs/audit.jsonl"

if [[ -f "$LOG_FILE" ]]; then
    echo ""
    echo "Session Summary"
    echo "================="

    # Count agent calls
    TOTAL_CALLS=$(wc -l < "$LOG_FILE")
    echo "Total agent calls: $TOTAL_CALLS"

    # Privacy breakdown
    LOCAL_CALLS=$(grep -c '"privacy":"local"' "$LOG_FILE")
    CLOUD_CALLS=$(grep -c '"privacy":"cloud"' "$LOG_FILE")
    echo "Privacy: ${LOCAL_CALLS} local, ${CLOUD_CALLS} cloud"

    # Total cost estimate
    if command -v jq > /dev/null; then
        TOTAL_COST=$(jq -s 'map(.cost) | add' "$LOG_FILE" 2>/dev/null || echo "0")
        echo "Estimated cost: \$${TOTAL_COST}"
    else
        echo "Estimated cost: (install jq for cost tracking)"
    fi
fi
