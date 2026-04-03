---
description: Cancel active PRP Ralph loop
---

# Cancel PRP Ralph Loop

---

## Steps

1. **Check if loop is active**:

   ```bash
   test -f .claude/prp-ralph.state.md && echo "ACTIVE" || echo "NOT_FOUND"
   ```

2. **If NOT_FOUND**: Report "No active Ralph loop found."

3. **If ACTIVE**:

   a. Read the state file to get current iteration:

   ```bash
   head -20 .claude/prp-ralph.state.md
   ```

   b. Extract iteration number from the YAML frontmatter

   c. Remove the state file:

   ```bash
   rm .claude/prp-ralph.state.md
   ```

   d. Report:

> **Output Template**: See `.github/PRPs/templates/prp-ralph-cancel.prompt-cancel-template.md`
> Load this file and use its structure exactly when generating output.
