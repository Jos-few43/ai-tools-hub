#!/bin/bash
# Display AI Hub status and available tools

AI_HUB="$HOME/Projects/ai"

echo "═══════════════════════════════════════════════════════"
echo "           AI TOOLS HUB STATUS"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "Location: $AI_HUB"
echo "Size: $(du -sh $AI_HUB 2>/dev/null | cut -f1)"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "INSTALLED TOOLS"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

check_tool() {
    local name=$1
    local cmd=$2
    local workspace="$AI_HUB/workspaces/$name"
    local launcher="$AI_HUB/scripts/launch-$name.sh"

    echo -n "[$name] "

    if command -v "$cmd" &>/dev/null; then
        echo -n "✓ Installed"
        [ -d "$workspace" ] && echo -n " | Workspace: ✓"
        [ -x "$launcher" ] && echo -n " | Launcher: ✓"
        echo ""
    else
        echo "✗ Not installed"
    fi
}

check_tool "claude" "claude"
check_tool "crush" "crush"
check_tool "gemini" "gemini"
check_tool "ollama" "ollama"
check_tool "lmstudio" "lmstudio"
check_tool "qwen" "qwen"
check_tool "opencode" "opencode"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "WORKSPACES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
for workspace in "$AI_HUB/workspaces"/*/ ; do
    name=$(basename "$workspace")
    size=$(du -sh "$workspace" 2>/dev/null | cut -f1)
    echo "  $name: $size"
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "SHARED RESOURCES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f "$AI_HUB/configs/.env" ]; then
    echo "  API Keys: ✓ ($AI_HUB/configs/.env)"
    grep -c "API_KEY" "$AI_HUB/configs/.env" 2>/dev/null | xargs -I {} echo "    {} API keys configured"
else
    echo "  API Keys: ✗ Not found"
fi

if [ -d "$AI_HUB/configs/.venv" ]; then
    venv_size=$(du -sh "$AI_HUB/configs/.venv" 2>/dev/null | cut -f1)
    echo "  Python venv: ✓ ($venv_size)"
else
    echo "  Python venv: ✗ Not found"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "QUICK LAUNCH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ~/Projects/ai/scripts/launch-<tool>.sh"
echo ""
echo "Available launchers:"
ls -1 "$AI_HUB/scripts"/launch-*.sh 2>/dev/null | xargs -n1 basename | sed 's/^/  - /'
echo ""
echo "═══════════════════════════════════════════════════════"
