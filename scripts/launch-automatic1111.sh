#!/bin/bash
# Launch Stable Diffusion WebUI with AI hub context

cd "$HOME/Projects/ai/stable-diffusion-webui"
source "$HOME/Projects/ai/scripts/load-env.sh"

echo "═══════════════════════════════════════════════════════"
echo "    Stable Diffusion WebUI Launcher"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Location: $HOME/Projects/ai/stable-diffusion-webui"
echo "Shared models: $HOME/Projects/ai/models/checkpoints"
echo ""
echo "Starting SD WebUI..."
echo ""

# Launch SD WebUI
./webui.sh "$@"
