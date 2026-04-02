# Feature: Extract Prompt Output Templates — Phase 1: Setup

## Summary

Phase 1 establishes the target directory `.github/PRPs/templates/` and creates a README that
documents the naming convention and inventory of all 19 expected template files. The directory
already exists (empty); the only deliverable is `README.md`.

## User Story

As a framework maintainer,
I want a well-documented `.github/PRPs/templates/` directory with a naming-convention README,
So that contributors immediately understand where templates live and how to name them before Phases 2–3 add the actual files.

## Problem Statement

The `.github/PRPs/templates/` directory exists but is empty and undocumented. Without a README
that specifies the naming convention and expected inventory, contributors working on Phase 2
(extract) and Phase 3 (update prompts) will lack a shared reference, increasing the chance of
inconsistent naming or missing files.

## Solution Statement

Create `README.md` in `.github/PRPs/templates/` that documents:
- Purpose of the directory
- Naming convention (`<prompt-name>.prompt-<function>-template.md`)
- Complete inventory of all 19 expected template files with their source prompt and function label
- The reference instruction pattern prompts will use to point at template files

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | REFACTOR                                          |
| Complexity       | LOW                                               |
| Systems Affected | `.github/PRPs/templates/`                         |
| Dependencies     | None                                              |
| Estimated Tasks  | 1                                                 |

---

## UX Design

### Before State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────────────────────────┐                                        ║
║   │  .github/PRPs/templates/         │  ← empty, no documentation             ║
║   │  (directory exists, no README)   │                                        ║
║   └──────────────────────────────────┘                                        ║
║                                                                               ║
║   USER_FLOW: Contributor opens templates/ and sees an empty folder.            ║
║   PAIN_POINT: No naming convention documented; no inventory of expected files. ║
║   DATA_FLOW: N/A — directory is empty, nothing created yet.                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║   ┌──────────────────────────────────┐                                        ║
║   │  .github/PRPs/templates/         │                                        ║
║   │    README.md  ← NEW              │  ← naming convention + inventory       ║
║   └──────────────────────────────────┘                                        ║
║                            │                                                  ║
║                            ▼                                                  ║
║          ┌─────────────────────────────────────────────────────┐              ║
║          │ README documents:                                    │              ║
║          │  • Naming convention                                 │              ║
║          │  • 19 expected template files (inventory)           │              ║
║          │  • Template reference pattern for prompts           │              ║
║          └─────────────────────────────────────────────────────┘              ║
║                                                                               ║
║   USER_FLOW: Contributor reads README and knows exactly what 19 files to     ║
║              create in Phase 2 and how prompts will reference them in Phase 3.║
║   VALUE_ADD: Single source of truth for naming convention before coding starts.║
║   DATA_FLOW: README → informs Phase 2 file naming → informs Phase 3 prompt   ║
║              reference format.                                                ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location                         | Before                  | After                            | User Impact                                   |
| -------------------------------- | ----------------------- | -------------------------------- | --------------------------------------------- |
| `.github/PRPs/templates/`        | Empty folder            | Contains `README.md`             | Contributor knows naming convention instantly |
| Phase 2 implementer context      | Must infer from PRD     | Reads README for canonical names | Reduces risk of naming inconsistencies        |
| Phase 3 implementer context      | Must infer ref format   | Reads README for ref pattern     | Consistent reference instructions in prompts  |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting Task 1:**

| Priority | File                                                                     | Lines | Why Read This                                |
| -------- | ------------------------------------------------------------------------ | ----- | -------------------------------------------- |
| P0       | `.claude/PRPs/prds/extract-prompt-output-templates.prd.md`               | all   | Canonical inventory of 19 templates + naming |
| P1       | `.github/hooks/README.md`                                                | 1-20  | README style used in `.github/` subdirs      |

**External Documentation:**
None required — this is pure markdown file creation.

---

## Patterns to Mirror

**README_STYLE:**
```markdown
// SOURCE: .github/hooks/README.md:1-5
// COPY THIS PATTERN: concise heading + short purpose paragraph + structured sections
# PRP Ralph Hooks

This directory contains hooks for the PRP Ralph autonomous loop system.

## Setup
...
```

**NAMING_CONVENTION (to document in README):**
```
// SOURCE: .claude/PRPs/prds/extract-prompt-output-templates.prd.md, Decision Log
// PATTERN: <prompt-name>.prompt-<function>-template.md
// EXAMPLES:
prp-prd.prompt-prd-template.md          ← from prompt: prp-prd, phase: GENERATE
prp-prd.prompt-summary-template.md      ← from prompt: prp-prd, phase: OUTPUT
prp-commit.prompt-output-template.md    ← from prompt: prp-commit, phase: OUTPUT
```

**TEMPLATE_REFERENCE_PATTERN (to document in README — how prompts will point to files):**
```markdown
// SOURCE: .claude/PRPs/prds/extract-prompt-output-templates.prd.md, Technical Approach
// PATTERN agents use in prompt files:
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

---

## Files to Change

| File                                 | Action | Justification                                         |
| ------------------------------------ | ------ | ----------------------------------------------------- |
| `.github/PRPs/templates/README.md`   | CREATE | Documents naming convention, inventory, reference pattern |

> **Note**: `.github/PRPs/templates/` directory already exists (confirmed empty). No `mkdir` needed.

---

## NOT Building (Scope Limits)

- **Template files themselves** — those are Phase 2 (Extract)
- **Prompt file updates** — those are Phase 3 (Update)
- **Deduplication or shared template inheritance** — explicitly out of scope per PRD
- **Template rendering engine** — templates remain static markdown

---

## Step-by-Step Tasks

### Task 1: CREATE `.github/PRPs/templates/README.md`

- **ACTION**: CREATE README file documenting the templates directory
- **IMPLEMENT**: Use the exact content specified below
- **MIRROR**: `.github/hooks/README.md:1-5` — concise heading, short paragraph, structured sections
- **CONTENT**:

```markdown
# PRP Prompt Output Templates

This directory contains standalone output format templates extracted from the 13 prompt files in `.github/prompts/`.

## Purpose

Each template defines the exact output structure an agent must produce when executing a PRP prompt.
Separating templates from prompt logic lets maintainers update output formats without touching
agent instruction logic, and lets contributors find any template in under 10 seconds.

## Naming Convention

```
<prompt-name>.prompt-<function>-template.md
```

- `<prompt-name>` — matches the source `.prompt.md` file name without the extension (e.g., `prp-prd`)
- `<function>` — derived from the phase name where the template is embedded (e.g., `generate`, `output`, `report`, `design`)

## Template Reference Pattern

When a prompt references a template, it uses this instruction block:

```markdown
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

## Template Inventory

19 template files total across 13 source prompts:

| Template File | Source Prompt | Function (Phase) |
|---|---|---|
| `prp-codebase-question.prompt-research-template.md` | `prp-codebase-question.prompt.md` | DOCUMENT (Phase 5) |
| `prp-codebase-question.prompt-summary-template.md` | `prp-codebase-question.prompt.md` | OUTPUT (Phase 6) |
| `prp-commit.prompt-output-template.md` | `prp-commit.prompt.md` | OUTPUT (Phase 4) |
| `prp-debug.prompt-report-template.md` | `prp-debug.prompt.md` | REPORT (Phase 5) |
| `prp-implement.prompt-report-template.md` | `prp-implement.prompt.md` | REPORT (Phase 5) |
| `prp-issue-fix.prompt-report-template.md` | `prp-issue-fix.prompt.md` | OUTPUT |
| `prp-issue-investigate.prompt-artifact-template.md` | `prp-issue-investigate.prompt.md` | BLUEPRINT |
| `prp-plan.prompt-design-template.md` | `prp-plan.prompt.md` | DESIGN (Phase 4) |
| `prp-plan.prompt-plan-template.md` | `prp-plan.prompt.md` | GENERATE (Phase 6) |
| `prp-pr.prompt-pr-template.md` | `prp-pr.prompt.md` | GENERATE |
| `prp-pr.prompt-summary-template.md` | `prp-pr.prompt.md` | OUTPUT |
| `prp-prd.prompt-prd-template.md` | `prp-prd.prompt.md` | GENERATE (Phase 7) |
| `prp-prd.prompt-summary-template.md` | `prp-prd.prompt.md` | OUTPUT (Phase 8) |
| `prp-ralph-cancel.prompt-cancel-template.md` | `prp-ralph-cancel.prompt.md` | OUTPUT |
| `prp-ralph.prompt-setup-template.md` | `prp-ralph.prompt.md` | SETUP (Phase 2) |
| `prp-ralph.prompt-progress-template.md` | `prp-ralph.prompt.md` | PROGRESS |
| `prp-review-agents.prompt-summary-template.md` | `prp-review-agents.prompt.md` | SUMMARY |
| `prp-review.prompt-report-template.md` | `prp-review.prompt.md` | REPORT |
| `prp-review.prompt-summary-template.md` | `prp-review.prompt.md` | OUTPUT/SUMMARY |
```

- **GOTCHA**: The content contains a nested fenced code block (` ``` `) inside a markdown file that is itself in a code block in this plan. When writing the actual file, the nested triple backticks must be raw (they are safe because they're the content being written, not interpreted). Write the file directly — do not try to escape the backticks.
- **VALIDATE**: `Test-Path .github/PRPs/templates/README.md` → returns `True`

---

## Testing Strategy

### Validation: Phase 1 Complete

| Check | Command | Expected |
| ----- | ------- | -------- |
| Directory exists | `Test-Path .github/PRPs/templates` | `True` |
| README created | `Test-Path .github/PRPs/templates/README.md` | `True` |
| README has naming convention section | `Select-String "Naming Convention" .github/PRPs/templates/README.md` | Match found |
| README has inventory table | `Select-String "Template Inventory" .github/PRPs/templates/README.md` | Match found |
| README lists all 19 files | `(Select-String "template.md" .github/PRPs/templates/README.md).Count` | `>= 19` |

### Edge Cases Checklist

- [ ] README does not accidentally use Windows CRLF line endings (use LF)
- [ ] All 19 template file names in the inventory match exactly the names in the PRD deliverables list
- [ ] Nested code fences render correctly in GitHub markdown preview

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```powershell
# Confirm files exist
Test-Path .github/PRPs/templates/README.md

# Verify 19 template entries
(Select-String "template\.md" .github/PRPs/templates/README.md).Count
# EXPECT: 19 or more matches
```

### Level 2: MARKDOWN_LINT

```
# Use markdown-linter skill on the new README
```

**EXPECT**: No lint errors

### Level 3: MANUAL_VALIDATION

1. Open `.github/PRPs/templates/README.md` in VS Code
2. Verify the naming convention section is clear and matches PRD Decision Log
3. Cross-check all 19 file names in the inventory against the PRD's Phase 2 deliverables list
4. Confirm the template reference pattern matches the PRD's Technical Approach section exactly

---

## Acceptance Criteria

- [ ] `.github/PRPs/templates/README.md` created
- [ ] README contains "Naming Convention" section with `<prompt-name>.prompt-<function>-template.md` pattern
- [ ] README lists all 19 expected template files in an inventory table
- [ ] README contains the template reference pattern block (`> **Output Template**: ...`)
- [ ] All 19 file names in README match the PRD Phase 2 deliverables list exactly
- [ ] Markdown linter passes on new README

---

## Completion Checklist

- [ ] Task 1 completed: `README.md` created in `.github/PRPs/templates/`
- [ ] Level 1 validation: `Test-Path` returns `True` for directory and README
- [ ] Level 2 validation: markdown linter passes
- [ ] Level 3 validation: manual cross-check of 19 file names against PRD
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk                                          | Likelihood | Impact | Mitigation                                                            |
| --------------------------------------------- | ---------- | ------ | --------------------------------------------------------------------- |
| 19 file names in README diverge from PRD list | LOW        | MEDIUM | Cross-check line-by-line against PRD Phase 2 deliverables before save |
| Nested code fences break README render        | LOW        | LOW    | Preview in VS Code markdown renderer before marking complete          |

---

## Notes

- The `.github/PRPs/templates/` directory already exists (empty). No `mkdir` needed.
- Phase 1 success signal from PRD is "Directory exists" — this is already met. Adding the README
  is the "Could" MoSCoW requirement that makes Phase 2 and Phase 3 easier to execute without error.
- Once this plan is complete, PRD Phase 1 can be marked `complete` and Phase 2 planning can begin.
- Phase 2 and Phase 3 are sequential and each warrants its own plan file.
