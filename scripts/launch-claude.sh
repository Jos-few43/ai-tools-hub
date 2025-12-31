#!/bin/bash
# Launch claude with AI hub context

cd "/home/yish/Projects/ai/workspaces/claude"
source "/home/yish/Projects/ai/scripts/load-env.sh"

# Launch claude with appropriate flags
case "claude" in
    claude)
        claude --context "/home/yish/Projects/ai" "$@"
        ;;
    crush)
        crush --workspace "/home/yish/Projects/ai/workspaces/crush" "$@"
        ;;
    *)
        echo "Unknown tool: claude"
        exit 1
        ;;
esac
