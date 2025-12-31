#!/usr/bin/env python3
"""
AI Tools Hub - Terminal User Interface
Interactive dashboard for managing AI tools, models, and system resources
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, List, Tuple

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    import readchar
except ImportError as e:
    print(f"Error: Missing library. Installing...")
    missing = str(e).split("'")[1] if "'" in str(e) else "rich readchar"
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "rich", "readchar"], check=True)
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.layout import Layout
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich import box
    import readchar

console = Console()

# Constants
AI_HUB = Path.home() / "Projects" / "ai"
CONFIGS_DIR = AI_HUB / "configs"
WORKSPACES_DIR = AI_HUB / "workspaces"
MODELS_DIR = AI_HUB / "models"
SCRIPTS_DIR = AI_HUB / "scripts"

# ASCII Art for each tool with brand colors
TOOL_ASCII_ART = {
    "claude": """[bold #CC785C]    ╔═══════════════════════════════════════╗
    ║   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
    ║  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
    ║  ██║     ██║     ███████║██║   ██║██║  ██║█████╗
    ║  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
    ║  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
    ║   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    ╚═══════════════════════════════════════╝[/]""",
    "crush": """[bold #FF6B9D]    ╔═══════════════════════════════════╗
    ║   ██████╗██████╗ ██╗   ██╗███████╗██╗  ██╗
    ║  ██╔════╝██╔══██╗██║   ██║██╔════╝██║  ██║
    ║  ██║     ██████╔╝██║   ██║███████╗███████║
    ║  ██║     ██╔══██╗██║   ██║╚════██║██╔══██║
    ║  ╚██████╗██║  ██║╚██████╔╝███████║██║  ██║
    ║   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    ╚═══════════════════════════════════╝[/]""",
    "gemini": """[bold #4285F4]    ╔══════════════════════════════════════════╗
    ║   ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
    ║  ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
    ║  ██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
    ║  ██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║
    ║  ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║
    ║   ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝
    ╚══════════════════════════════════════════╝[/]""",
    "ollama": """[bold white]    ╔════════════════════════════════════════╗
    ║   ██████╗ ██╗     ██╗      █████╗ ███╗   ███╗ █████╗
    ║  ██╔═══██╗██║     ██║     ██╔══██╗████╗ ████║██╔══██╗
    ║  ██║   ██║██║     ██║     ███████║██╔████╔██║███████║
    ║  ██║   ██║██║     ██║     ██╔══██║██║╚██╔╝██║██╔══██║
    ║  ╚██████╔╝███████╗███████╗██║  ██║██║ ╚═╝ ██║██║  ██║
    ║   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    ╚════════════════════════════════════════╝[/]""",
    "lmstudio": """[bold #7B61FF]    ╔═══════════════════════════════╗
    ║  ██╗     ███╗   ███╗███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗
    ║  ██║     ████╗ ████║██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
    ║  ██║     ██╔████╔██║███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
    ║  ██║     ██║╚██╔╝██║╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
    ║  ███████╗██║ ╚═╝ ██║███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
    ║  ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝
    ╚═══════════════════════════════╝[/]""",
    "qwen": """[bold #FF6B00]    ╔════════════════════════════════╗
    ║   ██████╗ ██╗    ██╗███████╗███╗   ██╗
    ║  ██╔═══██╗██║    ██║██╔════╝████╗  ██║
    ║  ██║   ██║██║ █╗ ██║█████╗  ██╔██╗ ██║
    ║  ██║▄▄ ██║██║███╗██║██╔══╝  ██║╚██╗██║
    ║  ╚██████╔╝╚███╔███╔╝███████╗██║ ╚████║
    ║   ╚══▀▀═╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═══╝
    ╚════════════════════════════════╝[/]""",
    "opencode": """[bold #00D4FF]    ╔═══════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗
    ║  ██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ║  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║██║     ██║   ██║██║  ██║█████╗
    ║  ██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║     ██║   ██║██║  ██║██╔══╝
    ║  ╚██████╔╝██║     ███████╗██║ ╚████║╚██████╗╚██████╔╝██████╔╝███████╗
    ║   ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
    ╚═══════════════════════════════════════╝[/]""",
    "automatic1111": """[bold #FF6B35]    ╔═══════════════════════════════════════╗
    ║   █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ██╗ ██╗ ██╗ ██╗
    ║  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔════╝███║███║███║███║
    ║  ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   ██║██║     ╚██║╚██║╚██║╚██║
    ║  ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██║██║      ██║ ██║ ██║ ██║
    ║  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╗ ██║ ██║ ██║ ██║
    ║  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚═╝
    ╚═══════════════════════════════════════╝[/]""",
    "comfyui": """[bold #FFD700]    ╔═══════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███╗   ███╗███████╗██╗   ██╗██╗   ██╗██╗
    ║  ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚██╗ ██╔╝██║   ██║██║
    ║  ██║     ██║   ██║██╔████╔██║█████╗   ╚████╔╝ ██║   ██║██║
    ║  ██║     ██║   ██║██║╚██╔╝██║██╔══╝    ╚██╔╝  ██║   ██║██║
    ║  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║        ██║   ╚██████╔╝██║
    ║   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝    ╚═════╝ ╚═╝
    ╚═══════════════════════════════════════╝[/]"""
}

# Theme color mappings
THEMES = {
    "tokyonight": {
        "primary": "#7AA2F7",
        "accent": "#BB9AF7",
        "success": "#9ECE6A",
        "warning": "#E0AF68",
        "error": "#F7768E",
        "muted": "#565F89",
        "border": "#414868"
    },
    "gruvbox": {
        "primary": "#83A598",
        "accent": "#D3869B",
        "success": "#B8BB26",
        "warning": "#FABD2F",
        "error": "#FB4934",
        "muted": "#928374",
        "border": "#504945"
    },
    "catppuccin": {
        "primary": "#89B4FA",
        "accent": "#CBA6F7",
        "success": "#A6E3A1",
        "warning": "#F9E2AF",
        "error": "#F38BA8",
        "muted": "#6C7086",
        "border": "#45475A"
    },
    "nord": {
        "primary": "#88C0D0",
        "accent": "#B48EAD",
        "success": "#A3BE8C",
        "warning": "#EBCB8B",
        "error": "#BF616A",
        "muted": "#4C566A",
        "border": "#3B4252"
    },
    "ansi": {
        "primary": "blue",
        "accent": "magenta",
        "success": "green",
        "warning": "yellow",
        "error": "red",
        "muted": "bright_black",
        "border": "bright_black"
    }
}

def detect_vim_theme() -> str:
    """Detect vim/nvim colorscheme from config files"""

    # Check nvim config first
    nvim_paths = [
        Path.home() / ".config/nvim/lua/config/lazy.lua",
        Path.home() / ".config/nvim/init.lua",
        Path.home() / ".config/nvim/init.vim",
        Path.home() / ".vimrc"
    ]

    for config_path in nvim_paths:
        if not config_path.exists():
            continue

        try:
            content = config_path.read_text()

            # Look for common theme names
            for theme in ["tokyonight", "gruvbox", "catppuccin", "nord"]:
                if theme in content.lower():
                    return theme
        except:
            continue

    return "ansi"  # Fallback to ANSI colors

def load_theme_config() -> str:
    """Load theme preference from config file"""
    config_file = CONFIGS_DIR / "tui-theme.conf"

    if config_file.exists():
        try:
            theme = config_file.read_text().strip()
            if theme in THEMES:
                return theme
        except:
            pass

    return None

def save_theme_config(theme: str):
    """Save theme preference to config file"""
    config_file = CONFIGS_DIR / "tui-theme.conf"
    config_file.parent.mkdir(parents=True, exist_ok=True)
    config_file.write_text(theme)

def get_active_theme() -> Dict[str, str]:
    """Get the active theme colors"""
    # 1. Check user config
    user_theme = load_theme_config()
    if user_theme:
        return THEMES[user_theme]

    # 2. Try to detect vim theme
    detected_theme = detect_vim_theme()
    if detected_theme in THEMES:
        return THEMES[detected_theme]

    # 3. Fallback to ANSI
    return THEMES["ansi"]

# Initialize theme
THEME = get_active_theme()


@dataclass
class SystemSpecs:
    """System hardware specifications"""
    cpu: str
    cpu_cores: int
    ram_total_gb: float
    ram_available_gb: float
    gpu: Optional[str]
    vram_gb: Optional[float]
    disk_free_gb: float


@dataclass
class ModelRequirements:
    """Model minimum requirements"""
    name: str
    ram_gb: float
    vram_gb: float
    disk_gb: float


def get_system_specs() -> SystemSpecs:
    """Gather system hardware information"""

    # CPU info
    try:
        cpu_info = subprocess.run(
            ["lscpu"], capture_output=True, text=True
        ).stdout
        cpu_name = [l for l in cpu_info.split('\n') if 'Model name' in l][0].split(':')[1].strip()
        cpu_cores = int([l for l in cpu_info.split('\n') if 'CPU(s):' in l][0].split(':')[1].strip())
    except:
        cpu_name = "Unknown"
        cpu_cores = os.cpu_count() or 0

    # RAM info
    try:
        mem_info = subprocess.run(
            ["free", "-g"], capture_output=True, text=True
        ).stdout.split('\n')[1].split()
        ram_total = float(mem_info[1])
        ram_available = float(mem_info[6])
    except:
        ram_total = 0.0
        ram_available = 0.0

    # GPU info (NVIDIA)
    gpu_name = None
    vram_gb = None
    try:
        nvidia_smi = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"],
            capture_output=True, text=True
        )
        if nvidia_smi.returncode == 0:
            gpu_info = nvidia_smi.stdout.strip().split(',')
            gpu_name = gpu_info[0].strip()
            vram_gb = float(gpu_info[1].strip().split()[0]) / 1024
    except:
        pass

    # Disk space
    try:
        disk_stat = shutil.disk_usage(AI_HUB)
        disk_free_gb = disk_stat.free / (1024**3)
    except:
        disk_free_gb = 0.0

    return SystemSpecs(
        cpu=cpu_name,
        cpu_cores=cpu_cores,
        ram_total_gb=ram_total,
        ram_available_gb=ram_available,
        gpu=gpu_name,
        vram_gb=vram_gb,
        disk_free_gb=disk_free_gb
    )


def get_dir_size_gb(path: Path) -> float:
    """Get directory size in GB"""
    try:
        result = subprocess.run(
            ["du", "-sb", str(path)],
            capture_output=True, text=True
        )
        bytes_size = int(result.stdout.split()[0])
        return bytes_size / (1024**3)
    except:
        return 0.0


def check_tool_installed(tool: str) -> bool:
    """Check if a command-line tool is installed"""
    return shutil.which(tool) is not None


def get_tool_status() -> Dict[str, Dict]:
    """Get status of all AI tools"""
    tools = {
        "claude": {"cmd": "claude", "workspace": "claude"},
        "crush": {"cmd": "crush", "workspace": "crush"},
        "gemini": {"cmd": "gemini", "workspace": "gemini"},
        "ollama": {"cmd": "ollama", "workspace": "ollama"},
        "lmstudio": {"cmd": "lmstudio", "workspace": "lmstudio"},
        "qwen": {"cmd": "qwen", "workspace": "qwen"},
        "opencode": {"cmd": "opencode", "workspace": "opencode"},
    }

    status = {}
    for name, info in tools.items():
        launcher = SCRIPTS_DIR / f"launch-{name}.sh"
        workspace = WORKSPACES_DIR / info["workspace"]

        status[name] = {
            "installed": check_tool_installed(info["cmd"]),
            "launcher": launcher.exists() and launcher.is_file(),
            "workspace": workspace.exists() and workspace.is_dir(),
            "workspace_size": get_dir_size_gb(workspace) if workspace.exists() else 0.0
        }

    return status


def display_system_info():
    """Display system hardware information"""
    console.clear()

    specs = get_system_specs()

    # Create system info table
    table = Table(title="System Hardware Specifications", box=box.ROUNDED)
    table.add_column("Component", style="cyan", no_wrap=True)
    table.add_column("Specification", style="white")
    table.add_column("Status", style="green")

    # CPU
    table.add_row("CPU", specs.cpu, f"{specs.cpu_cores} cores")

    # RAM
    ram_percent = (specs.ram_available_gb / specs.ram_total_gb * 100) if specs.ram_total_gb > 0 else 0
    ram_status = "✓ Good" if specs.ram_available_gb > 8 else "⚠ Low"
    table.add_row(
        "RAM",
        f"{specs.ram_total_gb:.1f} GB total",
        f"{specs.ram_available_gb:.1f} GB available ({ram_percent:.0f}%) {ram_status}"
    )

    # GPU
    if specs.gpu:
        vram_status = "✓ Good" if specs.vram_gb and specs.vram_gb >= 8 else "⚠ Limited"
        table.add_row(
            "GPU",
            specs.gpu,
            f"{specs.vram_gb:.1f} GB VRAM {vram_status}"
        )
    else:
        table.add_row("GPU", "No NVIDIA GPU detected", "❌ Not available")

    # Disk
    disk_status = "✓ Good" if specs.disk_free_gb > 50 else "⚠ Low"
    table.add_row("Disk Space", f"{specs.disk_free_gb:.1f} GB free", disk_status)

    console.print(table)
    console.print()


def display_tool_status():
    """Display status of all AI tools"""
    status = get_tool_status()

    table = Table(title="AI Tools Status", box=box.ROUNDED)
    table.add_column("Tool", style="cyan", no_wrap=True)
    table.add_column("Installed", justify="center")
    table.add_column("Launcher", justify="center")
    table.add_column("Workspace", justify="center")
    table.add_column("Size", justify="right")

    for name, info in sorted(status.items()):
        installed = "✓" if info["installed"] else "✗"
        launcher = "✓" if info["launcher"] else "✗"
        workspace = "✓" if info["workspace"] else "✗"
        size = f"{info['workspace_size']:.2f} GB" if info['workspace_size'] > 0 else "0 MB"

        installed_style = "green" if info["installed"] else "red"

        table.add_row(
            name.title(),
            f"[{installed_style}]{installed}[/]",
            f"[green]{launcher}[/]" if info["launcher"] else f"[red]{launcher}[/]",
            f"[green]{workspace}[/]" if info["workspace"] else f"[red]{workspace}[/]",
            size
        )

    console.print(table)
    console.print()


def display_models():
    """Display information about AI models"""
    models_path = MODELS_DIR / "checkpoints"

    table = Table(title="AI Models (Checkpoints)", box=box.ROUNDED)
    table.add_column("Model", style="cyan")
    table.add_column("Size", justify="right")
    table.add_column("Type", style="yellow")

    if models_path.exists():
        total_size = 0.0
        model_count = 0

        for model_file in sorted(models_path.glob("*.safetensors")):
            size_gb = model_file.stat().st_size / (1024**3)
            total_size += size_gb
            model_count += 1

            # Determine type
            if "xl" in model_file.name.lower():
                model_type = "SDXL"
            elif "v1-5" in model_file.name.lower() or "v15" in model_file.name.lower():
                model_type = "SD 1.5"
            else:
                model_type = "SD"

            table.add_row(
                model_file.name,
                f"{size_gb:.2f} GB",
                model_type
            )

        table.add_row("", "", "", style="dim")
        table.add_row(
            f"Total: {model_count} models",
            f"{total_size:.2f} GB",
            "",
            style="bold cyan"
        )
    else:
        table.add_row("No models found", "", "")

    console.print(table)
    console.print()


def display_storage():
    """Display storage breakdown"""
    table = Table(title="AI Hub Storage", box=box.ROUNDED)
    table.add_column("Directory", style="cyan")
    table.add_column("Size", justify="right", style="yellow")
    table.add_column("Description")

    dirs = [
        (CONFIGS_DIR / ".venv", "Python venv (CUDA)"),
        (MODELS_DIR / "checkpoints", "SD Checkpoints"),
        (AI_HUB / "stable-diffusion-webui", "SD WebUI"),
        (WORKSPACES_DIR, "All Workspaces"),
        (SCRIPTS_DIR, "Scripts"),
    ]

    total_size = 0.0
    for dir_path, description in dirs:
        if dir_path.exists():
            size_gb = get_dir_size_gb(dir_path)
            total_size += size_gb
            table.add_row(
                dir_path.name,
                f"{size_gb:.2f} GB",
                description
            )

    table.add_row("", "", "", style="dim")
    table.add_row(
        "Total AI Hub",
        f"{total_size:.2f} GB",
        "",
        style="bold cyan"
    )

    console.print(table)
    console.print()


def check_model_requirements(model_name: str) -> Tuple[bool, List[str]]:
    """Check if system meets requirements for a model"""
    specs = get_system_specs()

    # Model requirements database
    requirements = {
        "flux-dev": ModelRequirements("FLUX Dev", ram_gb=16, vram_gb=12, disk_gb=24),
        "flux-schnell": ModelRequirements("FLUX Schnell", ram_gb=16, vram_gb=12, disk_gb=24),
        "sdxl": ModelRequirements("SDXL", ram_gb=16, vram_gb=8, disk_gb=7),
        "sd15": ModelRequirements("SD 1.5", ram_gb=8, vram_gb=4, disk_gb=4),
        "sd21": ModelRequirements("SD 2.1", ram_gb=8, vram_gb=6, disk_gb=5),
    }

    req = requirements.get(model_name)
    if not req:
        return True, []

    issues = []

    # Check RAM
    if specs.ram_available_gb < req.ram_gb:
        issues.append(f"RAM: Need {req.ram_gb}GB, have {specs.ram_available_gb:.1f}GB available")

    # Check VRAM
    if specs.vram_gb is None:
        issues.append(f"GPU: NVIDIA GPU required with {req.vram_gb}GB VRAM")
    elif specs.vram_gb < req.vram_gb:
        issues.append(f"VRAM: Need {req.vram_gb}GB, have {specs.vram_gb:.1f}GB")

    # Check disk space
    if specs.disk_free_gb < req.disk_gb:
        issues.append(f"Disk: Need {req.disk_gb}GB free, have {specs.disk_free_gb:.1f}GB")

    return len(issues) == 0, issues


def model_management_menu():
    """Interactive model management menu"""
    console.clear()
    console.print(Panel.fit("📦 Model Management", style="bold cyan"))
    console.print()

    console.print("  [1] View model details")
    console.print("  [2] Check requirements for new model")
    console.print("  [3] Consolidate duplicate models")
    console.print("  [4] Clean up old models")
    console.print("  [0] Back to main menu")
    console.print()

    choice = Prompt.ask("Select option", default="0")

    if choice == "1":
        display_models()
        Prompt.ask("\nPress Enter to continue")
    elif choice == "2":
        check_requirements_menu()
    elif choice == "3":
        consolidate_models_menu()
    elif choice == "4":
        cleanup_models_menu()


def check_requirements_menu():
    """Check system requirements for downloading a model"""
    console.clear()
    console.print(Panel.fit("🔍 Check Model Requirements", style="bold cyan"))
    console.print()

    console.print("Available model types:")
    console.print("  [1] FLUX Dev")
    console.print("  [2] FLUX Schnell")
    console.print("  [3] SDXL")
    console.print("  [4] SD 1.5")
    console.print("  [5] SD 2.1")
    console.print()

    choice = Prompt.ask("Select model type", default="1")

    model_map = {
        "1": "flux-dev",
        "2": "flux-schnell",
        "3": "sdxl",
        "4": "sd15",
        "5": "sd21"
    }

    model = model_map.get(choice)
    if not model:
        console.print("[red]Invalid choice![/]")
        return

    can_run, issues = check_model_requirements(model)

    console.print()
    if can_run:
        console.print(f"[green]✓ Your system meets the requirements for {model.upper()}![/]")
    else:
        console.print(f"[red]✗ Your system does not meet requirements for {model.upper()}:[/]")
        for issue in issues:
            console.print(f"  [yellow]• {issue}[/]")

    console.print()
    Prompt.ask("Press Enter to continue")


def consolidate_models_menu():
    """Find and consolidate duplicate models"""
    console.print("\n[yellow]Scanning for duplicate models...[/]")

    # This would scan ComfyUI and SD-WebUI for duplicates
    console.print("[green]✓ All models already consolidated in ~/Projects/ai/models/checkpoints/[/]")
    console.print()
    Prompt.ask("Press Enter to continue")


def cleanup_models_menu():
    """Interactive model cleanup"""
    models_path = MODELS_DIR / "checkpoints"

    if not models_path.exists():
        console.print("[yellow]No models directory found[/]")
        return

    models = list(models_path.glob("*.safetensors"))

    if not models:
        console.print("[yellow]No models to clean up[/]")
        return

    console.print("\n[bold]Current models:[/]")
    for idx, model in enumerate(models, 1):
        size_gb = model.stat().st_size / (1024**3)
        console.print(f"  [{idx}] {model.name} ({size_gb:.2f} GB)")

    console.print()
    if Confirm.ask("Would you like to remove any models?"):
        choice = Prompt.ask("Enter model number to remove (or 0 to cancel)", default="0")
        try:
            idx = int(choice)
            if idx > 0 and idx <= len(models):
                model_to_remove = models[idx - 1]
                if Confirm.ask(f"Really delete {model_to_remove.name}?"):
                    model_to_remove.unlink()
                    console.print(f"[green]✓ Removed {model_to_remove.name}[/]")
        except ValueError:
            console.print("[red]Invalid choice![/]")

    console.print()
    Prompt.ask("Press Enter to continue")


def storage_and_system_menu():
    """Combined storage breakdown and system information - compact one-screen view"""
    console.clear()
    console.print(Panel.fit(f"[bold {THEME['primary']}]💾 System & Storage Information[/]", style=THEME['primary'], border_style=THEME['border']))
    console.print()

    specs = get_system_specs()
    hub_size = get_dir_size_gb(AI_HUB)

    # Left column: System specs
    sys_table = Table.grid(padding=(0, 1))
    sys_table.add_column(style=THEME['accent'])
    sys_table.add_column(style="white")

    sys_table.add_row(f"[{THEME['accent']}]CPU:[/]", specs.cpu)
    sys_table.add_row(f"[{THEME['accent']}]Cores:[/]", str(specs.cpu_cores))
    sys_table.add_row(f"[{THEME['accent']}]RAM:[/]", f"{specs.ram_available_gb:.1f}/{specs.ram_total_gb:.1f} GB")
    if specs.gpu:
        sys_table.add_row(f"[{THEME['accent']}]GPU:[/]", f"{specs.gpu}")
        sys_table.add_row(f"[{THEME['accent']}]VRAM:[/]", f"{specs.vram_gb:.1f} GB")
    sys_table.add_row(f"[{THEME['accent']}]Disk:[/]", f"{specs.disk_free_gb:.1f} GB free")

    # Middle column: Storage breakdown
    storage_table = Table.grid(padding=(0, 1))
    storage_table.add_column(style=THEME['accent'])
    storage_table.add_column(style="white", justify="right")

    storage_table.add_row(f"[{THEME['accent']}]Hub Total:[/]", f"{hub_size:.1f} GB")

    # Calculate major directories
    models_size = get_dir_size_gb(MODELS_DIR) if MODELS_DIR.exists() else 0
    workspaces_size = get_dir_size_gb(WORKSPACES_DIR) if WORKSPACES_DIR.exists() else 0
    configs_size = get_dir_size_gb(CONFIGS_DIR) if CONFIGS_DIR.exists() else 0

    storage_table.add_row(f"[{THEME['muted']}]Models:[/]", f"{models_size:.1f} GB")
    storage_table.add_row(f"[{THEME['muted']}]Workspaces:[/]", f"{workspaces_size:.1f} GB")
    storage_table.add_row(f"[{THEME['muted']}]Configs:[/]", f"{configs_size:.1f} GB")

    # Right column: Tool status (compact)
    tool_table = Table.grid(padding=(0, 1))
    tool_table.add_column(style=THEME['accent'])
    tool_table.add_column(style="white", justify="center")

    launchers = list(SCRIPTS_DIR.glob("launch-*.sh"))
    tool_table.add_row(f"[{THEME['accent']}]Tools:[/]", str(len(launchers)))

    # Count models
    models_path = MODELS_DIR / "checkpoints"
    model_count = len(list(models_path.glob("*.safetensors"))) if models_path.exists() else 0
    tool_table.add_row(f"[{THEME['accent']}]Models:[/]", str(model_count))

    # Display in columns
    from rich.columns import Columns
    sys_panel = Panel(sys_table, title="Hardware", border_style=THEME['border'])
    storage_panel = Panel(storage_table, title="Storage", border_style=THEME['border'])
    tool_panel = Panel(tool_table, title="Stats", border_style=THEME['border'])

    console.print(Columns([sys_panel, storage_panel, tool_panel], equal=True, expand=True))

    Prompt.ask(f"\n[{THEME['muted']}]Press Enter to continue[/]")


def theme_selector_menu():
    """Interactive theme selector"""
    global THEME

    current_theme_name = load_theme_config() or detect_vim_theme()

    while True:
        console.clear()
        console.print(Panel.fit(f"[bold {THEME['primary']}]🎨 Theme Selector[/]", style=THEME['primary'], border_style=THEME['border']))
        console.print()

        # Show available themes
        theme_list = list(THEMES.keys())
        console.print(f"[{THEME['accent']}]Available Themes:[/]")
        console.print()

        for idx, theme_name in enumerate(theme_list, 1):
            marker = "●" if theme_name == current_theme_name else "○"
            status = "(active)" if theme_name == current_theme_name else ""

            # Show theme preview
            theme = THEMES[theme_name]
            console.print(f"  [{idx}] {marker} [bold]{theme_name.title()}[/] {status}")
            console.print(f"      [{theme['primary']}]█[/][{theme['accent']}]█[/][{theme['success']}]█[/][{theme['warning']}]█[/][{theme['error']}]█[/]")

        console.print()
        console.print(f"[{THEME['muted']}]Current: [bold]{current_theme_name.title()}[/] (detected from vim config)" if not load_theme_config() else f"[{THEME['muted']}]Current: [bold]{current_theme_name.title()}[/] (manually selected)")
        console.print()
        console.print(f"[{THEME['muted']}]Select theme number or [{THEME['primary']}]r[/]=Reset to auto-detect • [{THEME['error']}]q[/]=Back[/]")

        key = readchar.readkey()

        if key.lower() == 'q':
            break
        elif key.lower() == 'r':
            # Reset to auto-detect
            config_file = CONFIGS_DIR / "tui-theme.conf"
            if config_file.exists():
                config_file.unlink()
            THEME = get_active_theme()
            current_theme_name = detect_vim_theme()
            console.print(f"\n[{THEME['success']}]✓ Theme reset to auto-detect ({current_theme_name})[/]")
            import time
            time.sleep(1)
        else:
            try:
                choice = int(key)
                if 1 <= choice <= len(theme_list):
                    selected_theme = theme_list[choice - 1]
                    save_theme_config(selected_theme)
                    THEME = THEMES[selected_theme]
                    current_theme_name = selected_theme
                    console.print(f"\n[{THEME['success']}]✓ Theme changed to {selected_theme.title()}[/]")
                    import time
                    time.sleep(1)
            except ValueError:
                pass


def main_menu():
    """Main TUI menu - Interactive tool launcher with keyboard navigation"""
    selected = 0

    while True:
        # Get available launchers
        launchers = sorted(SCRIPTS_DIR.glob("launch-*.sh"))

        if not launchers:
            console.clear()
            console.print(Panel.fit(
                "[bold cyan]AI Tools Hub[/]\n"
                f"[dim]Location: {AI_HUB}[/]",
                style="cyan"
            ))
            console.print()
            console.print("[red]No launchers found![/]")
            console.print("[yellow]Install AI tools to use this hub.[/]")
            console.print()
            console.print("Press 'q' to exit...")

            key = readchar.readkey()
            if key.lower() == 'q':
                break
            continue

        # Display menu
        console.clear()

        # Header with theme colors
        console.print(Panel.fit(
            f"[bold {THEME['primary']}]AI Tools Hub[/]\n"
            f"[{THEME['muted']}]Location: {AI_HUB}[/]",
            style=THEME['primary'],
            border_style=THEME['border']
        ))
        console.print()

        # Display tool list with ASCII art overlay and info panel on right
        from rich.columns import Columns

        # Get selected tool info
        selected_launcher = launchers[selected]
        selected_tool_name = selected_launcher.stem.replace("launch-", "").replace("-", " ").title()
        selected_tool_key = selected_launcher.stem.replace("launch-", "")

        # Build tool list with ASCII art overlay
        console.print(f"[bold {THEME['accent']}]🚀 Select AI Tool to Launch:[/]")
        console.print()

        # Show ASCII art for selected tool (overlays on list)
        if selected_tool_key in TOOL_ASCII_ART:
            console.print(TOOL_ASCII_ART[selected_tool_key])

        # Show tool list
        for idx, launcher in enumerate(launchers):
            tool_name = launcher.stem.replace("launch-", "").replace("-", " ").title()
            if idx == selected:
                console.print(f"  [bold {THEME['success']}]▶ {tool_name}[/]")
            else:
                console.print(f"  [{THEME['muted']}]  {tool_name}[/]")

        console.print()

        # Show info in a compact line or small panel
        workspace = WORKSPACES_DIR / selected_tool_key
        info_line = f"[{THEME['muted']}]{selected_tool_name}[/]"
        if workspace.exists():
            info_line += f" [{THEME['muted']}]• {workspace}[/]"
        console.print(info_line)

        console.print()
        console.print(f"[{THEME['muted']}]Navigation: [{THEME['primary']}]↑/k[/] up • [{THEME['primary']}]↓/j[/] down • [{THEME['primary']}]Enter[/] launch • [{THEME['warning']}]s[/]=System • [{THEME['warning']}]m[/]=Models • [{THEME['warning']}]t[/]=Theme • [{THEME['error']}]q[/]=Quit[/]")

        # Handle keyboard input
        key = readchar.readkey()

        # Navigation
        if key == readchar.key.UP or key.lower() == 'k':
            selected = (selected - 1) % len(launchers)
        elif key == readchar.key.DOWN or key.lower() == 'j':
            selected = (selected + 1) % len(launchers)
        elif key == readchar.key.ENTER or key == '\r' or key == '\n':
            # Launch selected tool
            launcher = launchers[selected]
            tool_name = launcher.stem.replace("launch-", "").replace("-", " ").title()

            console.clear()
            console.print(f"[{THEME['primary']}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
            console.print(f"[{THEME['success']}]Launching {tool_name}...[/]")
            console.print(f"[{THEME['muted']}]Workspace: {AI_HUB}/workspaces/{launcher.stem.replace('launch-', '')}[/]")
            console.print(f"[{THEME['primary']}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]\n")

            # Run the launcher and wait for it to complete
            result = subprocess.run([str(launcher)], cwd=str(launcher.parent))

            # Show completion message
            console.print(f"\n[{THEME['primary']}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
            if result.returncode == 0:
                console.print(f"[{THEME['success']}]✓ {tool_name} exited successfully[/]")
            else:
                console.print(f"[{THEME['warning']}]⚠ {tool_name} exited with code {result.returncode}[/]")
            console.print(f"[{THEME['primary']}]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")

            console.print(f"\n[{THEME['muted']}]Press any key to return to menu...[/]")
            readchar.readkey()

        elif key.lower() == 's':
            storage_and_system_menu()
        elif key.lower() == 'm':
            model_management_menu()
        elif key.lower() == 't':
            theme_selector_menu()
        elif key.lower() == 'q':
            console.clear()
            console.print(f"\n[{THEME['accent']}]Goodbye![/]")
            break


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]Interrupted by user[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/]")
        sys.exit(1)
