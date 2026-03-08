# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Unified management system for 7+ AI CLI tools with an interactive TUI, shared model storage, and CLI orchestration. Provides a single interface for launching and monitoring Claude, Ollama, Gemini, LM Studio, Qwen, OpenCode, and Crush.

## Tech Stack

| Component | Technology |
|---|---|
| TUI | Python 3.10+, Rich |
| Scripts | Bash |
| AI Tools | Claude, Ollama, Gemini, LM Studio, Qwen, OpenCode, Crush |

## Project Structure

```
ai-tools-hub/
├── scripts/
│   ├── ai-hub-tui.py        # Interactive terminal interface (41KB)
│   ├── ai-hub-status.sh     # CLI status checker
│   └── launch-*.sh          # Per-tool launchers
├── configs/
│   └── .claude/              # Claude agent configs and hook scripts
├── models/                   # Shared model storage (checkpoints, embeddings, loras, vae)
├── ARCHITECTURE.md           # System design
├── install.sh                # Installation with dependency setup
└── workspaces/
```

## Key Commands

```bash
ai                    # Launch TUI
ai-status             # Quick status check
ai-models             # List models
./install.sh          # Setup with dependency installation
```

## Architecture

Real-time hardware monitoring (CPU, RAM, GPU, VRAM), shared model storage to eliminate duplicates (90GB+ savings), and requirements checking before model downloads.

## Cross-Repo Relationships

- **cortex** — Multi-agent workflow integration
- **deep-research** — Research methodology reference

## Things to Avoid

- Don't duplicate models across tool directories — use shared storage
- Don't hardcode `/home/yish` — use `$HOME` or `/var/home/yish`
