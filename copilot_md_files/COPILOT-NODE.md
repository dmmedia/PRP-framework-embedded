# COPILOT-NODE.md

> **MIGRATED: This guide is for GitHub Copilot and VS Code workflows.**

This file provides comprehensive guidance for using Copilot and VS Code with Node.js applications in this repository.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Simplicity is key. Choose straightforward solutions over complex ones. Simple code is easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)
Only implement features when needed. Avoid speculative development.

### Design Principles
- **Modular Architecture**: Build with small, focused modules.
- **Error-First**: Always handle errors first in callbacks.
- **Async by Default**: Use async/await for I/O.
- **Fail Fast**: Validate inputs early and throw errors immediately.
- **Security First**: Always validate and sanitize user input.

## 🤖 Copilot Assistant Guidelines

- Always check existing patterns before implementing features.
- Prefer composition over inheritance.
- Use existing utilities before creating new ones.
- Avoid duplicate functionality and unnecessary dependencies.
- Write tests before implementation (TDD preferred).
- Break complex tasks into smaller, testable units.
- Validate understanding before implementation.

### Search Command Requirements
**CRITICAL**: Use VS Code's search or `rg` (ripgrep) for codebase queries. Avoid legacy `grep`/`find` patterns.

> For Copilot: Use inline comments and JSDoc to provide context for Copilot suggestions. Validate Copilot output with ESLint and type-checking.