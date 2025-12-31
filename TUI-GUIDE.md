# AI Hub TUI - User Guide

Beautiful terminal interface for managing your AI Tools Hub.

## Quick Start

```bash
# From anywhere
~/Projects/ai/ai-hub

# Or from AI hub directory
cd ~/Projects/ai
./ai-hub
```

## Features

### 📊 System Information (Menu Option 1)

Real-time hardware specifications:
- **CPU:** Model and core count
- **RAM:** Total, available, and usage percentage
- **GPU:** NVIDIA GPU detection with VRAM
- **Disk:** Free space on AI hub volume

**Color-coded status indicators:**
- ✓ Green: Good (RAM >8GB, VRAM >8GB, Disk >50GB)
- ⚠ Yellow: Limited/Low
- ❌ Red: Not available/Critical

### 🛠️ Tool Status (Menu Option 2)

Overview of all installed AI tools:
- Installation status (✓ installed / ✗ not installed)
- Launcher script availability
- Workspace directory status
- Workspace storage usage

**Supported tools:**
- Claude Code
- Crush
- Gemini
- Ollama
- LM Studio
- Qwen
- OpenCode

### 📦 Model Management (Menu Option 3)

#### View Model Details
- List all Stable Diffusion checkpoints
- Size and type information (SDXL, SD 1.5, etc.)
- Total model count and storage

#### Check Requirements for New Model
Pre-download hardware verification:

**Supported model types:**
1. FLUX Dev (16GB RAM, 12GB VRAM, 24GB disk)
2. FLUX Schnell (16GB RAM, 12GB VRAM, 24GB disk)
3. SDXL (16GB RAM, 8GB VRAM, 7GB disk)
4. SD 1.5 (8GB RAM, 4GB VRAM, 4GB disk)
5. SD 2.1 (8GB RAM, 6GB VRAM, 5GB disk)

**System will check:**
- Available RAM vs. required
- GPU VRAM vs. required
- Free disk space vs. required

**Output:**
- ✓ Green: System meets all requirements
- ✗ Red: Missing requirements with detailed list of issues

#### Consolidate Duplicate Models
- Scan for duplicate models across tools
- Currently shows consolidation status

#### Clean Up Old Models
- Interactive model removal
- Shows all checkpoints with sizes
- Confirmation before deletion
- Safe removal from shared storage

### 💾 Storage Breakdown (Menu Option 4)

Detailed storage analysis:
- Python venv (CUDA libraries)
- SD Checkpoints
- SD WebUI installation
- All workspaces
- Scripts directory
- **Total AI Hub size**

### 🚀 Launch Tool (Menu Option 5)

Interactive launcher menu:
- Lists all available launcher scripts
- Numbered selection
- Direct execution from TUI

**Available launchers:**
- Claude Code
- Crush
- Gemini
- Ollama
- LM Studio
- Qwen
- OpenCode
- SD WebUI

## Quick Stats Dashboard

Always visible on main menu:
- **Hub Size:** Total AI hub storage usage
- **RAM Available:** Current free RAM
- **GPU:** Detected GPU with VRAM
- **Disk Free:** Available disk space

## Navigation

- **Number keys:** Select menu options
- **0:** Back to main menu / Exit
- **Enter:** Confirm selection
- **Ctrl+C:** Emergency exit

## Examples

### Example 1: Check if you can download FLUX Dev

```
1. Launch AI Hub TUI: ~/Projects/ai/ai-hub
2. Select [3] Model Management
3. Select [2] Check requirements for new model
4. Select [1] FLUX Dev
5. View results:
   - Green ✓: Ready to download
   - Red ✗: See missing requirements
```

### Example 2: Launch Ollama

```
1. Launch AI Hub TUI: ~/Projects/ai/ai-hub
2. Select [5] Launch Tool
3. Select [4] Ollama (or appropriate number)
4. Ollama launcher starts
```

### Example 3: Check Storage Usage

```
1. Launch AI Hub TUI: ~/Projects/ai/ai-hub
2. Select [4] Storage Breakdown
3. View detailed breakdown by component
4. See total AI Hub size
```

### Example 4: Remove Old Model

```
1. Launch AI Hub TUI: ~/Projects/ai/ai-hub
2. Select [3] Model Management
3. Select [4] Clean up old models
4. View list of models
5. Enter number of model to remove
6. Confirm deletion
```

## Requirements Database

The TUI includes a requirements database for popular models:

| Model | RAM | VRAM | Disk | Notes |
|-------|-----|------|------|-------|
| FLUX Dev | 16GB | 12GB | 24GB | Latest high-quality |
| FLUX Schnell | 16GB | 12GB | 24GB | Fast variant |
| SDXL | 16GB | 8GB | 7GB | High resolution |
| SD 1.5 | 8GB | 4GB | 4GB | Fast, efficient |
| SD 2.1 | 8GB | 6GB | 5GB | Improved SD |

## Color Scheme

- **Cyan:** Headers, titles, primary info
- **Green:** Success, available, good status
- **Yellow:** Warnings, limited resources
- **Red:** Errors, missing, critical
- **White:** Regular text
- **Dim:** Secondary information

## Troubleshooting

### TUI won't start
```bash
# Check if rich is installed
pacman -Q python-rich

# If not, install it
sudo pacman -S python-rich

# Check Python version
python3 --version  # Should be 3.10+
```

### GPU not detected
- Ensure NVIDIA drivers are installed
- Check: `nvidia-smi`
- TUI will show "No NVIDIA GPU detected" if unavailable

### Models not showing
- Verify models are in: `~/Projects/ai/models/checkpoints/`
- Check for `.safetensors` files
- Ensure proper permissions

### Launcher scripts not found
- Run: `~/Projects/ai/scripts/setup-tool-access.sh`
- Check: `ls ~/Projects/ai/scripts/launch-*.sh`

## Tips

1. **Before downloading large models:** Always use "Check requirements for new model" (Menu 3→2)
2. **Regular cleanup:** Use "Storage Breakdown" (Menu 4) to monitor usage
3. **Quick access:** Add alias to `.bashrc`:
   ```bash
   echo "alias ai-hub='~/Projects/ai/ai-hub'" >> ~/.bashrc
   source ~/.bashrc
   ```
4. **System monitoring:** Use "System Information" (Menu 1) before heavy tasks

## Advanced Features

### Model Requirements Checking

The TUI prevents you from downloading models your system can't run:
- Compares your hardware against model requirements
- Identifies specific bottlenecks (RAM, VRAM, or disk)
- Saves time and bandwidth by checking before download

### Shared Model Management

All model operations consider the shared model structure:
- Checkpoints in `~/Projects/ai/models/checkpoints/`
- Accessed by ComfyUI via symlink
- Accessed by SD-WebUI via symlink
- Single source of truth for all tools

---

**Last Updated:** 2025-12-31
