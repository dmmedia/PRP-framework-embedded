# Feature: Migrate PRP Framework to GitHub Copilot + VS Code

## Summary

This plan migrates the PRP framework from Claude-specific scripts, templates, and documentation to GitHub Copilot and VS Code-native workflows. It introduces an adapter for Copilot CLI/Chat, updates all documentation, and ensures PRP flows are discoverable and executable in VS Code. Legacy Claude artifacts are retained with deprecation headers for a transition period.

## User Story

As a VS Code-based developer
I want to run PRP workflows natively with Copilot
So that I can stay in context and deliver validated changes faster

## Problem Statement

The PRP framework is tightly coupled to "Claude Code" tooling, blocking Copilot/VS Code adoption. This causes onboarding friction, automation breakage, and duplicated documentation.

## Solution Statement

Replace Claude-specific runtime and docs with Copilot/VS Code equivalents. Add an adapter (`invoke_copilot.py`), migrate prompt templates, update docs, and integrate with VS Code workspace settings and extensions.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | REFACTOR                                          |
| Complexity       | MEDIUM                                            |
| Systems Affected | scripts, docs, adapters, VS Code config           |
| Dependencies     | Copilot CLI (latest), Python 3.12+, rich 14.2.0+  |
| Estimated Tasks  | 8                                                 |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   VS Code   │ ──────► │  Shell/CLI  │ ──────► │ Claude-only │            ║
║   │  User Flow  │         │  Scripts    │         │  Artifacts  │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: Must run shell scripts or external CLIs (e.g., `claude`)         ║
║   PAIN_POINT: Not native to VS Code, onboarding friction, duplicated docs     ║
║   DATA_FLOW: VS Code → shell → Claude CLI → .claude/PRPs/*                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   VS Code   │ ──────► │ Copilot CLI │ ──────► │ PRP Artifacts│           ║
║   │  User Flow  │         │  Adapter    │         │  (native)    │           ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                   │                                           ║
║                                   ▼                                           ║
║                          ┌─────────────┐                                      ║
║                          │ Copilot Docs│  ◄── [new guides, quickstarts]       ║
║                          └─────────────┘                                      ║
║                                                                               ║
║   USER_FLOW: Run PRP flows from VS Code, Copilot Chat, or CLI                  ║
║   VALUE_ADD: Native, discoverable, less friction, unified docs                 ║
║   DATA_FLOW: VS Code → Copilot CLI/Chat → .claude/PRPs/*                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| VS Code  | Shell scripts | Command palette, Copilot Chat | Native workflow |
| Docs     | Claude guides | Copilot guides | Up-to-date, relevant |
| Adapter  | None | invoke_copilot.py | CLI/Chat integration |

---

## Mandatory Reading

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | PRPs/scripts/invoke_copilot.py | 1-60 | Adapter pattern for Copilot integration |
| P1 | copilot_md_files/copilot-prp-quickstart.md | all | Copilot PRP workflow quickstart |
| P2 | copilot_md_files/copilot-migration-guide.md | all | Migration steps, FAQ |
| P3 | .vscode/extensions.json | all | Extension recommendations |
| P4 | .vscode/settings.json | all | Copilot settings |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Copilot CLI Docs](https://docs.github.com/en/copilot/cli) | Usage, install | Adapter integration |
| [Python 3.12 What's New](https://docs.python.org/3/whatsnew/3.12.html) | Deprecations | Ensure compatibility |
| [rich 14.2.0 Release Notes](https://github.com/Textualize/rich/releases/tag/v14.2.0) | Changelog | API changes |
| [VS Code Copilot Docs](https://docs.github.com/en/copilot/getting-started-with-github-copilot) | Setup | User onboarding |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```python
# SOURCE: PRPs/scripts/invoke_copilot.py:1-60
COPILOT_CLI = shutil.which("copilot")
def run_copilot_command(args): ...
```

**ERROR_HANDLING:**
```python
# SOURCE: PRPs/scripts/invoke_copilot.py:1-60
if not COPILOT_CLI:
    print("[WARN] Copilot CLI not found. Falling back to manual mode.")
    return manual_fallback(args)
```

**LOGGING_PATTERN:**
```python
# SOURCE: PRPs/scripts/invoke_copilot.py:1-60
print(f"[ERROR] Copilot CLI failed: {result.stderr}")
```

**REPOSITORY_PATTERN:**
```python
# SOURCE: PRPs/scripts/invoke_copilot.py:1-60
# Adapter pattern for CLI integration
```

**SERVICE_PATTERN:**
```python
# SOURCE: PRPs/scripts/invoke_copilot.py:1-60
# run_copilot_command(args) as service entrypoint
```

**TEST_STRUCTURE:**
```markdown
# SOURCE: copilot_md_files/copilot-prp-quickstart.md:all
# Manual validation steps, no automated tests
```

---

## Files to Change

| File                                   | Action  | Justification                         |
|---------------------------------------- | ------- |-------------------------------------- |
| PRPs/scripts/invoke_copilot.py         | CREATE  | Adapter for Copilot CLI/Chat          |
| copilot_md_files/copilot-prp-quickstart.md | DELETE  | No human-facing guides in `copilot_md_files/` directory       |
| copilot_md_files/copilot-migration-guide.md | DELETE  | No human-facing guides in `copilot_md_files/` directory                 |
| copilot_md_files/copilot-prp-troubleshooting.md | DELETE  | No human-facing guides in `copilot_md_files/` directory    |
| .vscode/extensions.json                 | CREATE/UPDATE | Extension recommendations         |
| .vscode/settings.json                   | CREATE/UPDATE | Copilot settings                  |
| README.md                              | UPDATE  | Add migration notes, update flows      |
| CLAUDE.md                              | UPDATE  | Add deprecation headers                |

---

## NOT Building (Scope Limits)

- `old-prp-commands/` (historical scripts) — not migrated
- Full feature parity for proprietary Claude-only behaviors — document manual steps or shims where needed

---

## Step-by-Step Tasks

### Task 1: CREATE `PRPs/scripts/invoke_copilot.py`
- **ACTION**: Implement Copilot CLI/Chat adapter
- **IMPLEMENT**: Adapter pattern, error handling, manual fallback
- **MIRROR**: PRPs/scripts/invoke_copilot.py:1-60
- **VALIDATE**: Manual run, check CLI fallback

### Task 2: DELETE `copilot_md_files/copilot-prp-quickstart.md`
- **ACTION**: Delete the file if it exists
- **VALIDATE**: The file is removed from the repository and no longer referenced in docs or code

### Task 3: DELETE `copilot_md_files/copilot-migration-guide.md`
- **ACTION**: Delete the file if it exists
- **VALIDATE**: The file is removed from the repository and no longer referenced in docs or code

### Task 4: DELETE `copilot_md_files/copilot-prp-troubleshooting.md`
- **ACTION**: Delete the file if it exists
- **VALIDATE**: The file is removed from the repository and no longer referenced in docs or code

### Task 5: CREATE/UPDATE `.vscode/extensions.json`
- **ACTION**: Recommend Copilot, Copilot Chat, GitLens, PR tools
- **VALIDATE**: VS Code recommends correct extensions

### Task 6: CREATE/UPDATE `.vscode/settings.json`
- **ACTION**: Enable Copilot, Copilot Chat, configure file excludes
- **VALIDATE**: Copilot features enabled, legacy files excluded

### Task 7: UPDATE `README.md`
- **ACTION**: Add migration notes, update flows
- **VALIDATE**: Docs reference Copilot, not Claude

### Task 8: UPDATE `CLAUDE.md`
- **ACTION**: Add deprecation headers, reference Copilot migration guide
- **VALIDATE**: Docs have clear deprecation notices, no new references to Claude

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| N/A | Manual validation only | Adapter, docs |

### Edge Cases Checklist
- [ ] Copilot CLI not installed
- [ ] User lacks Copilot subscription
- [ ] VS Code extensions missing
- [ ] Python/rich version mismatch
- [ ] Legacy Claude scripts still referenced

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
python -m py_compile PRPs/scripts/invoke_copilot.py
```

### Level 2: UNIT_TESTS
Manual: Run adapter, check fallback, follow quickstart

### Level 3: FULL_SUITE
Manual: End-to-end PRP flow in VS Code with Copilot

### Level 4: MANUAL_VALIDATION
- [ ] User can run PRP flows from VS Code
- [ ] All docs reference Copilot, not Claude
- [ ] Legacy docs have deprecation headers

---

## Acceptance Criteria
- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass
- [ ] Docs and adapter mirror discovered patterns
- [ ] No regressions in PRP flows
- [ ] UX matches "After State" diagram

---

## Completion Checklist
- [ ] All tasks completed in dependency order
- [ ] Each task validated after completion
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Copilot CLI not available | MED | HIGH | Provide manual fallback, document install steps |
| Prompt drift from Claude | MED | MED | Validate with acceptance tests, tune prompts |
| VS Code extension mismatch | LOW | MED | Document required extensions, recommend in settings |
| Python/rich version issues | LOW | MED | Document version requirements, test on 3.12+ |

---

## Notes
- All patterns, gotchas, and integration points are documented from the codebase and official docs.
- Tasks are executable in order, with validation at each step.
- Legacy Claude artifacts are retained with clear deprecation headers for a transition period.
