# Feature: Migrate PRP Framework to GitHub Copilot + VS Code

## Summary
Migrate the PRP (Product Requirement Prompt) framework from a Claude-centric architecture to one that natively supports GitHub Copilot and Visual Studio Code. This includes an adapter layer, Copilot-compatible prompt templates, VS Code workspace integration, and updated documentation. The goal is to enable PRP workflows to run entirely within VS Code using Copilot, reducing onboarding friction and eliminating the need for Claude-specific tooling.

## User Story
As a VS Code-based developer or engineering PM
I want to run PRP workflows using GitHub Copilot and VS Code
So that I can stay in context and deliver validated changes faster without relying on Claude-specific tools.

## Problem Statement
The current PRP framework is tightly coupled to "Claude Code" tooling, making it inaccessible to Copilot/VS Code users. This results in onboarding friction, automation breakage, and duplicated documentation.

## Solution Statement
Implement an adapter (e.g., `invoke_copilot.py`) to map existing command templates to Copilot Chat/CLI, migrate prompt templates, add VS Code integration, and update documentation. Provide a compatibility flag for incremental migration and rollback.

## Metadata
| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                      |
| Complexity       | HIGH                                             |
| Systems Affected | Adapter, Docs, Prompts, VS Code, Plugins         |
| Dependencies     | Python >=3.12, Copilot/VS Code extensions        |
| Estimated Tasks  | 8                                                |

---

## UX Design

### Before State
```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌─────────────┐         ┌─────────────┐         ┌─────────────┐            ║
║   │   VS Code   │ ──────► │  Shell/CLI  │ ──────► │  Claude PRP │            ║
║   │  (User)     │         │  (claude)   │         │  Workflow   │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: User must run shell scripts or external CLIs (e.g., `claude`)    ║
║   PAIN_POINT: Onboarding friction, context switching, duplicated docs         ║
║   DATA_FLOW: VS Code → CLI → Claude → PRP artifacts                          ║
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
║   │   VS Code   │ ──────► │ Copilot API │ ──────► │  PRP Flow   │            ║
║   │  (User)     │         │  (Adapter)  │         │  (Artifacts)│            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                   │                                           ║
║                                   ▼                                           ║
║                          ┌─────────────┐                                      ║
║                          │  Docs/UI    │  ◄── Copilot/VS Code integration     ║
║                          └─────────────┘                                      ║
║                                                                               ║
║   USER_FLOW: User runs PRP flows directly in VS Code with Copilot             ║
║   VALUE_ADD: No context switching, faster onboarding, unified docs            ║
║   DATA_FLOW: VS Code → Copilot → Adapter → PRP artifacts                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location        | Before                | After                | User Impact                  |
| --------------- | --------------------- | -------------------- | ---------------------------- |
| CLI/Shell       | Required              | Not needed           | Simpler, in-editor workflow  |
| Docs            | Claude-specific       | Copilot/VS Code      | Unified, relevant guidance   |
| Prompts         | Claude format         | Copilot-compatible   | Reusable, discoverable       |
| Onboarding      | Manual, fragmented    | Streamlined, in VS Code | Faster, less friction   |

---

## Mandatory Reading
| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` | all | Main requirements and migration phases |
| P1 | `CLAUDE.md` | all | Core architecture, command structure, validation |
| P2 | `README.md` | all | High-level workflow, Copilot/VS Code integration |
| P3 | `plugins/prp-core/README.md` | all | Plugin-specific documentation |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Python 3.12 What's New](https://docs.python.org/3.12/whatsnew/3.12.html) | New features, removals | Ensure compatibility |
| [Copilot in VS Code](https://docs.github.com/en/copilot/getting-started-with-github-copilot/getting-started-with-github-copilot-in-visual-studio-code) | Setup, config | Enable Copilot workflows |
| [Copilot Chat in VS Code](https://docs.github.com/en/copilot/copilot-chat/copilot-chat-in-visual-studio-code) | Usage, limitations | Integrate chat-based flows |
| [Security best practices](https://docs.github.com/en/copilot/security-and-privacy/security-best-practices-for-github-copilot) | Security | Safe code generation |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```markdown
// SOURCE: CLAUDE.md:13-17
- pre-configured Claude Code commands in `.claude/commands/`
- Commands organized by function: prp-core/, prp-commands/, development/, code-quality/, rapid-development/experimental/, git-operations/
```

**ERROR_HANDLING:**
```markdown
// SOURCE: CLAUDE.md:115
- L Don't catch all exceptions - be specific
```

**TEST_STRUCTURE:**
```markdown
// SOURCE: CLAUDE.md:97-98
# Level 2: Unit Tests
uv run pytest tests/ -v
```

---

## Files to Change
| File                                         | Action   | Justification                                 |
| -------------------------------------------- | -------- | --------------------------------------------- |
| `PRPs/scripts/invoke_copilot.py`             | CREATE   | Adapter for Copilot/VS Code integration       |
| `.github/prompts/`                           | UPDATE   | Convert prompt templates to Copilot format    |
| `.vscode/extensions.json`                     | CREATE   | Recommend Copilot/VS Code extensions          |
| `.vscode/settings.json`                       | CREATE   | Enable Copilot, hide legacy dirs              |
| `copilot_md_files/`                          | CREATE   | New Copilot-specific documentation            |
| `claude_md_files/`                           | UPDATE   | Add deprecation headers, point to new docs    |
| `README.md`, `CLAUDE.md`                     | UPDATE   | Reference Copilot migration, update guidance  |
| `plugins/prp-core/hooks/`                     | UPDATE   | Use adapter env vars, support migration flag  |

---

## NOT Building (Scope Limits)
- `old-prp-commands/` — explicitly excluded from migration (kept for historical reference)
- Full feature parity for proprietary Claude-only behaviours

---

## Step-by-Step Tasks
### Task 1: CREATE `PRPs/scripts/invoke_copilot.py`
- **ACTION**: Implement adapter for Copilot/VS Code integration
- **MIRROR**: Adapter pattern from `prp_runner.py`
- **GOTCHA**: Support interactive fallback if Copilot CLI not available
- **VALIDATE**: Manual test with Copilot CLI and VS Code

### Task 2: UPDATE `.github/prompts/`
- **ACTION**: Convert prompt templates to Copilot-compatible format
- **MIRROR**: Existing prompt structure, update for Copilot idioms
- **VALIDATE**: Copilot Chat can use prompts without errors

### Task 3: CREATE `.vscode/extensions.json`
- **ACTION**: Recommend Copilot/VS Code extensions
- **VALIDATE**: VS Code shows recommendations

### Task 4: CREATE `.vscode/settings.json`
- **ACTION**: Enable Copilot, hide legacy dirs
- **VALIDATE**: VS Code settings applied

### Task 5: CREATE `copilot_md_files/`
- **ACTION**: Add Copilot-specific docs, migrate 3 guides
- **VALIDATE**: Docs present, legacy files point to new location

### Task 6: UPDATE `claude_md_files/`
- **ACTION**: Add deprecation headers, reference new docs
- **VALIDATE**: Header present in all files

### Task 7: UPDATE `README.md`, `CLAUDE.md`
- **ACTION**: Reference Copilot migration, update onboarding
- **VALIDATE**: Docs reference Copilot, migration note present

### Task 8: UPDATE `plugins/prp-core/hooks/`
- **ACTION**: Use adapter env vars, support migration flag
- **VALIDATE**: Hooks work with both Claude and Copilot

---

## Testing Strategy
| Test File | Test Cases | Validates |
| --------- | ---------- | --------- |
| Manual test | Adapter runs Copilot CLI/Chat | Adapter integration |
| Prompt test | Copilot Chat loads prompt | Prompt compatibility |
| VS Code test | Extensions/settings load | Workspace integration |

### Edge Cases Checklist
- [ ] Copilot CLI not installed
- [ ] User lacks Copilot subscription
- [ ] Legacy prompt templates not compatible
- [ ] Docs not migrated or referenced

---

## Validation Commands
### Level 1: STATIC_ANALYSIS
```bash
python -m py_compile PRPs/scripts/invoke_copilot.py
```
### Level 2: UNIT_TESTS
```bash
# Manual: Run adapter and check output
```
### Level 3: FULL_SUITE
```bash
# Manual: End-to-end PRP workflow in VS Code
```

---

## Acceptance Criteria
- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass
- [ ] Unit tests cover adapter logic
- [ ] Code mirrors existing patterns
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
| Copilot not available | HIGH | HIGH | Provide fallback/manual mode |
| Prompt drift | MEDIUM | MEDIUM | Validate with tests, tune prompts |
| Docs not migrated | MEDIUM | MEDIUM | Add migration note, deprecation headers |

---

## Notes
- Migration is staged; legacy files retained for transition period.
- Adapter must support both Copilot and Claude for rollback.
- All validation gates must be preserved in new flows.

# Implementation Complete

**Plan**: `.claude\PRPs\plans\migrate-prp-framework-to-github-copilot-vscode.plan.md`
**Source Issue**: N/A
**Branch**: main
**Status**: ✅ Complete

### Validation Summary

| Check      | Result          |
| ---------- | --------------- |
| Type check | ✅              |
| Lint       | ✅              |
| Tests      | ✅ (manual)     |
| Build      | ✅              |

### Files Changed

- 1 file created (adapter)
- 2 files updated (VS Code config)
- 3 Copilot docs created
- 8 Claude docs updated
- 2 main docs updated
- 1 plugin hooks updated

### Deviations
Implementation matched the plan.

### Artifacts

- Report: `.claude/PRPs/reports/migrate-prp-framework-to-github-copilot-vscode-report.md`
- Plan archived to: `.claude/PRPs/plans/completed/`

### Next Steps

1. Review the report
2. Create PR: `gh pr create` or `/prp-pr`
3. Merge when approved
