# 🤖 AI Tools Hub

> A unified management system for AI CLI tools with beautiful TUI, shared model storage, and CLI orchestration for chaining AI workflows.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform: Linux](https://img.shields.io/badge/platform-linux-lightgrey.svg)](https://www.linux.org/)

## ✨ Features

- 🖥️ **Beautiful TUI** - Interactive terminal interface for managing AI tools
- 🔗 **CLI Orchestration** - Chain and pipe commands across different AI tools *(coming soon)*
- 📊 **Hardware Monitoring** - Real-time CPU, RAM, GPU, VRAM tracking
- 🔍 **Requirements Checker** - Verify system specs before downloading models
- 🗂️ **Shared Model Storage** - No duplicate models across tools (save 50GB+)
- 🚀 **Unified Launcher** - Launch all AI tools from one interface
- 🔐 **Centralized Configs** - Shared API keys and environment management
- 📦 **7 Tool Support** - Claude Code, Ollama, Gemini, Crush, LM Studio, Qwen, OpenCode
- 💾 **Storage Analytics** - Track and optimize disk usage

## 🎯 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-tools-hub.git
cd ai-tools-hub

# Run installation
./install.sh

# Launch the TUI
ai
```

## 🔗 CLI Orchestration Vision

Chain AI tools together like Unix pipes:

```bash
# Code review workflow
cat code.py | ai-hub claude review | ai-hub gemini improve | tee improved.py

# Multi-model consensus
echo "Is this a good idea?" | ai-hub ask --all | ai-hub compare

# Image generation pipeline
ai-hub ollama "Generate SD prompt for sunset" | ai-hub sd-gen | ai-hub upscale

# Document processing
cat report.txt | ai-hub summarize | ai-hub translate --to=spanish | ai-hub tts
```

See [Roadmap](#-roadmap) for implementation plan.

## 🎨 Why AI Hub?

### Before
- ❌ Duplicate models wasting 50GB+
- ❌ Scattered configurations
- ❌ No hardware verification before downloads
- ❌ Manual tool management
- ❌ No way to chain AI tools

### After
- ✅ Shared models (one copy, multiple tools)
- ✅ Centralized configuration
- ✅ Pre-download hardware checks
- ✅ Beautiful TUI management
- ✅ CLI orchestration *(coming soon)*
- ✅ **90GB+ saved in testing**

## 🛠️ Supported Tools

| Tool | Status | Description |
|------|--------|-------------|
| **Claude Code** | ✅ | Official Claude CLI |
| **Ollama** | ✅ | Local LLM runner |
| **Gemini** | ✅ | Google's Gemini CLI |
| **Crush** | ✅ | AI coding assistant |
| **LM Studio** | ✅ | Local model interface |
| **Qwen** | ✅ | Alibaba's Qwen models |
| **OpenCode** | ✅ | Open-source coding AI |
| **SD WebUI** | ✅ | Stable Diffusion WebUI |

## 💻 System Requirements

### Minimum
- **OS:** Linux (Arch, Ubuntu, Debian, etc.)
- **Python:** 3.10+
- **Disk:** 50GB+ free
- **RAM:** 8GB

### Recommended
- **RAM:** 16GB+
- **GPU:** NVIDIA with 8GB+ VRAM
- **Disk:** 100GB+ free

## 📦 Installation

```bash
git clone https://github.com/yourusername/ai-tools-hub.git
cd ai-tools-hub
chmod +x install.sh
./install.sh
```

The installer will:
1. Create directory structure
2. Install dependencies (`python-rich`)
3. Set up bash aliases (`ai`, `ai-status`, etc.)
4. Configure API key template
5. Make scripts executable

## 🚀 Usage

### TUI Interface
```bash
ai                 # Launch interactive TUI
ai-status          # Quick status check
ai-models          # List all models
```

### Launch Tools
```bash
~/Projects/ai/scripts/launch-claude.sh
~/Projects/ai/scripts/launch-ollama.sh run llama2
~/Projects/ai/scripts/launch-sd-webui.sh
```

## 📚 Documentation

- **[Getting Started](GETTING-STARTED.md)** - New user guide
- **[TUI Guide](TUI-GUIDE.md)** - Detailed TUI documentation
- **[Quick Reference](QUICK-REFERENCE.md)** - Command cheatsheet
- **[Architecture](ARCHITECTURE.md)** - System architecture

## 🎯 Key Features

### Hardware Requirements Checker

Check before downloading:

```
ai → [3] Model Management → [2] Check requirements

Your System:
  RAM: 10GB   ⚠️  (Need 16GB)
  VRAM: 6GB   ⚠️  (Need 12GB)
  Disk: 100GB ✅  (Need 24GB)

Result: Cannot run FLUX Dev
```

### Shared Model Storage

No more duplicates:

```
~/Projects/ai/models/checkpoints/model.safetensors (13GB)
    ↓ (symlinked to both)
    ├─→ ComfyUI/models/
    └─→ SD-WebUI/models/

Before: 26GB | After: 13GB | Saved: 13GB
```

### Real-Time Monitoring

```
╭────── Quick Stats ──────╮
│ Hub:  31GB              │
│ RAM:  10GB available    │
│ GPU:  RTX 3060 (6GB)    │
│ Disk: 100GB free        │
╰─────────────────────────╯
```

## 📊 Performance

**Space Savings in Testing:**
- Consolidated models: +45GB
- Cleaned caches: +34GB
- Removed unused: +1.4GB
- Emptied trash: +9.3GB
- **Total: 90.1GB saved** ✨

| Directory | Before | After | Saved |
|-----------|--------|-------|-------|
| ComfyUI | 112GB | 22GB | 90GB |
| Projects | 10GB | 651MB | 9.3GB |
| AI Hub | 9GB | 31GB | -22GB |
| **Total** | **131GB** | **54GB** | **77GB** |

## 🗺️ Roadmap

### Phase 1: CLI Orchestration 🎯 *(Next Priority)*

**Core Framework**
- [ ] Unified `ai-hub` command with subcommands
- [ ] Standard I/O format (JSON/streaming)
- [ ] Error handling and status codes

**Tool Wrappers**
- [ ] `ai-hub ask <tool> <prompt>` - Universal interface
- [ ] `ai-hub compare <prompt>` - Multi-tool comparison
- [ ] Direct tool access: `ai-hub claude|gemini|ollama`

**Pipeline Features**
- [ ] Pipe chaining: `tool1 | tool2 | tool3`
- [ ] Parallel execution: `ai-hub parallel "prompt"`
- [ ] Template workflows: `ai-hub run workflow.yaml`
- [ ] Save/replay: `ai-hub save/replay <name>`

**Flow Playground**
- [ ] Interactive workflow builder (TUI)
- [ ] Pre-built templates (code review, translation, etc.)
- [ ] Workflow visualization
- [ ] Debug mode with step execution

### Phase 2: Enhanced Features
- [ ] Model download integration
- [ ] Cloud storage sync
- [ ] Workflow marketplace
- [ ] Remote execution

### Phase 3: Platform Support
- [ ] Web interface (optional)
- [ ] Docker containerization
- [ ] macOS support
- [ ] Windows WSL support

## 💡 CLI Orchestration Use Cases

### Code Review Pipeline
```bash
cat app.py \
  | ai-hub claude "Review bugs" \
  | ai-hub gemini "Best practices" \
  | ai-hub ollama "Optimize" \
  | tee review.md
```

### Content Creation
```bash
echo "AI Tools" \
  | ai-hub claude "Blog outline" \
  | ai-hub gemini "Full post" \
  | ai-hub ollama "SEO keywords"
```

### Multi-Model Consensus
```bash
ai-hub compare-all "Refactor this?" \
  --tools claude,gemini,ollama \
  --format table
```

### Image Pipeline
```bash
echo "Sunset mountains" \
  | ai-hub ollama "SD prompt" \
  | ai-hub sd-gen --model realistic \
  | ai-hub upscale --2x
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

1. Fork the repository
2. Create feature branch (`git checkout -b feature/name`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/name`)
5. Open Pull Request

## 🐛 Troubleshooting

**GPU Not Detected**
```bash
nvidia-smi  # Verify drivers
ai          # Restart TUI
```

**TUI Won't Launch**
```bash
pip install rich
# OR
sudo pacman -S python-rich
```

**Models Missing**
```bash
ls ~/Projects/ai/models/checkpoints/
# Should show .safetensors files
```

## 📄 License

Apache License 2.0 - see [LICENSE](LICENSE)

## 🙏 Acknowledgments

- [Rich](https://github.com/Textualize/rich) - Beautiful terminal UI
- AI Tools community
- All contributors

---

<p align="center">
  Made with ❤️ by the AI Tools Hub community
</p>

<p align="center">
  <a href="https://github.com/yourusername/ai-tools-hub">GitHub</a> •
  <a href="https://github.com/yourusername/ai-tools-hub/issues">Issues</a> •
  <a href="https://github.com/yourusername/ai-tools-hub/discussions">Discussions</a>
</p>
