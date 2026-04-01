# AGENTS.md

## Overview

This file provides guidence to Copilot (github.com/copilot) when working with code in this repository.

## Project Nature

This is a **PRP (Product Requirement Prompt) Framework** repository, not a traditional software project.  
Core Concept: **"PRP = PRD + curated codebase intelligence + agent/runbook"**. It is designed to enable AI agents to ship production-ready code on the first pass.

## Core Architecture

### Command-Driven System

- **Pre-configured commands**: Located in `.github/prompts/`. AI agents should prioritize these commands for standard tasks.

### Template-Based Methodology

- **PRP Templates**: Located in `.github/PRPs/templates/` follow a structured format with built-in validation loops.
- **Context-Rich Approach**: Every PRP must include comprehensive documentation, examples, and known "gotchas".
- **Validation-First Design**: Each PRP contains executable validation gates covering syntax, tests, and integration.

### AI Documentation Curation

- `.github/PRPs/ai_docs/`: Curated documentation for context injection.
- `.github/agents_md_files/`: Programming language- or framework-specific examples of `AGENTS.md`.

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
```

### Key Copilot Commands

**Core PRP Workflow**:
- `/prp-prd`: Create a comprehensive feature PRD with deep codebase analysis.
- `/prp-plan`: Create a detailed plan with phases, tasks, and validation.
- `/prp-implement`: Implement feature following PRP methodology.
- `/prp-commit`: Create atomic git commits based on changes.
- `/prp-pr`: Push changes and create a PR with comprehensive description.

**Agent Skills**:
- `prp-core-runner`: An autonomous skill that orchestrates the complete PRP workflow.

**Legacy & Utilities**:

- **Workflows**: `/prp-story-create`, `/prp-story-execute`, `/prp-base-create`, `/prp-base-execute`, `/prp-planning-create`.
- **Utilities**: `/prime-core` (Project context), `/review-staged-unstaged` (PRP-based review), `/smart-commit` (AI analysis).

## Critical Success Patterns

### The PRP Methodology

1. **Context is King**: Include ALL necessary documentation, examples, and gotchas.
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix autonomously.
3. **Information Density**: Use specific keywords and patterns established in the codebase.
4. **Progressive Success**: Start simple, validate the foundation, then enhance.

### PRP Structure Requirements

A valid PRP must contain:

- **Goal**: Specific end state and desired outcome.
- **Why**: Business value and user impact.
- **What**: User-visible behavior and technical requirements.
- **Context**: Documentation URLs, code examples, gotchas, and patterns.
- **Implementation Blueprint**: Detailed pseudocode and task lists.
- **Validation Loop**: Executable commands for syntax, tests, integration.

### Validation Gates (Must be Executable)

1. **Syntax & Style**: `ruff check --fix && mypy .`
2. **Unit Tests**: `uv run pytest tests/ -v`
3. **Integration**: `uv run uvicorn main:app --reload` followed by API calls `curl -X POST http://localhost:8000/endpoint -H "Content-Type: application/json" -d '{...}'`
4. **Deployment**: MCP servers or creative self-validation methods.

## Anti-Patterns to Avoid

- **Minimal Context**: Never provide bare prompts. Context is everything; the PRP must be self-contained.
- **Skipping Validation**: Validation is critical for one-pass success. The better the AI runs the loop, the higher the success rate.
- **Ignoring Structure**: Do not deviate from the battle-tested structured PRP format.
- **Redundant Patterns**: Use existing templates rather than creating new patterns unnecessarily.
- **Hardcoding**: Avoid hardcoded values that belong in configuration.
- **Generic Exceptions**: Do not use "catch-all" exception handling; be specific.

## Working with This Framework

### When Creating new PRPs

1. **Context Assembly**: Gather documentation, code examples, and patterns. Context is King!
2. **Blueprint Development**: Draft a detailed Implementation Blueprint with pseudocode and task lists.
3. **Validation Mapping**: Define executable commands (syntax, tests, integration) for the Validation Loop.

### When Executing PRPs (Agent Instructions)

1. **Load PRP**: Read and understand all context and requirements.
2. **ULTRATHINK**: (Reasoning Step) Create a comprehensive plan, break it down into todos, use subagents, and check `.github/PRPs/ai_docs/`.
3. **Execute**: Implement following the provided blueprint.
4. **Validate**: Run every validation command; fix failures immediately.
5. **Complete**: Ensure every checklist item is verified as "done".

## Project Structure Understanding

```
.github/
   prompts/                # Pre-configured Copilot commands
   PRPs/
      templates/             # PRP templates with validation
      ai_docs/              # Curated Copilot documentation
      scripts/              # PRP runner and utilities
   agents_md_files/       # Language/Framework-specific AGENTS.md examples
```
