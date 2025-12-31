#!/bin/bash
# SessionStart hook - Display system status

echo "Multi-AI Research Team Status"
echo "================================"

# Check Ollama GPU
if ollama list > /dev/null 2>&1; then
    echo "Ollama (Local GPU): Running"
    echo "  Models: $(ollama list | tail -n +2 | wc -l)"
else
    echo "Ollama: Not running"
fi

# Check MCP Server
if ps aux | grep -v grep | grep "multi-ai-coordinator" > /dev/null; then
    echo "MCP Server: Active"
else
    echo "MCP Server: Not detected"
fi

# Check API Keys
[[ -n "$GEMINI_API_KEY" ]] && echo "Gemini API: Configured" || echo "Gemini API: Missing"
[[ -n "$OPENAI_API_KEY" ]] && echo "OpenAI API: Configured" || echo "OpenAI API: Missing"
[[ -n "$XAI_API_KEY" ]] && echo "X.AI API: Configured" || echo "X.AI API: Missing"

# GPU Status
if nvidia-smi > /dev/null 2>&1; then
    GPU_MEM=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -1)
    echo "GPU (RTX 3060): ${GPU_MEM}MB free"
else
    echo "GPU: Not accessible"
fi

echo ""
echo "Available Agents: @gemini-research @ollama-codereview @codex-generator @grok-realtime"
echo "Quick Commands: /agent-status /deep-research /private-review"
