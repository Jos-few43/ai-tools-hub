# AI Models Repository

Central storage for all AI models used across different tools and frameworks.

## Directory Structure

```
~/Projects/ai/models/
├── checkpoints/          # Stable Diffusion checkpoints (13GB)
│   ├── epicrealismXL_pureFix.safetensors (6.5GB)
│   ├── realisticVisionV60B1_v51HyperVAE.safetensors (2.0GB)
│   └── v1-5-pruned-emaonly.safetensors (4.0GB)
├── loras/                # LoRA models
├── vae/                  # VAE models
├── embeddings/           # Textual inversion embeddings
└── stable-diffusion/     # Additional SD models
```

## Model Sharing

Models are shared across tools using symlinks:

### ComfyUI
- **Original location:** `~/Projects/comfy/ComfyUI/models/checkpoints/`
- **Symlink:** `~/Projects/comfy/ComfyUI/models/checkpoints-link` → `~/Projects/ai/models/checkpoints/`
- **Usage:** ComfyUI can access shared checkpoints via the symlink

### Stable Diffusion WebUI
- **Original location:** `~/Projects/ai/stable-diffusion-webui/models/Stable-diffusion/`
- **Symlink:** `~/Projects/ai/stable-diffusion-webui/models/Stable-diffusion-shared` → `~/Projects/ai/models/checkpoints/`
- **Usage:** SD-WebUI can access shared checkpoints via the symlink

## Current Models

### Checkpoints (13GB)

| Model | Size | Type | Use Case |
|-------|------|------|----------|
| epicrealismXL_pureFix | 6.5GB | SDXL | Photorealistic images, high quality |
| realisticVisionV60B1_v51HyperVAE | 2.0GB | SD1.5 | Realistic portraits, fast generation |
| v1-5-pruned-emaonly | 4.0GB | SD1.5 | Base model, general purpose |

## Adding New Models

### Method 1: Direct Download
```bash
# Download to shared location
cd ~/Projects/ai/models/checkpoints
wget https://example.com/model.safetensors
```

### Method 2: Move Existing Models
```bash
# Move from ComfyUI
mv ~/Projects/comfy/ComfyUI/models/checkpoints/model.safetensors \
   ~/Projects/ai/models/checkpoints/

# Move from SD-WebUI
mv ~/Projects/ai/stable-diffusion-webui/models/Stable-diffusion/model.safetensors \
   ~/Projects/ai/models/checkpoints/
```

## Model Organization Best Practices

1. **Checkpoints:** Main SD models (SD1.5, SDXL, etc.)
2. **LoRAs:** Style and character modifications
3. **VAE:** Image decoders for better quality
4. **Embeddings:** Textual inversion models

## Disk Usage

Check model storage:
```bash
du -sh ~/Projects/ai/models/*
```

List all checkpoints:
```bash
ls -lh ~/Projects/ai/models/checkpoints/
```

## Cleanup

Remove unused models:
```bash
# Interactive removal
cd ~/Projects/ai/models/checkpoints
ls -lh
rm model-name.safetensors
```

## Symlink Verification

Check that symlinks are working:
```bash
# ComfyUI
ls -la ~/Projects/comfy/ComfyUI/models/checkpoints-link

# SD-WebUI
ls -la ~/Projects/ai/stable-diffusion-webui/models/Stable-diffusion-shared
```

---

**Last Updated:** 2025-12-31
