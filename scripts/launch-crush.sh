#!/bin/bash
# Launch crush with AI hub context

cd "/home/yish/Projects/ai/workspaces/crush"
source "/home/yish/Projects/ai/scripts/load-env.sh"

# Launch crush with appropriate flags
case "crush" in
    claude)
        claude --context "/home/yish/Projects/ai" "$@"
        ;;
    crush)
        crush --workspace "/home/yish/Projects/ai/workspaces/crush" "$@"
        ;;
    *)
        echo "Unknown tool: crush"
        exit 1
        ;;
esac
