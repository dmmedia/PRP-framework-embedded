# Feature: VS Code Integration for Copilot-Based PRP Workflow (Phase 4)

## Summary

This plan implements the VS Code integration phase of the PRP Copilot migration. It adds workspace configs, recommended extensions, and command-palette wiring for the three core PRP flows (`prp-prd`, `prp-plan`, `prp-implement`) using Copilot Chat/CLI as the adapter backend. It also defines verification steps to ensure flows work in VS Code and that the project can fall back to manual commands when entitlements are unavailable.

## User Story

As a VS Code-based developer
I want to run PRP workflows from VS Code with Copilot
So that I can stay in context and ship PRP tasks with fewer context switches

## Problem Statement

Phase 4 in the migration is currently missing direct VS Code integration. Without command-palette and workspace recommendations, developers must still run shell scripts manually and depend on external terminals.

## Solution Statement

Add `.vscode/extensions.json` and `.vscode/settings.json` that recommend Copilot and Copilot Chat. Create instructions for command-palette commands in `README.md` and implement a minimal VS Code tasks/command definitions using the existing `invoke_copilot.py` adapter.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | MEDIUM                                            |
| Systems Affected | .vscode, README.md, plugins/prp-core, PRP scripts |
| Dependencies     | GitHub Copilot extension, GitHub Copilot Chat extension |
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
║   │   VS Code   │ ──────► │  Terminal   │ ──────► │ Claude CLI  │            ║
║   │  Editor     │         │ (uv run)    │         │ /copilot    │            ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                                                               ║
║   USER_FLOW: Manual terminal commands and non-idiomatic VS Code workflow      ║
║   PAIN_POINT: Adds friction, users cannot discover commands in palette        ║
║   DATA_FLOW: VS Code -> terminal -> invoke_command.py -> claude/copilot      ║
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
║   │   VS Code   │ ──────► │ Copilot     │ ──────► │ PRP Artifacts│           ║
║   │  Editor     │         │ Command Pal  │         │ (.claude/.github)|         ║
║   └─────────────┘         └─────────────┘         └─────────────┘            ║
║                                   │                                           ║
║                                   ▼                                           ║
║                          ┌─────────────┐                                      ║
║                          │ .vscode settings│                                      ║
║                          └─────────────┘                                      ║
║                                                                               ║
║   USER_FLOW: VS Code command palette and tasks run PRP flows with Copilot    ║
║   VALUE_ADD: Reduced context switching, discoverability, productivity         ║
║   DATA_FLOW: VS Code -> command-palette/tasks -> adapter -> Copilot CLI/Chat  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `.vscode/extensions.json` | None or stale | Copilot + GitLens recommendations | Onboarding improved
| `.vscode/settings.json` | None or manual | Copilot/Chat settings + per-workspace defaults | Easy config
| `README.md` | CLI instructions | VS Code command palette usage | user can follow one-click flows
| `plugins/prp-core` | environmental paths | adapter flag-based integration | more resilient to migration

---

## Mandatory Reading

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | .github/PRPs/scripts/invoke_command.py | 1-180 | Core adapter path resolution and existing webhook logic |
| P1 | .github/PRPs/scripts/prp_workflow.py | 1-230 | Entry point for chained PRP operations |
| P2 | .vscode/extensions.json | all | extension recommendations pattern |
| P3 | .vscode/settings.json | all | workspace settings pattern |
| P4 | README.md | relevant section | update to Copilot flow instructions |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [VS Code Tasks](https://code.visualstudio.com/docs/editor/tasks#_custom-tasks) | Task definitions | create PRP task entries |
| [Copilot in VS Code](https://docs.github.com/en/copilot/getting-started-with-github-copilot) | Installation | ensure user has extension |
| [Copilot Chat](https://docs.github.com/en/copilot/copilot-chat) | Quickstart | recommended command palette usage |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```json
// SOURCE: .vscode/extensions.json:1-10
"recommendations": [
  "GitHub.copilot",
  "GitHub.copilot-chat",
  "eamodio.gitlens",
  "GitHub.vscode-pull-request-github"
]
```

**ERROR_HANDLING:**
```python
# SOURCE: .github/PRPs/scripts/invoke_command.py:70-92
if not COPILOT_CLI:
    print("[WARN] Copilot CLI not found. Falling back to manual mode.")
    return manual_fallback(args)
```

**LOGGING_PATTERN:**
```python
# SOURCE: .github/PRPs/scripts/prp_workflow.py:40-54
print(f"→ Running: {command_name} {arguments}", file=sys.stderr)
```

**SERVICE_PATTERN:**
```python
# SOURCE: .github/PRPs/scripts/invoke_command.py:1-150
# service wrapper for applying templates and calling the proper command
```

**TEST_STRUCTURE:**
```markdown
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-2-v-2.plan.md
// use explicit tasks + validation steps for each action
```

---

## Files to Change

| File | Action | Justification |
| --- | --- | --- |
| `.vscode/extensions.json` | UPDATE | ensure Copilot & Copilot Chat are recommended in workspace |
| `.github/PRPs/scripts/invoke_command.py` | UPDATE | add `PRP_TOOL_ADAPTER` logic for Copilot vs Claude fallback |
| `.github/PRPs/scripts/prp_workflow.py` | UPDATE | ensure commands reference adapter and support `--adapter` option |
| `README.md` | UPDATE | add section "VS Code Copilot PRP workflow" |
| `CLAUDE.md` | UPDATE | add deprecation notice and new AGENTS.md link |
| `plugins/prp-core/hooks/*` | UPDATE | support adapter env var and path mapping |
| `.claude/PRPs/commands/...` | REVIEW | ensure prompt templates support Copilot CLI output format |

---

## NOT Building (Scope Limits)

- Rewriting the entire codebase to remove all Claude references in one commit (out of scope for this phase)
- Building a full VS Code extension from scratch (phase 4 includes a minimal shortcut/task layer only)

---

## Step-by-Step Tasks

### Task 1: Update `.vscode/extensions.json`
- **ACTION**: Ensure the file includes `GitHub.copilot`, `GitHub.copilot-chat`, `eamodio.gitlens`, `GitHub.vscode-pull-request-github`, and `ms-python.python`.
- **VALIDATE**: `code --list-extensions` (if installed) and `cat .vscode/extensions.json`.

### Task 2: Add VS Code command palette tasks
- **ACTION**: Add `.vscode/tasks.json` with tasks:
  - `PRP: Create PRD` → `uv run .github/PRPs/scripts/prp_workflow.py --skip-create ...` (or direct `prp-prd` command)
  - `PRP: Plan` → `uv run .github/PRPs/scripts/prp_workflow.py --skip-create ...`
  - `PRP: Implement` → `uv run .github/PRPs/scripts/prp_workflow.py --skip-create ...`
- **VALIDATE**: `code --list-tasks` in workspace; run each task.

### Task 3: Update `README.md` (VS Code section)
- **ACTION**: Add a new section: "VS Code + Copilot PRP Workflow" with steps and task command names.
- **VALIDATE**: `grep -n "VS Code Copilot" README.md`.

### Task 4: Update `CLAUDE.md` with deprecation header
- **ACTION**: Add beginning note:
  "DEPRECATED: use AGENTS.md (Copilot + VS Code)."
- **VALIDATE**: `grep -n "DEPRECATED" CLAUDE.md`.

### Task 5: Update adapter logic in `.github/PRPs/scripts/invoke_command.py`
- **ACTION**: Add `PRP_TOOL_ADAPTER` environment variable and fallback path. Method:
  - `adapter = os.getenv('PRP_TOOL_ADAPTER', 'claude')`
  - if `copilot`: call `copilot` CLI with compatible args; else `claude`.
- **VALIDATE**: `python -m py_compile .github/PRPs/scripts/invoke_command.py`, run `uv run .github/PRPs/scripts/invoke_command.py prp-core-create "Add test" --output-format text` with adapter set.

### Task 6: Update `plugins/prp-core/hooks` and workflow entrypoints
- **ACTION**: Add adapter env var support in scripts that invoke `invoke_command.py` or run `claude` directly.
- **VALIDATE**: `grep` for `claude` references and update; all references present.

### Task 7: Update `README.md` instructions in top-level for Copilot workflow
- **ACTION**: Replace all remaining `claude` workflow snippets with Copilot usage, while preserving fallback.
- **VALIDATE**: Manual check and run local command sequences.

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| `.github/PRPs/scripts/test_invoke_command.py` | Copilot fallback, Claude fallback, command path resolution | Adapter behavior |

### Edge Cases Checklist
- [ ] `copilot` CLI not available
- [ ] `claude` binary not available
- [ ] `PRP_TOOL_ADAPTER` invalid value
- [ ] VS Code command palette tasks not found
- [ ] Legacy `claude` docs still shown; requires deprecation wing

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
python -m py_compile .github/PRPs/scripts/invoke_command.py .github/PRPs/scripts/prp_workflow.py
``` 

### Level 2: UNIT_TESTS
```bash
# (if tests exist)
python -m pytest .github/PRPs/scripts/test_invoke_command.py
``` 

### Level 3: FULL_SUITE
```bash
uv run .github/PRPs/scripts/prp_workflow.py "Run PRP flow test" --no-commit --no-pr
``` 

### Level 4: MANUAL_VALIDATION
- [ ] Open VS Code, run `Tasks: Run Task`, execute each PRP task.
- [ ] Verify `prp-prd`, `prp-plan`, and `prp-implement` are available in command palette (via `.vscode/tasks.json` or extension).
- [ ] Verify old `claude` path warnings are displayed as optional fallback.

---

## Acceptance Criteria
- [ ] All changes implemented as tasks above
- [ ] VS Code tasks run successfully in the workspace
- [ ] README/CLAUDE docs updated with Copilot guidance
- [ ] adapter supports `PRP_TOOL_ADAPTER=copilot` and fallback to `claude`

---

## Completion Checklist
- [ ] Task 1: VS Code extensions updated
- [ ] Task 2: Command palette tasks created
- [ ] Task 3: README updated
- [ ] Task 4: CLAUDE deprecation header added
- [ ] Task 5: Adapter env var logic updated
- [ ] Task 6: Hooks updated
- [ ] Task 7: Instruction flow updated

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Missing Copilot entitlement | HIGH | HIGH | document fallback to manual mode, ensure Claude path is available | 
| Command palette tasks not discoverable | MEDIUM | MEDIUM | provide explicit docs and script to generate tasks | 
| False sense of completion if tasks not run | MEDIUM | MEDIUM | add automated smoke test in CI for VS Code tasks | 

---

## Notes

- This plan specifically targets Phase 4 of migration (VS Code integration) and assumes Phase 1-3 are completed as per existing PRD state.
- Phase 5 (hooks and plugins) is scheduled as parallel work to Phase 4.
- The plan uses contextual mapping from existing file `.github/PRPs/scripts/invoke_command.py` to avoid duplicate logic.
