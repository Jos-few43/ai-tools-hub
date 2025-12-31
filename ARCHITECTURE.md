# AI Hub Architecture

Visual overview of the AI Tools Hub structure and data flow.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI Tools Hub (31GB)                         │
│                      ~/Projects/ai/                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                ▼                 ▼                 ▼
        ┌───────────────┐ ┌──────────────┐ ┌──────────────┐
        │   TUI Layer   │ │  CLI Layer   │ │ Config Layer │
        │   (ai-hub)    │ │  (scripts/)  │ │ (configs/)   │
        └───────────────┘ └──────────────┘ └──────────────┘
                │                 │                 │
                └────────┬────────┴────────┬────────┘
                         ▼                 ▼
                ┌─────────────────┐ ┌──────────────┐
                │   Workspaces    │ │    Models    │
                │  (sandboxed)    │ │   (shared)   │
                └─────────────────┘ └──────────────┘
```

## Component Breakdown

### 1. TUI Layer (Terminal User Interface)

```
ai-hub (launcher)
    │
    └──> ai-hub-tui.py
            │
            ├──> System Monitor
            │    ├── Hardware specs (CPU, RAM, GPU)
            │    ├── Disk usage
            │    └── Requirements checker
            │
            ├──> Tool Manager
            │    ├── Installation status
            │    ├── Workspace health
            │    └── Launcher availability
            │
            ├──> Model Manager
            │    ├── Model viewer
            │    ├── Requirements checker
            │    ├── Duplicate finder
            │    └── Cleanup tools
            │
            └──> Storage Analyzer
                 ├── Component breakdown
                 └── Total usage tracking
```

### 2. CLI Layer (Scripts)

```
scripts/
    │
    ├── Launch Scripts (Tool Execution)
    │   ├── launch-claude.sh
    │   ├── launch-ollama.sh
    │   ├── launch-gemini.sh
    │   └── ... (7 tools total)
    │
    ├── Management Scripts
    │   ├── setup-tool-access.sh (Initial setup)
    │   ├── load-env.sh (API key loader)
    │   └── ai-hub-status.sh (CLI status)
    │
    └── TUI
        └── ai-hub-tui.py (Interactive interface)
```

### 3. Configuration Layer

```
configs/
    │
    ├── Tool Configs (Per-tool settings)
    │   ├── .claude/
    │   ├── .ollama/
    │   ├── .gemini/
    │   └── ... (7 tools)
    │
    ├── Shared Resources
    │   ├── .venv/ (9.2GB Python + CUDA)
    │   └── .env (6 API keys)
    │
    └── Documentation
        └── CLAUDE.md
```

### 4. Workspace Layer

```
workspaces/
    │
    ├── claude/         (Isolated work area)
    ├── crush/          (Isolated work area)
    ├── gemini/         (Isolated work area)
    ├── ollama/         (Isolated work area)
    ├── lmstudio/       (Isolated work area)
    ├── qwen/           (Isolated work area)
    ├── opencode/       (Isolated work area)
    └── scratch/        (Temporary work)
```

### 5. Model Storage Layer

```
models/
    │
    ├── checkpoints/ (13GB)
    │   ├── epicrealismXL_pureFix.safetensors (6.5GB)
    │   ├── realisticVisionV60B1_v51HyperVAE.safetensors (2.0GB)
    │   └── v1-5-pruned-emaonly.safetensors (4.0GB)
    │
    ├── loras/
    ├── vae/
    └── embeddings/
```

## Data Flow

### Tool Launch Flow

```
User
  │
  └──> TUI or CLI
         │
         └──> launch-<tool>.sh
                │
                ├──> Load environment (.env)
                │
                ├──> Change to workspace
                │
                └──> Execute tool with context
                       │
                       └──> Tool accesses:
                              ├── Shared models
                              ├── Shared configs
                              └── Workspace (sandbox)
```

### Model Access Flow

```
ComfyUI
  │
  └──> checkpoints-link (symlink)
         │
         └──> ~/Projects/ai/models/checkpoints/
                │
                ├── epicrealismXL_pureFix.safetensors
                ├── realisticVisionV60B1_v51HyperVAE.safetensors
                └── v1-5-pruned-emaonly.safetensors
                       ▲
                       │
                       └──────────────────┐
                                          │
SD-WebUI                                  │
  │                                       │
  └──> Stable-diffusion-shared (symlink) ┘
```

### Requirements Checking Flow

```
User wants to download model
  │
  └──> TUI: Model Management → Check Requirements
         │
         └──> get_system_specs()
                │
                ├── Query CPU info (lscpu)
                ├── Query RAM info (free -g)
                ├── Query GPU info (nvidia-smi)
                └── Query disk space (shutil)
                       │
                       └──> Compare against model requirements
                              │
                              ├── ✓ All requirements met
                              │   └──> Safe to download
                              │
                              └── ✗ Missing requirements
                                  └──> Show specific issues:
                                       ├── RAM insufficient
                                       ├── VRAM insufficient
                                       └── Disk space low
```

## Integration Points

### External Tool Integration

```
~/.claude/settings.local.json
    │
    └──> "workingDirectory": "~/Projects/ai/workspaces/claude"
         "defaultContext": "~/Projects/ai"

~/.ollama/
    │
    └──> Models stored in ~/.ollama/models (20GB)
         Workspace: ~/Projects/ai/workspaces/ollama
```

### Filesystem Access Control

```
AI Tools
  │
  ├── Read Access (Full)
  │   ├── ~/Projects/
  │   ├── ~/Documents/
  │   └── /tmp/
  │
  ├── Write Access (Controlled)
  │   ├── ~/Projects/ai/workspaces/<tool>/  (Primary)
  │   ├── ~/Projects/                        (Projects)
  │   └── /tmp/                              (Temporary)
  │
  └── Blocked
      ├── /etc/shadow, /etc/passwd
      ├── /root/
      └── /sys/, /proc/
```

## Storage Optimization

### Shared Model Strategy

**Before:**
```
~/Projects/comfy/ComfyUI/models/checkpoints/     13GB
~/Projects/foss/stable-diffusion-webui/models/   13GB
Total: 26GB (duplicated)
```

**After:**
```
~/Projects/ai/models/checkpoints/                13GB
├── ComfyUI → checkpoints-link (symlink)
└── SD-WebUI → Stable-diffusion-shared (symlink)
Total: 13GB (shared)
Saved: 13GB
```

### Consolidated Structure

**Before:**
```
~/Projects/
├── comfy/               (112GB)
├── foss/                (10GB)
└── ai/                  (9.2GB)
Total: 131GB
```

**After cleanup:**
```
~/Projects/
├── comfy/               (22GB)  ← -90GB
├── foss/                (651MB) ← -9.3GB
└── ai/                  (31GB)  ← +22GB
Total: 54GB
Cleaned: 90.1GB
```

## System Requirements

### Minimum (for TUI)
- Python 3.10+
- `rich` library (installed via pacman)
- Terminal with 256 colors

### Recommended (for AI tools)
- CPU: Modern multi-core (detected: varies)
- RAM: 16GB+ (have: 10GB available)
- GPU: NVIDIA with 8GB+ VRAM (have: RTX 3060 6GB)
- Disk: 100GB+ free (have: 100GB)

## Security Model

```
AI Hub
  │
  ├── Sandboxed Workspaces
  │   └── Tools operate in dedicated directories
  │
  ├── Shared Read Access
  │   └── Tools can read most of ~/
  │
  ├── Controlled Write Access
  │   └── Tools write to workspaces + approved dirs
  │
  └── System Protection
      └── Critical system paths blocked
```

---

**Architecture Version:** 1.0
**Last Updated:** 2025-12-31
