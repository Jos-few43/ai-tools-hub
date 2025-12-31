# Getting Started with AI Hub

Welcome to your AI Tools Hub! This guide will get you up and running in 60 seconds.

## 🚀 Quick Start (3 Steps)

### Step 1: Activate Bash Aliases
```bash
source ~/.bashrc
```

### Step 2: Launch the TUI
```bash
ai
```

### Step 3: Explore!
That's it! You're now in the AI Hub management console.

---

## 📖 First Time Using the TUI?

When you launch `ai`, you'll see this menu:

```
Main Menu:
  [1] System Information
  [2] Tool Status
  [3] Model Management
  [4] Storage Breakdown
  [5] Launch Tool
  [0] Exit
```

**Try these first:**

1. Press `1` - See your hardware specs (CPU, RAM, GPU, VRAM)
2. Press `2` - Check which AI tools are installed
3. Press `4` - View storage breakdown
4. Press `0` - Exit

---

## 🎯 Common Tasks

### Check if you can run a model BEFORE downloading

**Problem:** Want to download FLUX Dev but not sure if your system can handle it?

**Solution:**
```bash
ai
# → [3] Model Management
# → [2] Check requirements for new model
# → [1] FLUX Dev
```

**Result:** TUI compares your hardware against requirements and tells you:
- ✓ Green: Good to go!
- ⚠️ Yellow/Red: Shows what's missing (RAM, VRAM, or disk space)

### View your installed models

**Quick way:**
```bash
ai-models
```

**TUI way:**
```bash
ai
# → [3] Model Management
# → [1] View model details
```

### Launch an AI tool

**Quick way:**
```bash
~/Projects/ai/scripts/launch-ollama.sh run llama2
```

**TUI way:**
```bash
ai
# → [5] Launch Tool
# → Select tool from menu
```

### Check overall system status

**Quick way:**
```bash
ai-status
```

**TUI way:**
```bash
ai
# → [1] System Information (detailed)
# → [2] Tool Status (installation status)
# → [4] Storage Breakdown (disk usage)
```

---

## 🔧 Available Commands

After running `source ~/.bashrc`, you have these commands:

| Command | What it does |
|---------|--------------|
| `ai` | Opens the interactive TUI |
| `ai-status` | Shows quick status in terminal |
| `ai-models` | Lists all checkpoint models |
| `ai-env` | Loads API keys into environment |

---

## 📁 Important Locations

| Path | Contains |
|------|----------|
| `~/Projects/ai/` | Main AI Hub directory (31GB) |
| `~/Projects/ai/models/checkpoints/` | All SD checkpoints (13GB) |
| `~/Projects/ai/workspaces/` | Tool sandboxes |
| `~/Projects/ai/configs/.env` | Your API keys |
| `~/Projects/ai/scripts/` | Launcher scripts |

---

## 🎓 Learning Path

### Beginner (Day 1)
1. ✅ Launch TUI with `ai`
2. ✅ Check system specs (Menu → 1)
3. ✅ View tool status (Menu → 2)
4. ✅ Check storage (Menu → 4)

### Intermediate (Week 1)
1. ✅ Check requirements before downloading models (Menu → 3 → 2)
2. ✅ Launch tools from TUI (Menu → 5)
3. ✅ View installed models (Menu → 3 → 1)
4. ✅ Use quick commands (`ai-status`, `ai-models`)

### Advanced (Month 1)
1. ✅ Clean up old models (Menu → 3 → 4)
2. ✅ Understand shared model architecture
3. ✅ Load environment and launch tools manually
4. ✅ Explore workspace sandboxing

---

## 💡 Pro Tips

### Tip 1: Check before downloading
**Always** use the requirements checker (Menu → 3 → 2) before downloading large models. It will save you time and bandwidth!

### Tip 2: Use the TUI for exploration
The TUI is great for:
- Seeing what's installed
- Checking system resources
- Managing models

### Tip 3: Use aliases for quick tasks
Use command-line aliases for routine tasks:
```bash
ai-status    # Quick status check
ai-models    # List models
```

### Tip 4: Shared models = no duplication
All your SD models are in one place:
- ComfyUI uses them via symlink
- SD-WebUI uses them via symlink
- No more duplicate 13GB models!

---

## 🆘 Troubleshooting

### TUI won't launch
```bash
# Check if ai command exists
type ai

# If not found, reload bashrc
source ~/.bashrc

# Try launching directly
~/Projects/ai/ai-hub
```

### GPU not detected in TUI
```bash
# Verify NVIDIA drivers
nvidia-smi

# If this works but TUI doesn't show GPU, restart TUI
```

### Models not showing
```bash
# Check models directory
ls ~/Projects/ai/models/checkpoints/

# Should show .safetensors files
```

### Want to add API keys
```bash
# Edit the shared environment file
nano ~/Projects/ai/configs/.env

# Add or update:
# ANTHROPIC_API_KEY="your-key"
# OPENAI_API_KEY="your-key"
# etc.
```

---

## 📚 Next Steps

1. **Read the guides:**
   - `~/Projects/ai/README.md` - Full documentation
   - `~/Projects/ai/TUI-GUIDE.md` - Detailed TUI guide
   - `~/Projects/ai/QUICK-REFERENCE.md` - Command cheatsheet
   - `~/Projects/ai/ARCHITECTURE.md` - System architecture

2. **Explore the TUI:**
   - Try all menu options
   - Check requirements for different models
   - Launch a tool

3. **Customize:**
   - Add your API keys to `.env`
   - Configure tool workspaces
   - Download models that fit your hardware

---

## 🎉 You're Ready!

Type `ai` and start exploring your AI Tools Hub!

**Remember:**
- `ai` = TUI interface
- `ai-status` = Quick status
- `ai-models` = List models
- `ai-env` = Load API keys

---

**Questions?** Check the documentation in `~/Projects/ai/*.md`

**Last Updated:** 2025-12-31
