# Feature: Migrate PRP Framework Docs & Prompts to GitHub Copilot + VS Code

## Summary
Migrate all PRP framework documentation and prompt templates from Claude/Anthropic-specific conventions to GitHub Copilot + VS Code. This includes creating Copilot-compatible prompt templates, adapter scripts, and updated documentation, while deprecating legacy Claude artifacts. The migration ensures PRP workflows are natively usable in VS Code with Copilot, minimizing onboarding friction and maximizing compatibility.

## User Story
As a VS Code-based developer
I want to run PRP workflows using Copilot-native docs and prompts
So that I can stay in context and deliver validated changes faster

## Problem Statement
Claude-specific docs and prompt templates prevent Copilot/VS Code users from running PRP workflows natively, causing onboarding friction and duplicated documentation.

## Solution Statement
Replace all Claude/Anthropic-specific documentation and prompt templates with Copilot/VS Code equivalents. Create an adapter for Copilot CLI/Chat, migrate and update all guides, and ensure all workflows are validated and discoverable in VS Code.

## Metadata
| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | REFACTOR                                          |
| Complexity       | MEDIUM                                            |
| Systems Affected | docs, prompts, adapters, onboarding, validation   |
| Dependencies     | GitHub Copilot (latest), Copilot Chat, Copilot CLI|
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
║   │   VS Code   │ ──────► │ Claude Docs │ ──────► │ PRP Output  │            ║
║   │  User       │         │ & Prompts   │         │ (Claude)    │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: User must follow Claude-specific docs and run external CLIs      ║
║   PAIN_POINT: Onboarding friction, duplicated docs, non-native workflows      ║
║   DATA_FLOW: VS Code → Claude docs/prompts → PRP output (Claude)              ║
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
║   │   VS Code   │ ──────► │ Copilot Docs│ ──────► │ PRP Output  │            ║
║   │  User       │         │ & Prompts   │         │ (Copilot)   │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: User runs PRP flows natively in VS Code with Copilot             ║
║   VALUE_ADD: Lower onboarding friction, unified docs, native workflows        ║
║   DATA_FLOW: VS Code → Copilot docs/prompts → PRP output (Copilot)            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location              | Before                | After                 | User Impact                        |
|-----------------------|----------------------|-----------------------|------------------------------------|
| `claude_md_files/`    | Claude-only guides   | Deprecated, replaced  | Users see Copilot-native docs      |
| `copilot_md_files/`   | N/A                  | Copilot guides        | Users access new Copilot docs      |
| `.github/prompts/`    | Claude prompts       | Copilot prompts       | Prompts work with Copilot/VS Code  |
| `README.md`           | Claude references    | Copilot references    | Onboarding is Copilot-first        |

---

## Mandatory Reading
| Priority | File                                         | Lines | Why Read This                         |
|----------|----------------------------------------------|-------|---------------------------------------|
| P0       | `.claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` | all   | Migration requirements and phases      |
| P1       | `README.md`                                 | all   | Main usage and migration notice       |
| P2       | `.github/prompts/prp-implement.prompt.md`   | all   | Copilot prompt template structure     |
| P2       | `.github/prompts/prp-plan.prompt.md`        | all   | Copilot plan prompt template          |
| P2       | `.github/prompts/prp-prd.prompt.md`         | all   | Copilot PRD prompt template           |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Copilot Docs](https://docs.github.com/en/copilot) | Getting started, features, privacy | Official Copilot usage and limits |
| [Copilot Chat](https://docs.github.com/en/copilot/github-copilot-chat) | VS Code integration | Prompting and context rules |
| [Copilot CLI](https://docs.github.com/en/copilot/github-copilot-cli) | CLI usage | Adapter integration |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```markdown
// SOURCE: .claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md:1-60
- Every Claude agent guide in `claude_md_files/CLAUDE-*.md` must have a Copilot/VS Code equivalent in `copilot_md_files/`, with the similar structure and conventions, updated for Copilot workflows.
- Add a deprecation header to each legacy Claude guide, referencing the new Copilot equivalent.
- Provide a compatibility/feature-flag (e.g., `PRP_TOOL_ADAPTER=claude|copilot`) to allow incremental migration and rollback.
```

**PROMPT_TEMPLATE:**
```markdown
// SOURCE: .github/prompts/prp-implement.prompt.md:1-40
## Your Mission

Execute the plan end-to-end with rigorous self-validation. You are autonomous.

**Core Philosophy**: Validation loops catch mistakes early. Run checks after every change. Fix issues immediately. The goal is a working implementation, not just code that exists.
```

**ERROR_HANDLING:**
```markdown
// SOURCE: .github/skills/prp-core-runner/SKILL.md:27-60
- Stop execution immediately if any validation fails
- Report the specific error clearly
- Guide the user on how to resolve the issue
- Do not attempt to auto-fix complex validation failures
```

**DOC_LOCATION:**
```markdown
// SOURCE: README.md:59-60
The `.github/prompts/` directory contains the core PRP workflow commands and templates.
```

---

## Files to Change
| File                                 | Action   | Justification                                 |
|-------------------------------------- |----------|-----------------------------------------------|
| `copilot_md_files/`                  | CREATE   | New Copilot-native guides                     |
| `claude_md_files/`                   | UPDATE   | Add deprecation headers, reference new docs   |
| `.github/prompts/`                   | UPDATE   | Add Copilot-compatible prompt templates        |
| `README.md`                          | UPDATE   | Reference Copilot, migration, new docs        |
| `.vscode/extensions.json`             | CREATE   | Recommend Copilot/VS Code extensions          |
| `PRPs/scripts/invoke_copilot.py`     | UPDATE   | Adapter for Copilot CLI/Chat integration      |
| `AGENTS.md`                          | CREATE   | Copilot agent guide (from CLAUDE.md)          |
| `docs_map.json`                      | CREATE   | Legacy→Copilot doc mapping for adapter        |

---

## NOT Building (Scope Limits)
- No migration of `old-prp-commands/` (historical only)
- No full feature parity for proprietary Claude-only behaviors
- No Copilot API for direct prompt injection (not supported)

---

## Step-by-Step Tasks

### Task 1: CREATE `copilot_md_files/` and migrate three guides
- **ACTION**: Copy/convert three key guides (e.g., Python, Node, React) from `claude_md_files/` to `copilot_md_files/`, updating for Copilot workflows
- **MIRROR**: Structure and conventions from legacy guides
- **VALIDATE**: Manual review for Copilot/VS Code accuracy

### Task 2: UPDATE `claude_md_files/` with deprecation headers
- **ACTION**: Add deprecation header to each file, referencing new Copilot location
- **MIRROR**: Header pattern from migration PRD
- **VALIDATE**: Check all files reference new Copilot guide

### Task 3: UPDATE `.github/prompts/` with Copilot-compatible templates
- **ACTION**: Ensure all prompt templates are Copilot/VS Code compatible
- **MIRROR**: `.github/prompts/prp-implement.prompt.md` structure
- **VALIDATE**: Test in Copilot Chat/CLI

### Task 4: UPDATE `README.md` for Copilot-first onboarding
- **ACTION**: Reference Copilot, migration, and new docs
- **MIRROR**: Migration notice pattern from PRD
- **VALIDATE**: Manual review

### Task 5: CREATE `.vscode/extensions.json`
- **ACTION**: Recommend Copilot, Copilot Chat, GitLens, PR extensions
- **VALIDATE**: VS Code shows recommendations

### Task 6: UPDATE `PRPs/scripts/invoke_copilot.py` for Copilot CLI/Chat
- **ACTION**: Ensure adapter supports Copilot CLI/Chat, fallback to manual if unavailable
- **VALIDATE**: Run PRP flows via adapter

### Task 7: CREATE `AGENTS.md` (from CLAUDE.md)
- **ACTION**: Copy/convert agent guide, update for Copilot
- **VALIDATE**: Manual review

### Task 8: CREATE `docs_map.json`
- **ACTION**: Map legacy Claude guides to Copilot equivalents for adapter compatibility
- **VALIDATE**: Adapter resolves docs correctly

---

## Testing Strategy
| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| Manual review | All migrated docs/prompts | Accuracy, completeness |
| Adapter test | PRP flows via Copilot CLI/Chat | Integration |

### Edge Cases Checklist
- [ ] Legacy doc not found in Copilot location
- [ ] Prompt template not compatible with Copilot
- [ ] Adapter fallback not triggered if Copilot CLI unavailable
- [ ] User attempts to use deprecated Claude doc

---

## Validation Commands
### Level 1: STATIC_ANALYSIS
Manual: Review all migrated docs/prompts for Copilot/VS Code compatibility

### Level 2: UNIT_TESTS
Manual: Run PRP flows via Copilot CLI/Chat and verify output

### Level 3: FULL_SUITE
Manual: End-to-end PRP workflow in VS Code with Copilot

---

## Acceptance Criteria
- [ ] All specified functionality implemented per user story
- [ ] All validation steps pass
- [ ] All new docs/prompts are Copilot/VS Code compatible
- [ ] No regressions in PRP workflows
- [ ] UX matches "After State" diagram

---

## Completion Checklist
- [ ] All tasks completed in order
- [ ] Each task validated after completion
- [ ] All acceptance criteria met

---

## Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Copilot prompt length limits | MED | MED | Keep templates concise, prioritize context |
| No API for prompt injection | HIGH | MED | Use code comments/docstrings, not direct injection |
| Security/privacy (data sent to GitHub) | MED | HIGH | Avoid secrets in prompts/docs |
| User confusion during transition | MED | MED | Add clear deprecation headers, update onboarding |

---

## Notes
- Copilot does not support direct prompt injection; all prompt engineering must be via comments/docstrings
- Legacy Claude docs are retained with deprecation headers for a transition period
- Adapter must support fallback/manual mode if Copilot CLI/Chat is unavailable
- All new docs/prompts must be validated in Copilot/VS Code
