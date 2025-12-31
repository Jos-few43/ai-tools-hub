# Contributing to AI Tools Hub

Thank you for your interest in contributing to AI Tools Hub! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** to avoid duplicates
2. **Use the bug report template** when creating a new issue
3. **Include details:**
   - OS and version
   - Python version
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/logs

### Suggesting Features

1. **Check the roadmap** in README.md
2. **Open a discussion** before creating a feature request
3. **Describe the use case** and why it's valuable
4. **Consider implementation** if you're willing to contribute code

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch** from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
6. **Push and create PR**

## 📝 Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-tools-hub.git
cd ai-tools-hub

# Run installation
./install.sh

# Create a development branch
git checkout -b feature/my-feature
```

## 🎨 Code Style

### Python
- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small

### Bash
- Use `#!/bin/bash` shebang
- Quote variables: `"$VAR"`
- Check exit codes
- Add comments for complex logic

### Commits
- Use conventional commits format:
  - `feat: add new feature`
  - `fix: correct bug`
  - `docs: update documentation`
  - `refactor: improve code structure`
  - `test: add tests`
  - `chore: maintenance tasks`

## 🧪 Testing

Before submitting a PR:

1. **Test the TUI**: `./ai-hub`
2. **Test installation**: Run `./install.sh` in a clean environment
3. **Test scripts**: Verify all launcher scripts work
4. **Check for errors**: Review Python tracebacks
5. **Test on your system**: Ensure it works with your setup

## 📋 PR Checklist

- [ ] Code follows project style guidelines
- [ ] Changes are tested and working
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes
- [ ] No sensitive data (API keys, tokens) in code
- [ ] `.gitignore` updated if adding new file types

## 🎯 Priority Areas

We're especially interested in contributions for:

1. **CLI Orchestration** (Phase 1 of roadmap)
   - Tool wrapper commands
   - Pipeline/chaining features
   - Workflow templates
   - Flow playground TUI

2. **Tool Support**
   - Additional AI tool integrations
   - Improved launcher scripts
   - Better error handling

3. **Documentation**
   - Tutorial videos
   - Use case examples
   - Troubleshooting guides

4. **Testing**
   - Unit tests for Python code
   - Integration tests
   - CI/CD workflows

## 🚫 What We Won't Accept

- Code that requires root/sudo unnecessarily
- Features that violate tool ToS or licenses
- Hardcoded credentials or API keys
- Breaking changes without discussion
- Code without proper attribution

## 📖 Resources

- [Architecture Documentation](ARCHITECTURE.md)
- [TUI Guide](TUI-GUIDE.md)
- [Quick Reference](QUICK-REFERENCE.md)

## 💬 Questions?

- Open a [Discussion](https://github.com/yourusername/ai-tools-hub/discussions)
- Check [existing issues](https://github.com/yourusername/ai-tools-hub/issues)
- Read the documentation

## 📄 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

---

Thank you for making AI Tools Hub better! 🎉
