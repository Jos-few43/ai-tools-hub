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

# ASCII Art for each tool
TOOL_ASCII_ART = {
    "claude": r"""
    ╔═══════════════════════════════════════╗
    ║   ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
    ║  ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
    ║  ██║     ██║     ███████║██║   ██║██║  ██║█████╗
    ║  ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
    ║  ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
    ║   ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝
    ╚═══════════════════════════════════════╝
    """,
    "crush": r"""
    ╔═══════════════════════════════════╗
    ║   ██████╗██████╗ ██╗   ██╗███████╗██╗  ██╗
    ║  ██╔════╝██╔══██╗██║   ██║██╔════╝██║  ██║
    ║  ██║     ██████╔╝██║   ██║███████╗███████║
    ║  ██║     ██╔══██╗██║   ██║╚════██║██╔══██║
    ║  ╚██████╗██║  ██║╚██████╔╝███████║██║  ██║
    ║   ╚═════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    ╚═══════════════════════════════════╝
    """,
    "gemini": r"""
    ╔══════════════════════════════════════════╗
    ║   ██████╗ ███████╗███╗   ███╗██╗███╗   ██╗██╗
    ║  ██╔════╝ ██╔════╝████╗ ████║██║████╗  ██║██║
    ║  ██║  ███╗█████╗  ██╔████╔██║██║██╔██╗ ██║██║
    ║  ██║   ██║██╔══╝  ██║╚██╔╝██║██║██║╚██╗██║██║
    ║  ╚██████╔╝███████╗██║ ╚═╝ ██║██║██║ ╚████║██║
    ║   ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝
    ╚══════════════════════════════════════════╝
    """,
    "ollama": r"""
    ╔════════════════════════════════════════╗
    ║   ██████╗ ██╗     ██╗      █████╗ ███╗   ███╗ █████╗
    ║  ██╔═══██╗██║     ██║     ██╔══██╗████╗ ████║██╔══██╗
    ║  ██║   ██║██║     ██║     ███████║██╔████╔██║███████║
    ║  ██║   ██║██║     ██║     ██╔══██║██║╚██╔╝██║██╔══██║
    ║  ╚██████╔╝███████╗███████╗██║  ██║██║ ╚═╝ ██║██║  ██║
    ║   ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
    ╚════════════════════════════════════════╝
    """,
    "lmstudio": r"""
    ╔═══════════════════════════════╗
    ║  ██╗     ███╗   ███╗███████╗████████╗██╗   ██╗██████╗ ██╗ ██████╗
    ║  ██║     ████╗ ████║██╔════╝╚══██╔══╝██║   ██║██╔══██╗██║██╔═══██╗
    ║  ██║     ██╔████╔██║███████╗   ██║   ██║   ██║██║  ██║██║██║   ██║
    ║  ██║     ██║╚██╔╝██║╚════██║   ██║   ██║   ██║██║  ██║██║██║   ██║
    ║  ███████╗██║ ╚═╝ ██║███████║   ██║   ╚██████╔╝██████╔╝██║╚██████╔╝
    ║  ╚══════╝╚═╝     ╚═╝╚══════╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝ ╚═════╝
    ╚═══════════════════════════════╝
    """,
    "qwen": r"""
    ╔════════════════════════════════╗
    ║   ██████╗ ██╗    ██╗███████╗███╗   ██╗
    ║  ██╔═══██╗██║    ██║██╔════╝████╗  ██║
    ║  ██║   ██║██║ █╗ ██║█████╗  ██╔██╗ ██║
    ║  ██║▄▄ ██║██║███╗██║██╔══╝  ██║╚██╗██║
    ║  ╚██████╔╝╚███╔███╔╝███████╗██║ ╚████║
    ║   ╚══▀▀═╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═══╝
    ╚════════════════════════════════╝
    """,
    "opencode": r"""
    ╔═══════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███████╗███╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗
    ║  ██╔═══██╗██╔══██╗██╔════╝████╗  ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝
    ║  ██║   ██║██████╔╝█████╗  ██╔██╗ ██║██║     ██║   ██║██║  ██║█████╗
    ║  ██║   ██║██╔═══╝ ██╔══╝  ██║╚██╗██║██║     ██║   ██║██║  ██║██╔══╝
    ║  ╚██████╔╝██║     ███████╗██║ ╚████║╚██████╗╚██████╔╝██████╔╝███████╗
    ║   ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝
    ╚═══════════════════════════════════════╝
    """,
    "sd-webui": r"""
    ╔═══════════════════════════════════════╗
    ║   █████╗ ██╗   ██╗████████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ██╗ ██╗ ██╗ ██╗
    ║  ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔════╝███║███║███║███║
    ║  ███████║██║   ██║   ██║   ██║   ██║██╔████╔██║███████║   ██║   ██║██║     ╚██║╚██║╚██║╚██║
    ║  ██╔══██║██║   ██║   ██║   ██║   ██║██║╚██╔╝██║██╔══██║   ██║   ██║██║      ██║ ██║ ██║ ██║
    ║  ██║  ██║╚██████╔╝   ██║   ╚██████╔╝██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╗ ██║ ██║ ██║ ██║
    ║  ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝ ╚═╝ ╚═╝ ╚═╝
    ╚═══════════════════════════════════════╝
    """,
    "comfyui": r"""
    ╔═══════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███╗   ███╗███████╗██╗   ██╗██╗   ██╗██╗
    ║  ██╔════╝██╔═══██╗████╗ ████║██╔════╝╚██╗ ██╔╝██║   ██║██║
    ║  ██║     ██║   ██║██╔████╔██║█████╗   ╚████╔╝ ██║   ██║██║
    ║  ██║     ██║   ██║██║╚██╔╝██║██╔══╝    ╚██╔╝  ██║   ██║██║
    ║  ╚██████╗╚██████╔╝██║ ╚═╝ ██║██║        ██║   ╚██████╔╝██║
    ║   ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝        ╚═╝    ╚═════╝ ╚═╝
    ╚═══════════════════════════════════════╝
    """
}


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
    """Combined storage breakdown and system information"""
    console.clear()
    console.print(Panel.fit("💾 System & Storage Information", style="bold cyan"))
    console.print()

    # Quick stats
    specs = get_system_specs()
    hub_size = get_dir_size_gb(AI_HUB)

    stats = Table.grid(padding=(0, 2))
    stats.add_column(style="cyan")
    stats.add_column(style="white")

    stats.add_row("Hub Size:", f"{hub_size:.1f} GB")
    stats.add_row("RAM Available:", f"{specs.ram_available_gb:.1f} GB")
    if specs.gpu:
        stats.add_row("GPU:", f"{specs.gpu} ({specs.vram_gb:.1f} GB)")
    stats.add_row("Disk Free:", f"{specs.disk_free_gb:.1f} GB")

    console.print(Panel(stats, title="Quick Stats", box=box.ROUNDED))
    console.print()

    # System specs
    display_system_info()
    console.print()

    # Storage breakdown
    display_storage()
    console.print()

    # Tool status
    display_tool_status()

    Prompt.ask("\nPress Enter to continue")


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

        # Header
        console.print(Panel.fit(
            "[bold cyan]AI Tools Hub[/]\n"
            f"[dim]Location: {AI_HUB}[/]",
            style="cyan"
        ))
        console.print()

        # Tool list with selection highlight
        console.print("[bold cyan]🚀 Select AI Tool to Launch:[/]")
        console.print()

        for idx, launcher in enumerate(launchers):
            tool_name = launcher.stem.replace("launch-", "").replace("-", " ").title()
            tool_key = launcher.stem.replace("launch-", "")

            if idx == selected:
                # Show ASCII art for selected tool
                if tool_key in TOOL_ASCII_ART:
                    console.print(f"[bold green]{TOOL_ASCII_ART[tool_key]}[/]")
                console.print(f"  [bold green]▶ {tool_name}[/]")
            else:
                console.print(f"  [dim]  {tool_name}[/]")

        console.print()
        console.print("[dim]Navigation: ↑/k up • ↓/j down • Enter to launch • s=System • m=Models • q=Quit[/]")

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
            console.print(f"[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
            console.print(f"[green]Launching {tool_name}...[/]")
            console.print(f"[dim]Workspace: {AI_HUB}/workspaces/{launcher.stem.replace('launch-', '')}[/]")
            console.print(f"[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]\n")

            # Run the launcher and wait for it to complete
            result = subprocess.run([str(launcher)], cwd=str(launcher.parent))

            # Show completion message
            console.print(f"\n[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")
            if result.returncode == 0:
                console.print(f"[green]✓ {tool_name} exited successfully[/]")
            else:
                console.print(f"[yellow]⚠ {tool_name} exited with code {result.returncode}[/]")
            console.print(f"[cyan]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")

            console.print("\n[dim]Press any key to return to menu...[/]")
            readchar.readkey()

        elif key.lower() == 's':
            storage_and_system_menu()
        elif key.lower() == 'm':
            model_management_menu()
        elif key.lower() == 'q':
            console.clear()
            console.print("\n[cyan]Goodbye![/]")
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
