# Copilot Migration Guide

This document details the migration from Claude-centric PRP workflows to Copilot/VS Code native flows.

## Migration Steps
- Use the new adapter script: PRPs/scripts/invoke_copilot.py
- Update prompt templates to Copilot format
- Reference new documentation in copilot_md_files/

## FAQ
**Q: Can I still use Claude?**
A: Yes, legacy commands are retained for rollback.

**Q: What if Copilot is not available?**
A: The adapter provides a manual fallback.
