# COPILOT-PYTHON-BASIC.md

> **MIGRATED: This guide is for GitHub Copilot and VS Code workflows.**

This file provides comprehensive guidance for using Copilot and VS Code with Python code in this repository.

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)
Simplicity is key. Choose straightforward solutions over complex ones. Simple code is easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)
Only implement features when needed. Avoid speculative development.

### Design Principles
- **Dependency Inversion**: High-level modules and low-level modules depend on abstractions.
- **Open/Closed Principle**: Software entities are open for extension, closed for modification.
- **Single Responsibility**: Each function, class, and module should have one clear purpose.
- **Fail Fast**: Validate early and raise errors immediately.

## 🧑‍💻 Code Structure & Modularity

- **Files < 500 lines**; split into modules if larger.
- **Functions < 50 lines**; single responsibility.
- **Classes < 100 lines**; single concept.
- **Organize by feature/responsibility.**
- **Line length ≤ 100 chars** (see ruff in pyproject.toml).

### Project Architecture

Follow vertical slice architecture with tests next to code:

```
src/project/
    __init__.py
    main.py
    tests/
        test_main.py
    conftest.py
    # Core modules
    database/
        __init__.py
        connection.py
        models.py
        tests/
            test_connection.py
            test_models.py
    auth/
        __init__.py
        authentication.py
        authorization.py
        tests/
            test_authentication.py
            test_authorization.py
```

> For Copilot: Use inline comments and docstrings to provide context for Copilot suggestions. Validate Copilot output with ruff and mypy.