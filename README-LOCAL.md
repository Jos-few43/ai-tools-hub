# AI Tools Hub

Central configuration and workspace for AI CLI tools with filesystem access.

## Directory Structure

```
~/Projects/ai/
├── configs/               # Tool-specific configurations
│   ├── .claude/          # Claude Code configs
│   ├── .crush/           # Crush AI configs
│   ├── .gemini/          # Gemini configs
│   ├── .ollama/          # Ollama configs
│   ├── .lmstudio/        # LM Studio configs
│   ├── .qwen/            # Qwen configs
│   ├── .opencode/        # OpenCode configs
│   ├── .venv/            # Shared Python environment (CUDA libs)
│   ├── .env              # Shared API keys
│   └── CLAUDE.md         # Claude-specific notes
├── workspaces/           # Sandboxed work directories
│   ├── claude/           # Claude Code workspace
│   ├── crush/            # Crush workspace
│   ├── gemini/           # Gemini workspace
│   ├── ollama/           # Ollama workspace
│   ├── lmstudio/         # LM Studio workspace
│   ├── qwen/             # Qwen workspace
│   ├── opencode/         # OpenCode workspace
│   └── scratch/          # Temporary work
├── models/               # Shared AI models (13GB)
│   ├── checkpoints/      # SD checkpoints (13GB)
│   ├── loras/            # LoRA models
│   ├── vae/              # VAE models
│   └── embeddings/       # Textual inversion
├── stable-diffusion-webui/  # SD WebUI installation (9.3GB)
└── scripts/              # Automation & launcher scripts
    ├── setup-tool-access.sh
    ├── load-env.sh
    ├── launch-claude.sh
    ├── launch-crush.sh
    ├── launch-gemini.sh
    ├── launch-ollama.sh
    ├── launch-lmstudio.sh
    ├── launch-qwen.sh
    └── launch-opencode.sh
```

## Configuration Philosophy

**Sandbox with Filesystem Access:**
- Tools operate in dedicated workspaces under `~/Projects/ai/workspaces/`
- Full read/write access to most of the filesystem for troubleshooting
- Specific exclusions for safety (system files, other users)
- Auto-run capabilities for scripts and workflows

## Tool Configuration

### Claude Code
**Config Location:** `~/Projects/ai/configs/.claude/`
**Workspace:** `~/Projects/ai/workspaces/claude/`
**Settings:**
```json
{
  "workingDirectory": "/home/yish/Projects/ai/workspaces/claude",
  "allowedPaths": [
    "/home/yish/Projects",
    "/home/yish/Documents",
    "/home/yish/.config",
    "/tmp"
  ],
  "blockedPaths": [
    "/etc/shadow",
    "/etc/passwd",
    "/root"
  ]
}
```

### Crush
**Config Location:** `~/Projects/ai/configs/.crush/`
**Workspace:** `~/Projects/ai/workspaces/crush/`

### Gemini
**Config Location:** `~/Projects/ai/configs/.gemini/`
**Workspace:** `~/Projects/ai/workspaces/gemini/`
**Command:** `/usr/bin/gemini`

### Ollama
**Config Location:** `~/Projects/ai/configs/.ollama/`
**Workspace:** `~/Projects/ai/workspaces/ollama/`
**Command:** `/usr/bin/ollama`
**Models:** Stored in `~/.ollama/models` (20GB)

### LM Studio
**Config Location:** `~/Projects/ai/configs/.lmstudio/`
**Workspace:** `~/Projects/ai/workspaces/lmstudio/`
**Original Config:** `~/.lmstudio/`

### Qwen
**Config Location:** `~/Projects/ai/configs/.qwen/`
**Workspace:** `~/Projects/ai/workspaces/qwen/`
**Original Config:** `~/.qwen/`

### OpenCode
**Config Location:** `~/Projects/ai/configs/.opencode/`
**Workspace:** `~/Projects/ai/workspaces/opencode/`
**Original Config:** `~/.opencode/`

### Shared Resources
**Python Environment:** `~/Projects/ai/configs/.venv/`
- CUDA libraries for GPU acceleration
- Shared across all Python-based AI tools
- 9.2GB (NVIDIA CUDA libs)

**API Keys:** `~/Projects/ai/configs/.env`
- Gemini, Anthropic, OpenAI, X.AI, DeepSeek, DashScope
- Source this file in tool configs

## Filesystem Access Rules

### Read Access (Full)
- `/home/yish/` (all user files)
- `/tmp/` (temporary files)
- `/opt/` (optional software)

### Write Access (Controlled)
- `~/Projects/ai/workspaces/<tool>/` (primary workspace)
- `~/Projects/` (for project modifications)
- `~/Documents/` (for documentation)
- `/tmp/` (temporary files)

### Blocked
- `/etc/shadow`, `/etc/passwd` (system auth)
- `/root/` (root user home)
- `/sys/`, `/proc/` (kernel interfaces)
- Other user home directories

## Quick Launch Commands

All tools can be launched using their respective launcher scripts:

```bash
# Claude Code
~/Projects/ai/scripts/launch-claude.sh

# Crush AI
~/Projects/ai/scripts/launch-crush.sh

# Gemini
~/Projects/ai/scripts/launch-gemini.sh

# Ollama
~/Projects/ai/scripts/launch-ollama.sh
~/Projects/ai/scripts/launch-ollama.sh run llama2  # Interactive chat
~/Projects/ai/scripts/launch-ollama.sh list        # List installed models

# LM Studio
~/Projects/ai/scripts/launch-lmstudio.sh

# Qwen
~/Projects/ai/scripts/launch-qwen.sh

# OpenCode
~/Projects/ai/scripts/launch-opencode.sh
```

## Manual Usage Examples

### Claude Code
```bash
# Start Claude with AI hub context
cd ~/Projects/ai/workspaces/claude
source ~/Projects/ai/scripts/load-env.sh
claude --context ~/Projects/ai
```

### Crush
```bash
# Start Crush with shared config
cd ~/Projects/ai/workspaces/crush
source ~/Projects/ai/scripts/load-env.sh
crush --config ~/Projects/ai/configs/.crush/config.json
```

### Ollama
```bash
# Start Ollama in workspace
cd ~/Projects/ai/workspaces/ollama
source ~/Projects/ai/scripts/load-env.sh
ollama run deepseek-coder  # Use any installed model
```

### Gemini
```bash
# Start Gemini CLI
cd ~/Projects/ai/workspaces/gemini
source ~/Projects/ai/scripts/load-env.sh
gemini
```

## TUI Management Console

**Quick Start:**
```bash
# Launch the interactive TUI
~/Projects/ai/ai-hub
```

**Features:**
- 📊 Real-time system hardware monitoring (CPU, RAM, GPU, VRAM, Disk)
- 🛠️ Tool status dashboard (7 AI tools tracked)
- 📦 Model management with requirements checking
- 💾 Storage breakdown and analysis
- 🚀 Interactive tool launcher
- ⚠️ Pre-download hardware verification (prevents downloading incompatible models)

**See detailed guide:** [TUI-GUIDE.md](TUI-GUIDE.md)

## Benefits

1. **Centralized Configuration:** All AI tools share API keys and base configs
2. **Workspace Isolation:** Each tool has its own sandbox
3. **Filesystem Access:** Tools can troubleshoot and modify files across your system
4. **Auto-Run Capability:** Scripts can execute in workspaces with full context
5. **Easy Cleanup:** Clear separation of tool data
6. **Hardware Verification:** Check system requirements before downloading models
7. **Visual Management:** Beautiful TUI for monitoring and control

## Maintenance

### Clean Workspaces
```bash
# Remove temporary files from all workspaces
find ~/Projects/ai/workspaces -name "*.tmp" -delete
```

### Update API Keys
```bash
# Edit shared environment
nano ~/Projects/ai/configs/.env
```

### Rebuild Python Environment
```bash
cd ~/Projects/ai/configs
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

**Last Updated:** 2025-12-31
