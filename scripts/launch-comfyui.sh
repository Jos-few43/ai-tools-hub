#!/bin/bash
# Launch ComfyUI from AI Hub

cd "/home/yish/Projects/comfy/ComfyUI"
source "/home/yish/Projects/ai/scripts/load-env.sh"

# Launch ComfyUI
exec python main.py "$@"
