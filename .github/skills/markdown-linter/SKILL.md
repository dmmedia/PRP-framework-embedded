---
name: markdown-linter
description: Formats markdown files and checks for common issues.
license: MIT
metadata:
   author: "dmmedia"
   version: "1.0"
compatibility: Requires Python 3.12+, uv, mdformat and pymarkdownlnt.
---

# Markdown validation guide

## Overview

This guide covers essential markdown formatting and linting using Python libraries and command-line tools.

## Quick Start

```console
uv run mdformat path/to/document.md
uv run pymarkdownlnt -c .github/skills/markdown-linter/config/pymarkdown.toml scan path/to/document.md
```
