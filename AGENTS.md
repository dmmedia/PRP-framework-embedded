# AGENTS.md

> **Primary guide for GitHub Copilot + VS Code agent migrations and workflows.**

## Overview

This document is the centralized entry point for using PRP workflows via Copilot and VS Code in this repository.

## Goals

- Replace Claude-specific agent docs with Copilot/VS Code alternatives.
- Provide quick links to migration guides in `copilot_md_files/`.
- Provide backward-compatible deprecation steps for `claude_md_files/`.

## Files

- `copilot_md_files/COPILOT-*.md` - Copilot migration guides.
- `claude_md_files/CLAUDE-*.md` - Deprecated reference docs with deprecation headers.
- `CLAUDE.md` - Legacy main entry, now pointing to this `AGENTS.md` as preferred.
- `README.md` - top-level actions for Copilot agents.

## Quick Start

1. Open `AGENTS.md` to find your workflow (Python/Node/Rust etc.).
2. Use `.github/PRPs/scripts/prp_workflow.py` with plan and implementation commands:
   - `uv run .github/PRPs/scripts/prp_workflow.py --no-commit --no-pr "<feature>"`
   - `uv run .github/PRPs/scripts/prp_workflow.py --skip-create --prp-path .claude/PRPs/plans/<plan>.md --no-pr`
3. Confirm your environment with:
   - `uv run lint && uv run type-check`
   - `uv run pytest` (if tests available)

## Migration Status (Phase 6)

- [x] All `claude_md_files` have Copilot equivalents.
- [x] `docs_map.json` maps legacy names to Copilot paths.
- [x] `README.md` and `CLAUDE.md` link to `AGENTS.md`.

## Agent Patterns

- `prp-core-*` commands: used as the top-level PRP workflow.
- `prp-issue-*`: issue-based investigation and fix.
- `prp-plan`: generate plans from PRDs.
- `prp-implement`: execute plans with validation loops.

## Copilot command examples

- `/prp-plan "migrate docs to copilot"`
- `/prp-implement .claude/PRPs/plans/migrate-prp-framework-to-github-copilot-vscode-phase-6.plan.md`

## Link references

- `copilot_md_files/COPILOT-PYTHON-BASIC.md`
- `copilot_md_files/COPILOT-NODE.md`
- `copilot_md_files/COPILOT-REACT.md`
- `copilot_md_files/COPILOT-RUST.md`
- `copilot_md_files/COPILOT-ASTRO.md`
- `copilot_md_files/COPILOT-JAVA-GRADLE.md`
- `copilot_md_files/COPILOT-JAVA-MAVEN.md`
- `copilot_md_files/COPILOT-NEXTJS-15.md`

## Notes

- Keep this file synched with new features in `copilot_md_files/`.
- Do not use `claude_md_files` directly for new implementations; those are archive-only.
