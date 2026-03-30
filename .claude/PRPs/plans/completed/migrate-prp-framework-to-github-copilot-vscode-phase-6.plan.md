# Feature: Migrate PRP framework to GitHub Copilot + VS Code (Phase 6)

## Summary

Finish migration of agent documentation assets and transition guides from Claude-specific files to Copilot + VS Code files, while adding permanent project landing page and deprecation safety net. This plan is built from Phase 6 scope in `.claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` and mirrors existing Phase 3/5 patterns.

## User Story

As a VS Code developer
I want legacy Claude agent docs migrated to Copilot/VS Code guides with backward-compatible deprecation links
So that I can use the PRP workflow with Copilot consistently and trust docs are up to date.

## Problem Statement

The project still retains Claude-specific agent guide artifacts and the migration is incomplete; this blocks full adoption of Copilot/VS Code workflows and causes doc confusion for new users.

## Solution Statement

Copy and adapt all remaining `claude_md_files/*.md` entries to `copilot_md_files/*.md`, create root `AGENTS.md`, and add standard deprecation headers in legacy files. Update `README.md`, `CLAUDE.md` reference points, and optionally implement a lookup script (`docs_map.json`).

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | ENHANCEMENT                                       |
| Complexity       | MEDIUM                                            |
| Systems Affected | docs, CLI adapter, command mapping, onboarding    |
| Dependencies     | None (docs/content)                               |
| Estimated Tasks  | 10                                                |

---

## UX Design

### Before State
```
- User opens docs and finds `claude_md_files/` in README and root docs.
- Some command docs refer to Claude commands only.
- No `AGENTS.md`; Copilot-wired path is partial.
```

### After State
```
- All `claude_md_files/` have Copilot equivalents in `copilot_md_files/`.
- `CLAUDE.md` and root README refer to `AGENTS.md` and new Copilot guides.
- `AGENTS.md` provides top-level Copilot + VS Code agent workflow.
- Legacy files retain deprecation header linking new docs.
```

### Interaction Changes
| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `README.md` | Points to Claude documents | Points to AGENTS.md + copilot_md_files | Clear Copilot path for new users |
| `CLAUDE.md` | Primary agent guide | Deprecated note + link to AGENTS.md | Reduces confusion |
| `claude_md_files/*.md` | Active docs | Deprecation header + pointer to new guide | Safe transition |
| `copilot_md_files/*.md` | Existing migrated subset | Full coverage + consistent template | Complete Copilot docs |

---

## Mandatory Reading

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` | Implementation Phases | Source phase requirements |
| P0 | `.claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md` | Docs & prompts migration scheme | pattern to mirror |
| P1 | `claude_md_files/CLAUDE-*.md` | all | legacy source text |
| P1 | `copilot_md_files/COPILOT-*.md` | all | existing converted pattern |
| P1 | `README.md` | top | update linking behavior |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| [Copilot Chat agent mode](https://docs.github.com/en/copilot/how-tos/chat-with-copilot/chat-in-ide#agent-mode) | Agent command usage | Correct command palette integration |
| [Copilot CLI](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli) | CLI invocation | adapter mapping |
| [VS Code command API](https://code.visualstudio.com/api/references/commands) | `executeCommand` | extension integration |
| [Copilot policies](https://docs.github.com/en/copilot/managing-github-copilot-in-your-organization/managing-policies-and-features-for-copilot-in-your-organization) | policy gating | entitlement checks |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md:134-141
// COPY THIS PATTERN:
- File naming: `COPILOT-*.md` to match existing `CLAUDE-*.md`.
- top-level section: "## Overview", "## Quickstart", "## Commands".
```

**ERROR_HANDLING:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-5.plan.md:25-40
// COPY THIS PATTERN:
- Document entitlement failures as explicit steps.
- Provide fallback: "if not available, run using local draft workflow".
```

**LOGGING_PATTERN:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-5.plan.md:57
// COPY THIS PATTERN:
- Document implementation changes as bullet entries with `- ` & sub-bullets.
```

**REPOSITORY_PATTERN:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md:154-162
// COPY THIS PATTERN:
- Use transitional mapping file (e.g., docs_map.json) and explicit fallback.
```

**SERVICE_PATTERN:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md:165
// COPY THIS PATTERN:
- create root `AGENTS.md` with architecture and workflows.
```

**TEST_STRUCTURE:**
```md
// SOURCE: .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md:80-90
// COPY THIS PATTERN:
- Unit tests for docs mapping: ensure all legacy names map to new names.
- Integration test for `prp_workflow.py --help` and doc path selection.
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `copilot_md_files/COPILOT-*.md` | UPDATE/CREATE | Full guide coverage for replacement docs |
| `AGENTS.md` | CREATE | New root agent migration guide for Copilot |
| `CLAUDE.md` | UPDATE | Mark as deprecated and link `AGENTS.md` |
| `claude_md_files/CLAUDE-*.md` | UPDATE | Add deprecation header and upward link |
| `README.md` | UPDATE | pointer updates to new docs and migration note |
| `docs_map.json` | CREATE | optional lookup helper for adapters |
| `.github/prompts/*.prompt.md` | UPDATE | ensure prompts reference Copilot docs (if used) |

---

## NOT Building (Scope Limits)

- full semantics migration of old CLI command names beyond docs (out-of-scope for Phase 6) 
- runtime code path conversion for `old-prp-commands/` (kept historically) 

---

## Step-by-Step Tasks

### Task 1: Audit remaining `claude_md_files/`

- ACTION: List `claude_md_files/*.md` that have no matching `copilot_md_files/*.md`.
- IMPLEMENT: `ls claude_md_files | sed ...` or script.
- VALIDATE: `python - <<'PY' ...` or manual check with `ls` and diff.

### Task 2: Convert one-to-one docs

- ACTION: For each file in `claude_md_files/*.md` create `copilot_md_files/COPILOT-*.md` (same content, adapt naming and instructions to Copilot/VS Code).
- MIRROR: existing converted examples (e.g., `COPILOT-PYTHON-BASIC.md`).
- VALIDATE: `grep -q "COPILOT" copilot_md_files/COPILOT-*.md` and manual spot check.

### Task 3: Add `AGENTS.md`

- ACTION: Convert and merge `CLAUDE.md` patterns into an agent-specific Copilot guide.
- IMPLEMENT: top section, command references, migration path, examples.
- VALIDATE: `grep -q "Copilot" AGENTS.md` and link checks e.g., `python -c 'import pathlib; path=pathlib.Path("AGENTS.md"); assert "CLAUDE" not in path.read_text().splitlines()[0]'`.

### Task 4: Add legacy deprecation header in `claude_md_files/*.md`

- ACTION: Insert standard header at top of every remaining legacy doc.
- IMPLEMENT: `<!-- DEPRECATED -->` and `see copilot_md_files/...`.
- VALIDATE: `grep -R "DEPRECATED" claude_md_files/*.md`.

### Task 5: Update `README.md` and `CLAUDE.md`

- ACTION: Ensure migration section points to `AGENTS.md` and `copilot_md_files/`.
- IMPLEMENT: top-level doc path updates in repo README.
- VALIDATE: `grep -E "AGENTS.md|copilot_md_files" README.md CLAUDE.md` returns non-empty.

### Task 6: Create optional mapping helper `docs_map.json`

- ACTION: Build one-to-one mapping from old to new names, used by scripts.
- IMPLEMENT: JSON dictionary.
- VALIDATE: `python -c 'import json; j=json.load(open("docs_map.json")); assert "CLAUDE-PYTHON-BASIC" in j'`.

### Task 7: Add tests for mapping

- ACTION: Add tests under `.claude/PRPs/tests/` or appropriate tests folder, e.g., `tests/test_doc_mapping.py`.
- IMPLEMENT: assert all legacy keys map and all `copilot_md_files` exist.
- VALIDATE: run test runner e.g., `uv run pytest tests/` or `npm test` as applicable.

### Task 8: Finish Phase 6 status in PRD and report

- ACTION: set Phase 6 status to `complete`, add plan path in PRD.
- IMPLEMENT: update markdown, add link to `phase-6` report path.
- VALIDATE: PRD table now has `complete` for Phase 6.

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
| ---------- | ---------- | --------- |
| `tests/test_doc_mapping.py` | all legacy->new keys exist + no missing files | mapping correctness |
| `tests/test_docs_links.py` | README/CLAUDE/AGENTS links exist | doc pointers |
| `tests/test_deprecation_headers.py` | legacy docs have header and pointer | transition behavior |

### Edge Cases Checklist

- [x] Legacy doc has missing Copilot equivalent  
- [x] Copilot doc target missing for legacy alias  
- [x] README still references old path  
- [x] `AGENTS.md` is missing  
- [x] docs_map.json mismatch

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
uv run lint && uv run type-check
```

### Level 2: UNIT_TESTS
```bash
uv run pytest tests/test_doc_mapping.py tests/test_docs_links.py tests/test_deprecation_headers.py
```

### Level 3: FULL_SUITE
```bash
uv run pytest && uv run build
```

### Level 4: DATABASE_VALIDATION
- not applicable (docs-only)

### Level 5: BROWSER_VALIDATION
- not applicable (docs-only)

### Level 6: MANUAL_VALIDATION
1. Open VS Code, use command palette to verify `PRP: Plan` and `PRP: Implement` docs in `AGENTS.md`.
2. Confirm `copilot_md_files/COPILOT-*.md` exists and the grammar is consistent.

---

## Acceptance Criteria

- [x] All phase-6 tasks completed in `.claude/PRPs/prds/...` and plan file.
- [x] `/copilot_md_files` has one-to-one coverage for `claude_md_files` (or migration backlog enumerated).
- [x] `AGENTS.md` created and linked from `README.md` and `CLAUDE.md`.
- [x] `CLAUDE.md` and `claude_md_files/*.md` include deprecation header.
- [x] `docs_map.json` exists and is tested.
- [x] tests pass with uv pytest and full suite.
- [x] PRD Phase 6 status is in-progress for this plan generation.
- [x] final PRD status should be `complete` after work.

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Incomplete one-to-one migration | MEDIUM | MEDIUM | Script-assisted coverage check, manual spot-check, and test assertion on file sets.
| Stale references in README/CLAUDE | MEDIUM | LOW | `grep` checks + pre-commit link validation script.
| Copilot policy mismatch in orgs | HIGH | MEDIUM | Add preflight docs with URL and entitlement checklist.

---

## Notes

- This plan intentionally focuses on docs artifacts; runtime integration (phase 2-5) already already implemented.
- Keep `old-prp-commands/` untouched as historical scope.
- After phase complete, set PRD phase 6 status to `complete` and optionally archive `claude_md_files` or keep as reference.
