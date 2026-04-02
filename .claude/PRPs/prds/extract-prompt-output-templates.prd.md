# Extract Prompt Output Templates

## Problem Statement

The 13 prompt files in `.github/prompts/` each embed their output format templates inline, making
the prompts long, hard to navigate, and templates impossible to reuse. Maintainers must edit two
concerns in one file — agent instruction logic and output format — which increases the risk of
unintended changes and makes it hard to audit or update templates independently.

## Evidence

- Every prompt file in `.github/prompts/` (13/13) contains at least one embedded output template
- Six prompts (`prp-codebase-question`, `prp-plan`, `prp-pr`, `prp-prd`, `prp-ralph`, `prp-review`) contain two distinct templates each, yielding 19 template files total from 13 prompts
- Templates range from compact 8-line snippets to 130-line structured documents with YAML frontmatter, tables, and code blocks
- No shared reference mechanism exists: similar patterns (validation status tables, tasks-completed tables) are duplicated across `prp-implement` and `prp-issue-fix` without a common source

## Proposed Solution

Extract all embedded output format templates verbatim (preserving all examples, placeholder syntax,
and structural extras) into standalone template files under `.github/PRPs/templates/`. Each file
is named `<prompt-name>-<function>-template.md`, where `<function>` is derived from the phase name
where the template is embedded (e.g., `prp-prd.prompt-prd-template.md`,
`prp-prd.prompt-summary-template.md`). Prompts with two embedded templates get two separate files.
Update each source prompt to replace the inline template block with a reference to its template
file(s), so agents know where to find the output format.

## Key Hypothesis

We believe separating output templates from prompt logic will make prompts easier to read and
templates easier to maintain. We'll know we're right when a contributor can find any output
template in under 10 seconds and update it without touching agent instruction logic.

## What We're NOT Building

- **Template rendering engine** — templates remain static markdown files, not code
- **Shared/reusable template inheritance** — each prompt gets its own template file even if patterns overlap; deduplication is a separate concern
- **New template format** — templates are extracted "as-is", no reformatting or normalization

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Templates extracted | 19 template files created | File count in `.github/PRPs/templates/` |
| Prompts updated | 13 prompts reference their template | Grep for template reference in each prompt |
| Zero content lost | Template files match original embedded content | Diff between original and extracted |

---

## Users & Context

**Primary User**
- **Who**: Framework maintainer or developer creating/debugging a PRP prompt
- **Current behavior**: Scrolls through 300–600 line prompt files to find the output template section
- **Trigger**: Needs to update an output format, audit what a prompt produces, or reuse a pattern
- **Success state**: Opens `.github/PRPs/templates/<name>.prompt-<function>-template.md`, edits only the template

**Job to Be Done**
When maintaining a PRP prompt, I want to find and edit the output format template independently of
the agent instructions, so I can update one concern without risking changes to the other.

**Non-Users**
End users of the PRP framework who just run prompts — they are unaffected by this change.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Create `.github/PRPs/templates/` directory | Target location for all template files |
| Must | Extract templates from all 13 prompt files verbatim | Preserves all examples, placeholders, extras |
| Must | Update each prompt to reference its template file | Agents must know where to find output format |
| Must | Separate file per template for multi-template prompts | Function label in filename derived from phase name; unique name per template |
| Could | Add a README to the templates directory | Explains naming convention and purpose |
| Won't | Normalize or deduplicate similar templates | Out of scope; separate concern |

### MVP Scope

All 19 template files created, all 13 prompts updated with a template reference. No content lost or altered.

### User Flow

1. Maintainer receives request to update PR body format
2. Opens `.github/PRPs/templates/prp-pr.prompt-create-template.md`
3. Edits template structure
4. Prompt file `prp-pr.prompt.md` is untouched — its instruction logic unchanged

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**
- Template files are pure markdown — no parsing, no tooling required
- Reference instruction in prompts should be clear enough that AI agents reading the prompt will load the template file before generating output
- Prompts with multiple templates get one file per template; the `<function>` in the filename is derived from the phase name (e.g., GENERATE → `generate`, REPORT → `report`, DESIGN → `design`) where the template is embedded

**Template Reference Pattern in Prompts**

Replace embedded template blocks with:
```
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

**Prompts with Multiple Templates**

| Prompt | Templates | Template Files |
|--------|-----------|----------------|
| `prp-codebase-question.prompt.md` | Research document + Output summary | `prp-codebase-question.prompt-research-template.md`, `prp-codebase-question.prompt-summary-template.md` |
| `prp-plan.prompt.md` | UX Design (ASCII diagrams + interaction table) + Full `.plan.md` file | `prp-plan.prompt-design-template.md`, `prp-plan.prompt-plan-template.md` |
| `prp-prd.prompt.md` | Full `.prd.md` file + Output summary (`## PRD Created`) | `prp-prd.prompt-prd-template.md`, `prp-prd.prompt-summary-template.md` |
| `prp-pr.prompt.md` | PR body markdown + Output summary (`## Pull Request Created`) | `prp-pr.prompt-pr-template.md`, `prp-pr.prompt-summary-template.md` |
| `prp-ralph.prompt.md` | Startup message + Iteration progress log | `prp-ralph.prompt-setup-template.md`, `prp-ralph.prompt-progress-template.md` |
| `prp-review.prompt.md` | Full review report (YAML frontmatter + tables) + Output summary | `prp-review.prompt-report-template.md`, `prp-review.prompt-summary-template.md` |

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| AI agent ignores template file reference | L | Phrase reference as explicit instruction, not a comment |
| Template extracted with missing context | L | Verify each extract includes all examples and extras |
| Prompt logic accidentally removed during edit | L | Make targeted replacements; do not rewrite surrounding context |

---

## Implementation Phases

<!--
  STATUS: pending | in-progress | complete
  PARALLEL: phases that can run concurrently (e.g., "with 3" or "-")
  DEPENDS: phases that must complete first (e.g., "1, 2" or "-")
  PRP: link to generated plan file once created
-->

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Setup | Create `.github/PRPs/templates/` directory | complete | - | - | `.claude/PRPs/plans/completed/extract-prompt-output-templates-phase-1-setup.plan.md` |
| 2 | Extract | Extract 19 templates from all 13 prompt files into separate template files | in-progress | - | 1 | `.claude/PRPs/plans/extract-prompt-output-templates-phase-2-extract.plan.md` |
| 3 | Update | Update all 13 prompt files to reference their template files | pending | - | 2 | - |

### Phase Details

**Phase 1: Setup**
- **Goal**: Establish the target directory
- **Scope**: Create `.github/PRPs/templates/` directory
- **Success signal**: Directory exists

**Phase 2: Extract**
- **Goal**: Each prompt's embedded output template(s) live as a standalone file
- **Scope**: Create one `<name>.prompt-<function>-template.md` per embedded template; function is derived from the phase name where the template is embedded; extract verbatim — no reformatting
- **Deliverables**: 19 files
  - `prp-codebase-question.prompt-research-template.md`
  - `prp-codebase-question.prompt-summary-template.md`
  - `prp-commit.prompt-output-template.md`
  - `prp-debug.prompt-report-template.md`
  - `prp-implement.prompt-report-template.md`
  - `prp-issue-fix.prompt-report-template.md`
  - `prp-issue-investigate.prompt-artifact-template.md`
  - `prp-plan.prompt-design-template.md`
  - `prp-plan.prompt-plan-template.md`
  - `prp-pr.prompt-pr-template.md`
  - `prp-pr.prompt-summary-template.md`
  - `prp-prd.prompt-prd-template.md`
  - `prp-prd.prompt-summary-template.md`
  - `prp-ralph-cancel.prompt-cancel-template.md`
  - `prp-ralph.prompt-setup-template.md`
  - `prp-ralph.prompt-progress-template.md`
  - `prp-review-agents.prompt-summary-template.md`
  - `prp-review.prompt-report-template.md`
  - `prp-review.prompt-summary-template.md`
- **Success signal**: 19 template files exist; content matches what was embedded in source prompts

**Phase 3: Update**
- **Goal**: Each prompt references its template file rather than embedding the template inline
- **Scope**: For each prompt, replace each embedded template block with a reference instruction pointing to the corresponding `.github/PRPs/templates/<name>.prompt-<function>-template.md`; preserve all surrounding instruction text
- **Success signal**: No large markdown template blocks remain in prompt files; each prompt contains a reference to its template file

### Parallelism Notes

Phase 2 file extractions are independent per prompt and could be parallelized across prompts.
Phase 3 prompt updates are independent per prompt and could be parallelized across prompts.
Phases 2 and 3 are sequential: templates must exist before prompts reference them.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Multi-template file structure | One file per template function (19 files total) | One combined file per prompt with section headers | Unique filenames enable direct navigation; function label makes template purpose explicit |
| Template reference format | Instruction block with file path | YAML frontmatter include / symlink | Markdown-native; works for AI agents reading the file |
| Naming convention | `<prompt-name>-<function>-template.md` | `prompt-<name>-output.md` / `output-<name>.md` | Function label derived from phase name; groups files by source prompt; makes template purpose explicit |
| Content fidelity | Extract verbatim | Normalize/clean up | Avoids unintended behavior changes; respects "as-is" requirement |

---

## Research Summary

**Market Context**
Standard practice in documentation-as-code frameworks (e.g., Docusaurus, Backstage) is to separate
template definitions from template-invoking logic. The DRY principle applied to agent prompts
suggests output format templates are data, not logic.

**Technical Context**
All 13 prompt files in `.github/prompts/` (100%) contain embedded output templates. 6 prompts
contain 2 templates each, yielding 19 template files total. Templates range from 8 lines (prp-commit) to ~130 lines (prp-plan).
The `.github/PRPs/templates/` directory does not yet exist. No tooling changes required — pure
file creation and text replacement in existing prompts.

---

*Generated: 2026-04-02*
*Status: DRAFT - needs validation*
