#!/bin/bash
# AI Tools Hub - Installation Script
# Apache License 2.0

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
AI_HUB_DIR="$HOME/Projects/ai"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo -e "${CYAN}   AI Tools Hub - Installation${NC}"
echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo ""

# Check if running from the correct directory
if [ "$INSTALL_DIR" != "$AI_HUB_DIR" ]; then
    echo -e "${YELLOW}Warning: Installing from $INSTALL_DIR${NC}"
    echo -e "${YELLOW}Expected location: $AI_HUB_DIR${NC}"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    AI_HUB_DIR="$INSTALL_DIR"
fi

echo -e "${GREEN}[1/8] Checking system requirements...${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
    echo -e "${RED}Error: Python 3.10+ required (found $PYTHON_VERSION)${NC}"
    exit 1
fi

echo -e "${GREEN}  ✓ Python $PYTHON_VERSION${NC}"

# Check for rich library
if python3 -c "import rich" 2>/dev/null; then
    echo -e "${GREEN}  ✓ python-rich installed${NC}"
else
    echo -e "${YELLOW}  Installing python-rich...${NC}"
    if command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python-rich || pip install --user rich
    elif command -v apt-get &> /dev/null; then
        sudo apt-get install -y python3-rich || pip install --user rich
    else
        pip install --user rich
    fi
    echo -e "${GREEN}  ✓ python-rich installed${NC}"
fi

echo ""
echo -e "${GREEN}[2/8] Creating directory structure...${NC}"

# Create main directories
mkdir -p "$AI_HUB_DIR"/{configs,workspaces,models,scripts}

# Create config subdirectories
mkdir -p "$AI_HUB_DIR"/configs/{.claude,.crush,.gemini,.ollama,.lmstudio,.qwen,.opencode}

# Create workspace subdirectories
mkdir -p "$AI_HUB_DIR"/workspaces/{claude,crush,gemini,ollama,lmstudio,qwen,opencode,scratch}

# Create model subdirectories
mkdir -p "$AI_HUB_DIR"/models/{checkpoints,loras,vae,embeddings}

# Create .gitkeep files
touch "$AI_HUB_DIR"/workspaces/.gitkeep
touch "$AI_HUB_DIR"/models/{checkpoints,loras,vae,embeddings}/.gitkeep

echo -e "${GREEN}  ✓ Directory structure created${NC}"

echo ""
echo -e "${GREEN}[3/8] Setting up configuration files...${NC}"

# Create .env from template if it doesn't exist
if [ ! -f "$AI_HUB_DIR/configs/.env" ]; then
    if [ -f "$AI_HUB_DIR/configs/.env.example" ]; then
        cp "$AI_HUB_DIR/configs/.env.example" "$AI_HUB_DIR/configs/.env"
        echo -e "${GREEN}  ✓ Created .env from template${NC}"
    else
        cat > "$AI_HUB_DIR/configs/.env" <<'EOF'
# AI Tools Hub - API Keys Configuration
# Add your API keys below

GEMINI_API_KEY=""
ANTHROPIC_API_KEY=""
OPENAI_API_KEY=""
XAI_API_KEY=""
DEEPSEEK_API_KEY=""
DASHSCOPE_API_KEY=""
EOF
        echo -e "${GREEN}  ✓ Created default .env template${NC}"
    fi
    echo -e "${YELLOW}  → Edit $AI_HUB_DIR/configs/.env to add your API keys${NC}"
else
    echo -e "${GREEN}  ✓ .env file already exists${NC}"
fi

echo ""
echo -e "${GREEN}[4/8] Making scripts executable...${NC}"

chmod +x "$AI_HUB_DIR"/ai-hub
chmod +x "$AI_HUB_DIR"/scripts/*.sh 2>/dev/null || true
chmod +x "$AI_HUB_DIR"/scripts/*.py 2>/dev/null || true

echo -e "${GREEN}  ✓ Scripts are now executable${NC}"

echo ""
echo -e "${GREEN}[5/8] Setting up bash aliases...${NC}"

# Check if aliases already exist
if grep -q "alias ai=" ~/.bashrc 2>/dev/null; then
    echo -e "${YELLOW}  → Aliases already exist in ~/.bashrc${NC}"
else
    cat >> ~/.bashrc <<EOF

# AI Tools Hub aliases
alias ai='$AI_HUB_DIR/ai-hub'
alias ai-status='$AI_HUB_DIR/scripts/ai-hub-status.sh'
alias ai-models='ls -lh $AI_HUB_DIR/models/checkpoints/'
alias ai-env='source $AI_HUB_DIR/scripts/load-env.sh'
EOF
    echo -e "${GREEN}  ✓ Added aliases to ~/.bashrc${NC}"
fi

echo ""
echo -e "${GREEN}[6/8] Checking for AI tools...${NC}"

# Check which tools are installed
tools_found=0
declare -A TOOLS=(
    ["claude"]="Claude Code"
    ["ollama"]="Ollama"
    ["gemini"]="Gemini"
    ["crush"]="Crush"
)

for cmd in "${!TOOLS[@]}"; do
    if command -v "$cmd" &> /dev/null; then
        echo -e "${GREEN}  ✓ ${TOOLS[$cmd]}${NC}"
        ((tools_found++))
    else
        echo -e "${YELLOW}  - ${TOOLS[$cmd]} (not installed)${NC}"
    fi
done

if [ $tools_found -eq 0 ]; then
    echo -e "${YELLOW}  → No AI tools detected. Install tools separately.${NC}"
fi

echo ""
echo -e "${GREEN}[7/8] Running setup script...${NC}"

if [ -f "$AI_HUB_DIR/scripts/setup-tool-access.sh" ]; then
    bash "$AI_HUB_DIR/scripts/setup-tool-access.sh"
else
    echo -e "${YELLOW}  → setup-tool-access.sh not found, skipping${NC}"
fi

echo ""
echo -e "${GREEN}[8/8] Finalizing installation...${NC}"

# Create a summary file
cat > "$AI_HUB_DIR/INSTALL_INFO.txt" <<EOF
AI Tools Hub Installation Summary
==================================

Installation Date: $(date)
Install Location: $AI_HUB_DIR
Python Version: $PYTHON_VERSION
Tools Found: $tools_found

Next Steps:
1. Add your API keys to: $AI_HUB_DIR/configs/.env
2. Activate aliases: source ~/.bashrc
3. Launch TUI: ai
4. Install AI tools if not already installed

Documentation:
- Getting Started: $AI_HUB_DIR/GETTING-STARTED.md
- TUI Guide: $AI_HUB_DIR/TUI-GUIDE.md
- Quick Reference: $AI_HUB_DIR/QUICK-REFERENCE.md

For help: https://github.com/yourusername/ai-tools-hub
EOF

echo -e "${GREEN}  ✓ Installation complete!${NC}"

echo ""
echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo -e "${CYAN}   Installation Complete! ${NC}"
echo -e "${CYAN}══════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}✓ AI Tools Hub installed to: $AI_HUB_DIR${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo -e "  1. Add API keys: nano $AI_HUB_DIR/configs/.env"
echo -e "  2. Activate aliases: ${CYAN}source ~/.bashrc${NC}"
echo -e "  3. Launch TUI: ${CYAN}ai${NC}"
echo ""
echo -e "${YELLOW}Documentation:${NC}"
echo -e "  - Getting Started: cat $AI_HUB_DIR/GETTING-STARTED.md"
echo -e "  - TUI Guide: cat $AI_HUB_DIR/TUI-GUIDE.md"
echo ""
echo -e "${GREEN}Happy AI Tool Managing! 🤖${NC}"
echo ""
