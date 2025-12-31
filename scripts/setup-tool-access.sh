#!/bin/bash
# Setup filesystem access for AI tools with sandbox + broad access

set -e

AI_HUB="$HOME/Projects/ai"
CONFIGS_DIR="$AI_HUB/configs"
WORKSPACES_DIR="$AI_HUB/workspaces"

echo "Setting up AI Tools Hub..."

# Ensure directories exist
mkdir -p "$WORKSPACES_DIR"/{claude,crush,scratch}
mkdir -p "$AI_HUB/scripts"

# Set up symlinks for configs (optional - keeps tools pointing to central location)
setup_claude_config() {
    if [ -d "$HOME/.claude" ] && [ ! -L "$CONFIGS_DIR/.claude" ]; then
        echo "Linking Claude config to AI hub..."
        # Keep original in place, but add workspace pointer
        cat > "$HOME/.claude/settings.local.json" <<EOF
{
  "workingDirectory": "$WORKSPACES_DIR/claude",
  "allowGlobalFileAccess": true,
  "defaultContext": "$AI_HUB"
}
EOF
    fi
}

setup_crush_config() {
    if [ -d "$CONFIGS_DIR/.crush" ]; then
        echo "Setting up Crush workspace..."
        # Create crush workspace config
        mkdir -p "$WORKSPACES_DIR/crush"
    fi
}

# Source shared environment
create_env_loader() {
    cat > "$AI_HUB/scripts/load-env.sh" <<'EOF'
#!/bin/bash
# Source shared API keys for AI tools

if [ -f "$HOME/Projects/ai/configs/.env" ]; then
    export $(cat "$HOME/Projects/ai/configs/.env" | grep -v '^#' | xargs)
    echo "Loaded AI tool environment variables"
else
    echo "Warning: .env file not found at $HOME/Projects/ai/configs/.env"
fi
EOF
    chmod +x "$AI_HUB/scripts/load-env.sh"
}

# Create workspace launcher
create_launcher() {
    local tool=$1
    cat > "$AI_HUB/scripts/launch-$tool.sh" <<EOF
#!/bin/bash
# Launch $tool with AI hub context

cd "$WORKSPACES_DIR/$tool"
source "$AI_HUB/scripts/load-env.sh"

# Launch $tool with appropriate flags
case "$tool" in
    claude)
        claude --context "$AI_HUB" "\$@"
        ;;
    crush)
        crush --workspace "$WORKSPACES_DIR/crush" "\$@"
        ;;
    *)
        echo "Unknown tool: $tool"
        exit 1
        ;;
esac
EOF
    chmod +x "$AI_HUB/scripts/launch-$tool.sh"
    echo "Created launcher: $AI_HUB/scripts/launch-$tool.sh"
}

# Run setup
setup_claude_config
setup_crush_config
create_env_loader
create_launcher "claude"
create_launcher "crush"

# Create .gitignore for workspaces
cat > "$WORKSPACES_DIR/.gitignore" <<'EOF'
# Ignore all workspace contents
*

# But track the structure
!.gitignore
EOF

echo ""
echo "AI Tools Hub setup complete!"
echo ""
echo "Structure:"
echo "  Configs:    $CONFIGS_DIR"
echo "  Workspaces: $WORKSPACES_DIR"
echo "  Scripts:    $AI_HUB/scripts"
echo ""
echo "Usage:"
echo "  Launch Claude: $AI_HUB/scripts/launch-claude.sh"
echo "  Launch Crush:  $AI_HUB/scripts/launch-crush.sh"
echo "  Load env vars: source $AI_HUB/scripts/load-env.sh"
echo ""
echo "Filesystem Access:"
echo "  Tools can read/write to most of ~/Projects, ~/Documents, /tmp"
echo "  Workspace sandbox: $WORKSPACES_DIR/<tool>/"
echo ""
