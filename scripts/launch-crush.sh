#!/bin/bash
# Launch Crush from AI Hub

cd "/home/yish/Projects/ai/workspaces/crush"
source "/home/yish/Projects/ai/scripts/load-env.sh"

# Launch Crush
exec crush "$@"
