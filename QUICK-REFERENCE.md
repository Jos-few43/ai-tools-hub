# AI Hub - Quick Reference

## 🚀 Launch Commands

```bash
# TUI Management Console (Recommended)
~/Projects/ai/ai-hub

# Individual Tools
~/Projects/ai/scripts/launch-claude.sh
~/Projects/ai/scripts/launch-crush.sh
~/Projects/ai/scripts/launch-gemini.sh
~/Projects/ai/scripts/launch-ollama.sh run llama2
~/Projects/ai/scripts/launch-lmstudio.sh
~/Projects/ai/scripts/launch-qwen.sh
~/Projects/ai/scripts/launch-opencode.sh
~/Projects/ai/scripts/launch-sd-webui.sh

# Status Check
~/Projects/ai/scripts/ai-hub-status.sh
```

## 📁 Directory Structure

```
~/Projects/ai/                    (31GB)
├── ai-hub                        # TUI launcher
├── configs/                      # Tool configs
│   ├── .venv/                   # 9.2GB CUDA Python
│   └── .env                     # API keys
├── workspaces/                   # Tool workspaces
│   ├── claude/
│   ├── ollama/
│   └── ...
├── models/                       # Shared AI models (13GB)
│   └── checkpoints/             # SD checkpoints
├── stable-diffusion-webui/      # 9.3GB
└── scripts/                      # Launchers & tools
```

## 🛠️ TUI Quick Menu

```
Main Menu:
  [1] System Information      - CPU, RAM, GPU, VRAM stats
  [2] Tool Status            - Installation & workspace status
  [3] Model Management       - View, check, cleanup models
  [4] Storage Breakdown      - Disk usage analysis
  [5] Launch Tool            - Interactive launcher
  [0] Exit
```

## 📦 Model Requirements

| Model | RAM | VRAM | Disk |
|-------|-----|------|------|
| FLUX Dev | 16GB | 12GB | 24GB |
| SDXL | 16GB | 8GB | 7GB |
| SD 1.5 | 8GB | 4GB | 4GB |

**Your System:**
- RAM: 10GB available
- GPU: RTX 3060 (6GB VRAM)
- Disk: 100GB free

## 💾 Storage Locations

```bash
# Models
~/Projects/ai/models/checkpoints/

# ComfyUI (symlinked to shared models)
~/Projects/comfy/ComfyUI/models/checkpoints-link

# SD-WebUI (symlinked to shared models)
~/Projects/ai/stable-diffusion-webui/models/Stable-diffusion-shared

# API Keys
~/Projects/ai/configs/.env
```

## ⚡ Quick Tasks

### Check system specs before downloading
```bash
~/Projects/ai/ai-hub
# → [3] Model Management → [2] Check requirements
```

### View all installed tools
```bash
~/Projects/ai/ai-hub
# → [2] Tool Status
```

### Clean up old models
```bash
~/Projects/ai/ai-hub
# → [3] Model Management → [4] Clean up old models
```

### Check storage usage
```bash
~/Projects/ai/ai-hub
# → [4] Storage Breakdown
```

### Launch Ollama with model
```bash
~/Projects/ai/scripts/launch-ollama.sh run deepseek-coder
```

## 🔧 Maintenance

```bash
# Load API keys
source ~/Projects/ai/scripts/load-env.sh

# Check hub status
~/Projects/ai/scripts/ai-hub-status.sh

# Update hub setup
~/Projects/ai/scripts/setup-tool-access.sh
```

## 📊 Current Stats

- **Total Space:** 90.1GB cleaned, 31GB in use
- **Tools:** 7 AI tools configured
- **Models:** 3 SD checkpoints (13GB)
- **Workspaces:** 8 isolated environments

## 🎯 Installed Tools

✓ Claude Code
✓ Crush
✓ Gemini
✓ Ollama
✓ LM Studio
✓ Qwen
✓ OpenCode
✓ SD WebUI

## 📖 Documentation

- Full guide: `~/Projects/ai/README.md`
- TUI guide: `~/Projects/ai/TUI-GUIDE.md`
- Model info: `~/Projects/ai/models/README.md`

---

## 🔥 Bash Aliases (Already Added!)

The following aliases have been added to your `~/.bashrc`:

```bash
# Main TUI launcher
ai                    # Launch AI Hub TUI

# Quick commands
ai-status            # Show tool status (non-interactive)
ai-models            # List all checkpoint models
ai-env               # Load API keys into environment
```

**Usage examples:**
```bash
# Open TUI
ai

# Quick status check
ai-status

# View models
ai-models

# Load environment for manual tool launch
ai-env
ollama run deepseek-coder
```

**To activate in current session:**
```bash
source ~/.bashrc
```

**Then just type:**
```bash
ai  # That's it!
```
