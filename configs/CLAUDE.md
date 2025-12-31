# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a multi-AI coordination workspace that orchestrates specialized AI agents for research, code generation, review, and real-time intelligence gathering. The system integrates Claude Code with Google Gemini (research), OpenAI GPT-4 (code generation), X.AI Grok (real-time info), and Ollama (local GPU-based code review).

## Architecture

### Agent System
The workspace uses Claude Code's agent system with four specialized agents:

- **@gemini-research** - Web research and fact-checking (1M token context, cloud)
- **@ollama-codereview** - Privacy-safe local code review (RTX 3060 GPU, 100% local)
- **@codex-generator** - Fast code scaffolding and boilerplate (OpenAI GPT-4, cloud)
- **@grok-realtime** - Real-time information and social sentiment analysis (X.AI, cloud)

Agent definitions are in `.claude/agents/*.md` with system prompts, available tools, output formats, and constraints.

### Workflow Commands (Skills)
Multi-agent workflows are defined in `.claude/commands/*.md`:

- `/deep-research` - Comprehensive research via @gemini-research
- `/private-review` - Local code review via @ollama-codereview
- `/scaffold` - Code generation via @codex-generator
- `/status-check` - Real-time status via @grok-realtime
- `/collab-research` - Combined @grok-realtime + @gemini-research workflow
- `/full-pipeline` - Generate code with @codex-generator then review with @ollama-codereview
- `/agent-status`, `/ai-status` - System health checks

### Hook System
Automated hooks in `.claude/hooks-scripts/*.sh` triggered by Claude Code events:

**SessionStart** (`session-init.sh`)
- Displays multi-AI system status (Ollama, MCP server, API keys, GPU memory)

**UserPromptSubmit** (`analyze-intent.sh`)
- Suggests relevant agents based on prompt keywords

**PreToolUse** (`detect-secrets.sh`)
- Blocks cloud API calls containing secrets (API keys, tokens)
- Enforces privacy: sensitive code must use @ollama-codereview

**PostToolUse** (`post-edit-format.sh`)
- Runs after Edit/Write operations

**SubagentStop** (`subagent-report.sh`)
- Logs agent execution metrics (duration, tokens)

**Stop** (`session-summary.sh`)
- Session cleanup and summary

### MCP Integration
The `multi-ai-coordinator` MCP server (enabled in `.claude/settings.local.json`) provides tools:
- `gemini_research` - Google Gemini research with citations
- `ollama_code_review` - Local Ollama inference for code review
- `codex_generate` - OpenAI code generation
- `grok_realtime` - X.AI real-time intelligence

### Privacy Model
The system enforces strict privacy boundaries:

- **Cloud agents** (@gemini-research, @codex-generator, @grok-realtime) - Public/research code only
- **Local agent** (@ollama-codereview) - Proprietary/sensitive code stays on GPU
- **Secret detection** - PreToolUse hook blocks cloud transmission of API keys/tokens

## Configuration

### API Keys
Required API keys in `.env`:
```
GEMINI_API_KEY
ANTHROPIC_API_KEY
OPENAI_API_KEY
XAI_API_KEY
DEEPSEEK_API_KEY
DASHSCOPE_API_KEY
```

### Permissions
`.claude/settings.json` and `.claude/settings.local.json` define:
- Allowed bash commands (gemini-cli, openai, grok-cli, ollama, systemctl, etc.)
- Hook configurations
- Enabled MCP servers

### GPU Requirements
- RTX 3060 GPU required for @ollama-codereview
- Check status: `nvidia-smi` or via SessionStart hook
- Ollama must be running: `ollama list`

## Agent Selection Guide

**Use @gemini-research when:**
- Conducting deep research with citations
- Fact-checking claims
- Analyzing large documents (up to 1M tokens)
- Need historical context or comprehensive analysis

**Use @ollama-codereview when:**
- Reviewing proprietary or sensitive code
- Security audits of private code
- Code must not leave local machine
- GPU-based inference acceptable

**Use @codex-generator when:**
- Creating boilerplate/scaffolding
- Generating function implementations
- Writing tests from specifications
- Converting pseudocode to code

**Use @grok-realtime when:**
- Checking current service status
- Monitoring breaking news/events
- Analyzing X/Twitter sentiment
- Need real-time information (< 15 min old)

**Multi-agent workflows:**
- `/collab-research` - Combine real-time + historical research
- `/full-pipeline` - Generate then review code

## Rate Limits & Costs

- **Gemini**: 60 requests/minute, 1-hour cache
- **OpenAI**: 3500 requests/minute, ~$0.002/1K tokens
- **Grok**: Varies by endpoint, 15-minute cache
- **Ollama**: No limits (local GPU)

## Important Notes

- Hook scripts expect paths at `/home/yish/Projects/claude-workspace/.claude/hooks-scripts/` - update if repository moved
- Secret detection uses regex patterns in `detect-secrets.sh` - extend for custom secret formats
- All agents have specific output formats - see `.claude/agents/*.md` for details
- Ollama models used: codellama:13b-instruct, deepseek-coder:6.7b
