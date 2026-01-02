#!/usr/bin/env python3
"""
Prompt Library Manager - Store and access ComfyUI prompts
Portable prompt storage with CLI and TUI interfaces
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional, Dict
from datetime import datetime

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich import box
    import readchar
except ImportError:
    print("Installing dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--break-system-packages", "rich", "readchar"], check=True)
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich import box
    import readchar

console = Console()

# Paths
AI_HUB = Path.home() / "Projects" / "ai"
PROMPTS_DIR = AI_HUB / "prompts"
COMFYUI_DIR = PROMPTS_DIR / "comfyui"
GENERAL_DIR = PROMPTS_DIR / "general"
TEMPLATES_DIR = PROMPTS_DIR / "templates"


@dataclass
class ComfyPrompt:
    """Represents a ComfyUI generation prompt"""
    name: str
    positive: str
    negative: str
    tags: List[str]
    category: str
    settings: Optional[Dict] = None
    notes: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class PromptLibrary:
    """Manage prompt library operations"""

    def __init__(self, library_dir: Path = COMFYUI_DIR):
        self.library_dir = library_dir
        self.library_dir.mkdir(parents=True, exist_ok=True)

    def list_prompts(self) -> List[str]:
        """List all prompt files"""
        return sorted([f.stem for f in self.library_dir.glob("*.json")])

    def load_prompt(self, name: str) -> Optional[ComfyPrompt]:
        """Load a prompt by name"""
        prompt_file = self.library_dir / f"{name}.json"
        if not prompt_file.exists():
            return None

        try:
            with open(prompt_file, 'r') as f:
                data = json.load(f)
            return ComfyPrompt.from_dict(data)
        except Exception as e:
            console.print(f"[red]Error loading prompt: {e}[/]")
            return None

    def save_prompt(self, prompt: ComfyPrompt, overwrite: bool = False):
        """Save a prompt to the library"""
        prompt_file = self.library_dir / f"{prompt.name}.json"

        if prompt_file.exists() and not overwrite:
            console.print(f"[yellow]Prompt '{prompt.name}' already exists![/]")
            if not Confirm.ask("Overwrite?"):
                return False

        # Update timestamps
        if not prompt.created:
            prompt.created = datetime.now().isoformat()
        prompt.modified = datetime.now().isoformat()

        try:
            with open(prompt_file, 'w') as f:
                json.dump(prompt.to_dict(), f, indent=2)
            console.print(f"[green]✓ Saved prompt '{prompt.name}'[/]")
            return True
        except Exception as e:
            console.print(f"[red]Error saving prompt: {e}[/]")
            return False

    def delete_prompt(self, name: str) -> bool:
        """Delete a prompt"""
        prompt_file = self.library_dir / f"{name}.json"
        if not prompt_file.exists():
            console.print(f"[red]Prompt '{name}' not found![/]")
            return False

        try:
            prompt_file.unlink()
            console.print(f"[green]✓ Deleted prompt '{name}'[/]")
            return True
        except Exception as e:
            console.print(f"[red]Error deleting prompt: {e}[/]")
            return False

    def search_prompts(self, query: str) -> List[str]:
        """Search prompts by name or tags"""
        query = query.lower()
        results = []

        for prompt_name in self.list_prompts():
            prompt = self.load_prompt(prompt_name)
            if not prompt:
                continue

            # Search in name, tags, and category
            if (query in prompt.name.lower() or
                query in prompt.category.lower() or
                any(query in tag.lower() for tag in prompt.tags)):
                results.append(prompt_name)

        return results

    def export_txt(self, name: str, output_file: Path):
        """Export prompt to plain text file"""
        prompt = self.load_prompt(name)
        if not prompt:
            return False

        content = f"""Prompt: {prompt.name}
Category: {prompt.category}
Tags: {', '.join(prompt.tags)}

Positive Prompt:
{prompt.positive}

Negative Prompt:
{prompt.negative}
"""

        if prompt.settings:
            content += f"\nSettings:\n{json.dumps(prompt.settings, indent=2)}\n"

        if prompt.notes:
            content += f"\nNotes:\n{prompt.notes}\n"

        output_file.write_text(content)
        console.print(f"[green]✓ Exported to {output_file}[/]")
        return True

    def import_json(self, import_file: Path):
        """Import prompts from JSON file"""
        try:
            with open(import_file, 'r') as f:
                data = json.load(f)

            # Handle both single prompt and array of prompts
            prompts_data = data if isinstance(data, list) else [data]

            imported = 0
            for prompt_data in prompts_data:
                try:
                    prompt = ComfyPrompt.from_dict(prompt_data)
                    if self.save_prompt(prompt):
                        imported += 1
                except Exception as e:
                    console.print(f"[yellow]Skipped invalid prompt: {e}[/]")

            console.print(f"[green]✓ Imported {imported} prompt(s)[/]")
            return True
        except Exception as e:
            console.print(f"[red]Error importing: {e}[/]")
            return False


def display_prompt(prompt: ComfyPrompt):
    """Display a prompt in formatted view"""
    console.print()
    console.print(Panel.fit(
        f"[bold cyan]{prompt.name}[/]",
        subtitle=f"[dim]{prompt.category} • {', '.join(prompt.tags)}[/]"
    ))
    console.print()

    # Positive prompt
    console.print("[bold green]Positive:[/]")
    console.print(Panel(prompt.positive, border_style="green"))

    # Negative prompt
    console.print("\n[bold red]Negative:[/]")
    console.print(Panel(prompt.negative, border_style="red"))

    # Settings
    if prompt.settings:
        console.print("\n[bold yellow]Settings:[/]")
        settings_text = json.dumps(prompt.settings, indent=2)
        console.print(Syntax(settings_text, "json", theme="monokai"))

    # Notes
    if prompt.notes:
        console.print("\n[bold blue]Notes:[/]")
        console.print(prompt.notes)

    console.print()


def browse_prompts_tui():
    """Interactive TUI for browsing prompts"""
    library = PromptLibrary()
    prompts = library.list_prompts()

    if not prompts:
        console.print("[yellow]No prompts in library yet![/]")
        console.print("Create your first prompt with: [cyan]prompt-lib add[/]")
        return

    selected = 0

    while True:
        console.clear()
        console.print(Panel.fit("[bold cyan]📚 Prompt Library Browser[/]", style="cyan"))
        console.print()

        # Display prompt list
        for idx, name in enumerate(prompts):
            if idx == selected:
                console.print(f"  [bold green]▶ {name}[/]")
            else:
                console.print(f"  [dim]  {name}[/]")

        console.print()
        console.print("[dim]Navigation: [cyan]↑/k[/] up • [cyan]↓/j[/] down • [cyan]Enter[/] view • [cyan]c[/] copy • [cyan]e[/] export • [cyan]d[/] delete • [red]q[/] quit[/]")

        key = readchar.readkey()

        # Navigation
        if key == readchar.key.UP or key.lower() == 'k':
            selected = (selected - 1) % len(prompts)
        elif key == readchar.key.DOWN or key.lower() == 'j':
            selected = (selected + 1) % len(prompts)
        elif key == readchar.key.ENTER or key == '\r' or key == '\n':
            # View prompt
            prompt = library.load_prompt(prompts[selected])
            if prompt:
                console.clear()
                display_prompt(prompt)
                Prompt.ask("\n[dim]Press Enter to continue[/]")
        elif key.lower() == 'c':
            # Copy to clipboard
            prompt = library.load_prompt(prompts[selected])
            if prompt:
                try:
                    # Try xclip first, then wl-copy (Wayland), then pbcopy (macOS)
                    clipboard_cmd = None
                    if subprocess.run(["which", "xclip"], capture_output=True).returncode == 0:
                        clipboard_cmd = ["xclip", "-selection", "clipboard"]
                    elif subprocess.run(["which", "wl-copy"], capture_output=True).returncode == 0:
                        clipboard_cmd = ["wl-copy"]
                    elif subprocess.run(["which", "pbcopy"], capture_output=True).returncode == 0:
                        clipboard_cmd = ["pbcopy"]

                    if clipboard_cmd:
                        subprocess.run(clipboard_cmd, input=prompt.positive.encode(), check=True)
                        console.print(f"[green]✓ Copied '{prompts[selected]}' to clipboard[/]")
                    else:
                        console.print("[yellow]⚠ No clipboard tool found (install xclip or wl-clipboard)[/]")
                except Exception as e:
                    console.print(f"[red]Error copying: {e}[/]")
                import time
                time.sleep(1)
        elif key.lower() == 'e':
            # Export prompt
            prompt = library.load_prompt(prompts[selected])
            if prompt:
                output_file = Path.home() / f"{prompts[selected]}.txt"
                library.export_txt(prompts[selected], output_file)
                import time
                time.sleep(1)
        elif key.lower() == 'd':
            # Delete prompt
            console.print()
            if Confirm.ask(f"[yellow]Delete '{prompts[selected]}'?[/]"):
                if library.delete_prompt(prompts[selected]):
                    prompts = library.list_prompts()
                    if not prompts:
                        break
                    selected = min(selected, len(prompts) - 1)
        elif key.lower() == 'q':
            break


def create_prompt_interactive():
    """Interactive prompt creation"""
    console.clear()
    console.print(Panel.fit("[bold cyan]✨ Create New Prompt[/]", style="cyan"))
    console.print()

    name = Prompt.ask("[cyan]Prompt name[/]")
    category = Prompt.ask("[cyan]Category[/]", default="general")
    tags_str = Prompt.ask("[cyan]Tags (comma-separated)[/]")
    tags = [t.strip() for t in tags_str.split(",")]

    console.print("\n[green]Positive prompt (press Ctrl+D when done):[/]")
    console.print("[dim]Tip: Enter multiple lines, press Ctrl+D to finish[/]\n")
    positive_lines = []
    try:
        while True:
            line = input()
            positive_lines.append(line)
    except EOFError:
        pass
    positive = "\n".join(positive_lines)

    console.print("\n[red]Negative prompt (press Ctrl+D when done):[/]")
    console.print("[dim]Tip: Enter multiple lines, press Ctrl+D to finish[/]\n")
    negative_lines = []
    try:
        while True:
            line = input()
            negative_lines.append(line)
    except EOFError:
        pass
    negative = "\n".join(negative_lines)

    # Optional settings
    console.print()
    if Confirm.ask("[yellow]Add settings (steps, cfg, sampler)?[/]"):
        steps = Prompt.ask("Steps", default="30")
        cfg = Prompt.ask("CFG", default="7.5")
        sampler = Prompt.ask("Sampler", default="DPM++ 2M Karras")
        settings = {
            "steps": int(steps),
            "cfg": float(cfg),
            "sampler": sampler
        }
    else:
        settings = None

    # Optional notes
    notes = Prompt.ask("[blue]Notes (optional)[/]", default="")

    prompt = ComfyPrompt(
        name=name,
        positive=positive,
        negative=negative,
        tags=tags,
        category=category,
        settings=settings,
        notes=notes if notes else None
    )

    library = PromptLibrary()
    library.save_prompt(prompt)


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Library Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Browse command
    subparsers.add_parser("browse", help="Browse prompts in TUI")

    # Add command
    subparsers.add_parser("add", help="Add new prompt interactively")

    # List command
    list_parser = subparsers.add_parser("list", help="List all prompts")
    list_parser.add_argument("--search", "-s", help="Search prompts")

    # View command
    view_parser = subparsers.add_parser("view", help="View a prompt")
    view_parser.add_argument("name", help="Prompt name")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export prompt to file")
    export_parser.add_argument("name", help="Prompt name")
    export_parser.add_argument("output", help="Output file path")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import prompts from JSON")
    import_parser.add_argument("file", help="JSON file to import")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a prompt")
    delete_parser.add_argument("name", help="Prompt name")

    args = parser.parse_args()

    library = PromptLibrary()

    if args.command == "browse" or args.command is None:
        browse_prompts_tui()

    elif args.command == "add":
        create_prompt_interactive()

    elif args.command == "list":
        if args.search:
            prompts = library.search_prompts(args.search)
            console.print(f"[cyan]Search results for '{args.search}':[/]")
        else:
            prompts = library.list_prompts()
            console.print("[cyan]All prompts:[/]")

        if prompts:
            for name in prompts:
                console.print(f"  • {name}")
        else:
            console.print("[yellow]No prompts found[/]")

    elif args.command == "view":
        prompt = library.load_prompt(args.name)
        if prompt:
            display_prompt(prompt)
        else:
            console.print(f"[red]Prompt '{args.name}' not found![/]")

    elif args.command == "export":
        library.export_txt(args.name, Path(args.output))

    elif args.command == "import":
        library.import_json(Path(args.file))

    elif args.command == "delete":
        if Confirm.ask(f"[yellow]Delete '{args.name}'?[/]"):
            library.delete_prompt(args.name)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted[/]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/]")
        sys.exit(1)
