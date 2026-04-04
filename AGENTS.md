# AGENTS.md

## Project Nature

This is a **PRP (Product Requirement Prompt) Framework** repository, not a traditional software project.  
Core Concept: **"PRP = PRD + curated codebase intelligence + agent/runbook"**. It is designed to enable AI agents to ship production-ready code on the first pass.

## Development Commands

### PRP Execution

Execute these scripts using the `uv` package manager:

```bash
# Interactive mode (recommended for development)
uv run .github/PRPs/scripts/prp_runner.py --prp [prp-name] --interactive

# Headless mode (for CI/CD)
uv run .github/PRPs/scripts/prp_runner.py --prp [prp-name] --output-format json

# Streaming JSON (for real-time monitoring)
uv run .github/PRPs/scripts/prp_runner.py --prp [prp-name] --output-format stream-json

# Syntax & Style checks
# Python:
uv run ruff check --fix && uv run mypy .
# Markdown:
# Use 'markdown-linter' skill.

# Running Unit Tests:
uv run pytest tests/ -v

# Running Integration Tests:
uv run uvicorn main:app --reload`

# Followed by API calls
curl -X POST http://localhost:8000/endpoint -H "Content-Type: application/json" -d '{...}'
```

## Project Structure

- `.claude/`: obsolete Claude Code specific directory, being phased out in favor of `.github/` structure
   - `PRPs/`: PRP artifacts
      - `plans/`: Plans created based on PRDs
         - `completed/`: Executed plans
      - `PRDs/`: PRDs created from user requests by `/prp-prd` slash command
      - `reports/`: Post-implementation reports
- `.claude-plugin/`: Claude Code specific directory with undetermined purpose
- `.github/`: VS Code and Copilot PRP framework project
   - `agents/`: Pre-configured agents for specific tasks
   - `ai_docs/`: Curated documentation for agents
   - `hooks/`: Automation hooks
   - `prompts/`: Pre-configured VS Code/Copilot slash commands
   - `PRPs/`: PRP artifacts
      - `features/`: Feature-specific PRDs
         - `completed/`: Implemented feature PRDs
      - `scripts/`: PRP runner and utilities
      - `templates/`: PRP templates
   - `skills/`: Autonomous agent skills
- `.venv/`: Virtual environment for Python dependencies
- `.vscode/`: VS Code settings, extensions, tasks
- `agents_md_files/`: Language/Framework-specific `AGENTS.md` examples
- `claude_md_files/`: Obsolete `CLAUDE.md` examples for Claude Code
- `old-prp-commands/`: Obsolete PRP framework developments
- `plugins/`: PRP framework packed as a plugin (for Claude Code only?)
   - `prp-core/`: Core PRP framework plugin. Should be finally a copy of the `.github/` contents
- `PRPs/scripts/`: Obsolete location for scripts, being phased out in favor of `.github/PRPs/scripts/`
- `tests/`: Python unit tests for PRP framework
- `.gitignore`: Git ignore file
- `.python-version`: Python version for `pyenv`/`uv`
- `AGENTS.md`: This file - guidance for agents working with this codebase
- `docs_map.json`: Map of migrated templates from `claude_md_files/` to `agents_md_files/`
- `pyproject.toml`: Python project configuration
- `README-FOR-DUMMIES.md`: Simplified README for non-technical human readers
- `README.md`: Main project README with comprehensive documentation for humans
- `uv.lock`: Dependency lock file for `uv`

## Reference Docs
For task-specific guidance, read the relevant file before starting:
- `.github/ai_docs/` — PRP methodology, validation patterns, anti-patterns
- `.github/prompts/` — Available slash commands and their usage
- `.github/skills/` — Available agent skills and their capabilities

