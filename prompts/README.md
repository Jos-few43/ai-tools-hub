# Prompt Library

A portable, organized library for storing and accessing ComfyUI generation prompts.

## Features

- 📚 Browse prompts with interactive TUI
- 🔍 Search by name, tags, or category
- 📋 Copy prompts to clipboard
- 📤 Export to plain text files
- 📥 Import from JSON
- 🏷️ Tag and categorize prompts
- ⚙️ Store settings (steps, CFG, sampler)

## Quick Start

### From AI Hub TUI
```bash
ai            # Launch AI Hub
# Press 'p' for Prompt Library
```

### Direct CLI Access
```bash
# Browse prompts
~/Projects/ai/scripts/prompt-lib browse

# Add new prompt
~/Projects/ai/scripts/prompt-lib add

# List all prompts
~/Projects/ai/scripts/prompt-lib list

# Search prompts
~/Projects/ai/scripts/prompt-lib list --search cyberpunk

# View a prompt
~/Projects/ai/scripts/prompt-lib view cyberpunk-portrait

# Export to file
~/Projects/ai/scripts/prompt-lib export cyberpunk-portrait ~/my-prompt.txt
```

## Optional: Add Shell Alias

Add to your `~/.bashrc`:
```bash
alias prompts='~/Projects/ai/scripts/prompt-lib browse'
alias prompt-add='~/Projects/ai/scripts/prompt-lib add'
alias prompt-search='~/Projects/ai/scripts/prompt-lib list --search'
```

Then:
```bash
prompts              # Browse all prompts
prompt-add           # Add new prompt
prompt-search neon   # Search for "neon"
```

## Directory Structure

```
~/Projects/ai/prompts/
├── comfyui/          # ComfyUI generation prompts (JSON)
├── general/          # General-purpose prompts
├── templates/        # Prompt templates
└── README.md         # This file
```

## Prompt Format

Prompts are stored as JSON files:

```json
{
  "name": "prompt-name",
  "positive": "your positive prompt here...",
  "negative": "your negative prompt here...",
  "tags": ["tag1", "tag2", "tag3"],
  "category": "portrait",
  "settings": {
    "steps": 30,
    "cfg": 7.5,
    "sampler": "DPM++ 2M Karras"
  },
  "notes": "Optional notes about this prompt",
  "created": "2026-01-01T00:00:00",
  "modified": "2026-01-01T00:00:00"
}
```

## Usage Examples

### In TUI Browser

- **↑/k, ↓/j**: Navigate
- **Enter**: View details
- **c**: Copy to clipboard
- **e**: Export to file
- **d**: Delete prompt
- **q**: Quit

### Creating a New Prompt

```bash
~/Projects/ai/scripts/prompt-lib add
```

Follow the interactive prompts:
1. Enter name
2. Enter category
3. Enter tags (comma-separated)
4. Type positive prompt (Ctrl+D when done)
5. Type negative prompt (Ctrl+D when done)
6. Optionally add settings
7. Optionally add notes

### Exporting & Sharing

Export a prompt to share:
```bash
~/Projects/ai/scripts/prompt-lib export fantasy-landscape ~/fantasy.txt
```

Import prompts from others:
```bash
~/Projects/ai/scripts/prompt-lib import ~/downloaded-prompts.json
```

## Portability

This prompt library is **fully portable**:

- ✅ Works with AI Hub TUI
- ✅ Works standalone via CLI
- ✅ Plain JSON files (use with any tool)
- ✅ Export to text (copy anywhere)
- ✅ Version control friendly (git)
- ✅ Easy backup/sync (rsync, dropbox, etc.)

### Sync to Cloud

```bash
# Sync to cloud storage
rsync -av ~/Projects/ai/prompts/ ~/Dropbox/prompts/

# Or use git
cd ~/Projects/ai/prompts
git init
git add .
git commit -m "My prompt library"
git remote add origin <your-repo>
git push
```

### Use on Another Machine

```bash
# Copy the entire library
scp -r user@machine:~/Projects/ai/prompts ~/Projects/ai/

# Or clone from git
git clone <your-repo> ~/Projects/ai/prompts
```

## Sample Prompts Included

- `cyberpunk-portrait` - Futuristic neon portrait
- `fantasy-landscape` - Magical forest scene
- `photorealistic-portrait` - Professional photo style
- `anime-character` - Anime illustration style
- `product-photography` - Commercial product shots

## Tips

1. **Organize with tags**: Use descriptive tags for easy searching
2. **Categories**: Use categories like `portrait`, `landscape`, `product`, `anime`
3. **Version control**: Keep your prompts in git for history tracking
4. **Backup regularly**: These prompts are valuable, back them up!
5. **Share with team**: Export/import makes collaboration easy

## Advanced: Custom Scripts

The JSON format is easy to parse in any language:

### Python Example
```python
import json
from pathlib import Path

prompts_dir = Path.home() / "Projects/ai/prompts/comfyui"
prompt = json.loads((prompts_dir / "cyberpunk-portrait.json").read_text())
print(prompt["positive"])
```

### Bash Example
```bash
# Get positive prompt
jq -r '.positive' ~/Projects/ai/prompts/comfyui/cyberpunk-portrait.json
```

## Integration with ComfyUI

To use these prompts in ComfyUI:

1. Browse prompt library
2. Copy prompt (press 'c' in TUI)
3. Paste into ComfyUI positive prompt field
4. Use settings if included (steps, cfg, sampler)

Or export to file for reference:
```bash
~/Projects/ai/scripts/prompt-lib export fantasy-landscape ~/comfy-prompt.txt
```

## Contributing

Found a great prompt? Share it!

1. Export your prompt
2. Share the JSON file
3. Others can import with: `prompt-lib import your-prompt.json`
