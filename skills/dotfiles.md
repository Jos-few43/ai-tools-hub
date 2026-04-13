---
name: dotfiles
description: Manage stateless dotfiles using chezmoi + age encryption. Deploy, encrypt, push configs.
---

# Dotfiles Management Skill

Manage stateless configuration system: chezmoi (dotfiles) + age (encryption) + git (versioning).

## System Architecture

Three-tier setup:
1. **dotfiles-private** (~/.dotfiles-chezmoi) — Chezmoi source, age-encrypted secrets
2. **ai-configs** (~/.config/claude-code-tools/ai-configs) — Public tool configs (Claude, Gemini, etc)
3. **distrobox-configs** (~/.config/claude-code-tools/distrobox-configs) — Container defs (reference)

## Commands

### Apply Configs
```bash
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi apply
```
Deploy all managed files: .bashrc, .npmrc, .litellm/.env, .openclaw/openclaw.json

### Preview Changes
```bash
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi diff
```
Show what `apply` will change before executing.

### List Managed Files
```bash
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi managed
```
Show all files currently managed by chezmoi.

### Show Template Variables
```bash
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi data
```
Display all template variable values (from .chezmoi.toml.tmpl.age).

### Add File to Chezmoi
```bash
cd ~/.dotfiles-chezmoi
chezmoi add ~/.myfile
# Or manually: cp ~/.myfile dot_myfile
```
Add new file to chezmoi management (auto-encrypts if .age).

### Edit Managed File
```bash
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi edit ~/.bashrc
```
Edit in repo source, apply via chezmoi.

### Encrypt Credentials
```bash
cd ~/.dotfiles-chezmoi
age -r age1vfjhaqyt4akrwzsku5r05wypdk63phl0dqnt2xt2cpv42445yfeqnlkw5a myfile > myfile.age
rm myfile
```
Encrypt before committing. Public key: `age1vfjhaqyt4akrwzsku5r05wypdk63phl0dqnt2xt2cpv42445yfeqnlkw5a`

## Key Paths

| Item | Location |
|------|----------|
| Chezmoi source | ~/.dotfiles-chezmoi |
| Age private key | ~/.config/age/key.txt (chmod 600) |
| Chezmoi binary | ~/.local/bin/chezmoi |
| Age binary | ~/.local/bin/age* |
| AI tool configs | ~/.config/claude-code-tools/ai-configs |
| Consolidated repos | ~/.config/claude-code-tools/ |

## Encryption Details

- **Method:** age (X25519)
- **Public key:** age1vfjhaqyt4akrwzsku5r05wypdk63phl0dqnt2xt2cpv42445yfeqnlkw5a
- **Private key:** ~/.config/age/key.txt (never commit, back up offsite)
- **Encrypted files:** .chezmoi.toml.tmpl.age, any .age files in repo

## Template Variables

In `.chezmoi.toml.tmpl.age` [data] section:
- litellm_master_key
- gemini_api_key, groq_api_key
- opencode_api_key, openrouter_api_key
- github_token

Templates reference via `{{ .variable_name }}` in .tmpl files.

## Workflow: Add New Secret

1. Edit ~/.dotfiles-chezmoi/.chezmoi.toml.tmpl (unencrypted)
2. Add key=value under [data]
3. Encrypt: `age -r age1vfjhaqyt4akrwzsku5r05wypdk63phl0dqnt2xt2cpv42445yfeqnlkw5a .chezmoi.toml.tmpl > .chezmoi.toml.tmpl.age && rm .chezmoi.toml.tmpl`
4. Test: `chezmoi -S ~/.dotfiles-chezmoi apply`
5. Commit: `cd ~/.dotfiles-chezmoi && git add -A && git commit -m "Add new secret: XYZ"`
6. Push: `git push`

## Workflow: New Machine Recovery

```bash
# 1. Install tools
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b ~/.local/bin
cd /tmp && wget https://github.com/FiloSottile/age/releases/download/v1.2.0/age-v1.2.0-linux-amd64.tar.gz
tar -xzf age-*.tar.gz && mv age/* ~/.local/bin/

# 2. Restore age key (from secure backup)
mkdir -p ~/.config/age
cp /path/to/backup/key.txt ~/.config/age/key.txt
chmod 600 ~/.config/age/key.txt

# 3. Clone + apply
~/.local/bin/chezmoi init git@github.com:Jos-few43/dotfiles-private.git -S ~/.dotfiles-chezmoi
~/.local/bin/chezmoi -S ~/.dotfiles-chezmoi apply

# 4. Clone ai-configs
git clone https://github.com/Jos-few43/ai-configs.git ~/.config/claude-code-tools/ai-configs
ln -sfv ~/.config/claude-code-tools/ai-configs/{claude,gemini,aider} ~/.config/
```

## Safety Rules

- **Never edit managed files in ~/** — chezmoi overwrites on apply
- **Back up ~/.config/age/key.txt** — loss = permanent data loss
- **Encrypt before git push** — no unencrypted secrets in repo
- **Use ~/.local/bin/chezmoi** — not distro package (may be old)
- **Revoke exposed tokens** — token visible in chat = revoke immediately

## Repos

- dotfiles-private: github.com/Jos-few43/dotfiles-private
- ai-configs: github.com/Jos-few43/ai-configs
- distrobox-configs: github.com/Jos-few43/distrobox-configs

## References

- Chezmoi docs: chezmoi.io
- Age crypto: age-encryption.org
- Current config: ~/.dotfiles-chezmoi/CLAUDE.md + project memory