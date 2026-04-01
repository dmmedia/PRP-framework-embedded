# COPILOT-REACT.md

> **MIGRATED: This guide is for GitHub Copilot and VS Code workflows.**

This file provides guidance for using Copilot and VS Code with React applications in this repository.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Simplicity is key. Choose straightforward solutions over complex ones. Simple code is easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)
Only implement features when needed. Avoid speculative development.

### Component-First Architecture
- Build with reusable, composable components.
- Each component should have a single, clear responsibility and be self-contained with its own styles, tests, and logic.

### Performance by Default
- Focus on clean, readable code; let React's compiler handle optimizations.

### Design Principles
- **Vertical Slice Architecture**: Organize by features, not layers.
- **Composition Over Inheritance**: Use React's composition model.
- **Fail Fast**: Validate inputs early (e.g., with Zod), throw errors immediately.

## 🤖 Copilot Assistant Guidelines
- Check existing patterns before implementing features.
- Prefer composition over inheritance.
- Use existing utilities before creating new ones.
- Avoid duplicate functionality and unnecessary dependencies.
- Write tests before implementation (TDD preferred).
- Break complex tasks into smaller, testable units.
- Validate understanding before implementation.

### Search Command Requirements
**CRITICAL**: Use VS Code's search or `rg` (ripgrep) for codebase queries. Avoid legacy `grep`/`find` patterns.

> For Copilot: Use inline comments and JSDoc to provide context for Copilot suggestions. Validate Copilot output with ESLint and type-checking.