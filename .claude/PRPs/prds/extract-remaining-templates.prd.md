# Extract Remaining Output Templates from Prompts and Agents

## Problem Statement

The first template extraction (`extract-prompt-output-templates.prd.md`) left 6 output templates
inline in prompt files and entirely skipped the 10 agent files in `.github/agents/`, which each
embed their output format templates inline. Maintainers who want to update an output format still
must scroll through 200–400 line agent files and 6 partially-updated prompt files to find the
template, increasing the risk of accidental instruction changes during template edits.

## Evidence

- 5 of 13 prompt files (`prp-implement`, `prp-issue-fix`, `prp-issue-investigate`, `prp-plan`,
  `prp-ralph`) still contain at least one inline output template — confirmed by reading each file
- All 10 agent files in `.github/agents/` embed their `## Output Format` template inline — no
  agent has ever been updated to use a reference
- 3 agents (`pr-test-analyzer`, `silent-failure-hunter`, `type-design-analyzer`) contain two
  distinct templates each (main report + alternate/no-issues variant)
- `codebase-explorer.md` has a standalone exploration output template not yet extracted
- README.md TODO section lists all 18 extraction items explicitly

## Proposed Solution

Extract all remaining embedded output format templates verbatim into standalone template files under
`.github/PRPs/templates/`. For prompt files, follow the existing convention
(`<name>.prompt-<function>-template.md`). For agent files, introduce a parallel convention
(`<name>.agent-<function>-template.md`). Update each source file to replace the inline block with
a two-line reference instruction pointing to the template file.

Use the `text-file-content-extractor-replacer` skill for all extraction and replacement operations.
Do not use `markdown-linter` to validate templates.

Bash heredoc templates (sections 7.2 and 8.2 in `prp-issue-fix`, phase 6 in
`prp-issue-investigate`) are extracted as markdown content and the source bash command is updated
from a heredoc to `"$(cat .github/PRPs/templates/<template-file>.md)"`.

## Key Hypothesis

We believe separating the remaining output templates from their source files will complete the
maintainability improvement started in the first extraction. We'll know we're right when every
agent and every prompt in `.github/` can have its output format updated without touching any
instruction logic.

## What We're NOT Building

- **New template format or rendering** — templates remain static markdown files
- **Shared/reusable templates** — no deduplication across agents or prompts; each gets its own
  file even if patterns overlap
- **Normalization** — content is extracted verbatim; no reformatting or cleanup
- **Validation via markdown-linter** — explicitly out of scope per requirements

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Template files created | 18 new files in `.github/PRPs/templates/` | File count |
| Prompt files updated | 5 prompts reference their new template(s) | Grep for reference pattern |
| Agent files updated | 10 agents reference their template(s) | Grep for reference pattern |
| Zero content lost | Template files match original embedded content | Diff before/after |

---

## Users & Context

**Primary User**
- **Who**: Framework maintainer editing an output format or auditing what a prompt/agent produces
- **Current behavior**: Scrolls through 200–400 line agent files looking for the Output Format
  section; edits template inline alongside instruction logic
- **Trigger**: Needs to update an output structure, add a field, or audit a template
- **Success state**: Opens `.github/PRPs/templates/<name>.agent-report-template.md`, edits only
  the template, source agent file is untouched

**Job to Be Done**
When maintaining a PRP agent or prompt, I want to find and edit the output format template
independently of the agent instructions, so I can update one concern without risking changes to
the other.

**Non-Users**
End users of the PRP framework who just run prompts or agents — they are unaffected by this change.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Extract 6 remaining prompt templates to `.github/PRPs/templates/` | Completes first extraction |
| Must | Extract 12 agent templates (10 agents) to `.github/PRPs/templates/` | First-time agent extraction |
| Must | Update 5 prompt source files to reference their template(s) | Removes inline blocks |
| Must | Update 10 agent source files to reference their template(s) | Removes inline blocks |
| Must | Use `text-file-content-extractor-replacer` skill for all operations | Per requirements |
| Won't | Normalize or deduplicate similar templates | Separate concern |
| Won't | Validate templates with `markdown-linter` | Explicitly excluded |

### MVP Scope

All 18 template files created, all 15 source files updated with references. No content lost.

### Template Inventory

#### Prompt Templates (6 new files)

| Template File | Source File | Section | Content Description |
|---------------|-------------|---------|---------------------|
| `prp-implement.prompt-summary-template.md` | `prp-implement.prompt.md` | Phase 6 OUTPUT | `## Implementation Complete` markdown block shown to user after implementation |
| `prp-issue-fix.prompt-pr-template.md` | `prp-issue-fix.prompt.md` | Phase 7.2 | PR body markdown inside `gh pr create` heredoc |
| `prp-issue-fix.prompt-review-template.md` | `prp-issue-fix.prompt.md` | Phase 8.2 | Review comment markdown inside `gh pr comment` heredoc |
| `prp-issue-investigate.prompt-comment-template.md` | `prp-issue-investigate.prompt.md` | Phase 6 POST | GitHub issue comment markdown inside `gh issue comment` heredoc |
| `prp-plan.prompt-summary-template.md` | `prp-plan.prompt.md` | Phase 6 REPORT_TO_USER | `## Plan Created` markdown block shown to user after plan creation |
| `prp-ralph.prompt-report-template.md` | `prp-ralph.prompt.md` | Section 4.2 item 1 | `# Implementation Report` file content block |

#### Agent Templates (12 new files)

| Template File | Source File | Template Type |
|---------------|-------------|---------------|
| `code-reviewer.agent-report-template.md` | `code-reviewer.md` | Main code review report (with issues) |
| `code-simplifier.agent-report-template.md` | `code-simplifier.md` | Code simplification report |
| `codebase-analyst.agent-report-template.md` | `codebase-analyst.md` | Codebase analysis report |
| `codebase-explorer.agent-report-template.md` | `codebase-explorer.md` | Exploration report (README lists this under `codebase-analyst.md` — typo) |
| `comment-analyzer.agent-report-template.md` | `comment-analyzer.md` | Comment analysis report |
| `gpui-researcher.agent-report-template.md` | `gpui-researcher.md` | GPUI research report (includes Validation Failed variant) |
| `pr-test-analyzer.agent-report-template.md` | `pr-test-analyzer.md` | PR test analysis report (with gaps) |
| `pr-test-analyzer.agent-adequate-template.md` | `pr-test-analyzer.md` | Adequate coverage report (no critical gaps) |
| `silent-failure-hunter.agent-report-template.md` | `silent-failure-hunter.md` | Silent failure analysis report (with issues) |
| `silent-failure-hunter.agent-pass-template.md` | `silent-failure-hunter.md` | No silent failures found report |
| `type-design-analyzer.agent-report-template.md` | `type-design-analyzer.md` | Type design analysis report |
| `web-researcher.agent-report-template.md` | `web-researcher.md` | Web research findings report |

### Template Reference Pattern

**For Prompt files** (existing pattern — continue using):

```
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

**For Agent files** (new pattern — consistent with prompts):

```
> **Output Template**: See `.github/PRPs/templates/{name}.agent-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

**For Bash heredoc templates** (issue-fix 7.2, 8.2; issue-investigate phase 6):

Replace the heredoc syntax with a `cat` reference:

```bash
# Before (issue-fix 7.2 example)
gh pr create ... --body "$(cat <<'EOF'
[template content]
EOF
)"

# After
gh pr create ... --body "$(cat .github/PRPs/templates/prp-issue-fix.prompt-pr-template.md)"
```

Add a reference comment above the bash command:

```
> **PR Body Template**: See `.github/PRPs/templates/prp-issue-fix.prompt-pr-template.md`
> Load this file for the PR body content structure.
```

### User Flow

1. Maintainer opens `.github/agents/code-reviewer.md` to update PR review output format
2. Reads: `> **Output Template**: See .github/PRPs/templates/code-reviewer.agent-report-template.md`
3. Opens the template file, edits the format
4. Agent instruction logic in `code-reviewer.md` is untouched

---

## Technical Approach

**Feasibility**: HIGH

**Architecture Notes**
- All files are pure markdown — no tooling or parsing required
- `text-file-content-extractor-replacer` skill handles extract-and-replace in one step per block
- Exact start/end line numbers must be read and confirmed before each operation (skill safety rule)
- Bash heredoc blocks in `prp-issue-fix.prompt.md` (7.2, 8.2) and `prp-issue-investigate.prompt.md`
  (Phase 6) require extracting only the heredoc body (markdown content), not the bash wrapper
- The bash command in source files is updated from heredoc to `"$(cat <template-file>)"` so the
  command remains functional and self-documenting

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Line numbers shift between reads and writes | L | Read immediately before each write |
| Heredoc extraction boundary error (picking up EOF marker) | L | Exclude `EOF` and `)` lines; verify at `start-1` and `end+1` |
| Agent "no-issues" template omitted from extraction | L | Explicit inventory table above; verify each agent file has correct count of references |
| README typo causes wrong file to be targeted | L | Treat `codebase-analyst.md` second entry as `codebase-explorer.md` (documented in Open Questions) |

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
| 1 | Extract Prompt Templates | Create 6 template files from 5 prompt files using `text-file-content-extractor-replacer` skill | complete | - | - | `.claude/PRPs/plans/completed/extract-remaining-templates-phase-1.plan.md` |
| 2 | Update Prompt Files | Replace inline template blocks in 5 prompt files with reference instructions | in-progress | - | 1 | `.claude/PRPs/plans/extract-remaining-templates-phase-2.plan.md` |
| 3 | Extract Agent Templates | Create 12 template files from 10 agent files using `text-file-content-extractor-replacer` skill | pending | with 1 | - | - |
| 4 | Update Agent Files | Replace inline `## Output Format` template blocks in 10 agent files with reference instructions | pending | - | 3 | - |

### Phase Details

**Phase 1: Extract Prompt Templates**
- **Goal**: Every remaining prompt template exists as a standalone file
- **Scope**: Use `text-file-content-extractor-replacer` skill in `extract` mode to create each template file; identify exact line ranges before each operation
- **Deliverables**: 6 new files in `.github/PRPs/templates/`:
  - `prp-implement.prompt-summary-template.md`
  - `prp-issue-fix.prompt-pr-template.md`
  - `prp-issue-fix.prompt-review-template.md`
  - `prp-issue-investigate.prompt-comment-template.md`
  - `prp-plan.prompt-summary-template.md`
  - `prp-ralph.prompt-report-template.md`
- **Success signal**: 6 files exist; content matches original embedded blocks verbatim

**Phase 2: Update Prompt Files**
- **Goal**: No inline template blocks remain in the 5 affected prompt files
- **Scope**: Use `text-file-content-extractor-replacer` skill in `replace` mode; for markdown blocks replace with two-line reference instruction; for bash heredoc commands replace heredoc body with `cat <template-file>` and add reference comment above
- **Deliverables**: 5 updated prompt files:
  - `prp-implement.prompt.md` – Phase 6 block → reference
  - `prp-issue-fix.prompt.md` – Section 7.2 heredoc → `cat` ref; section 8.2 heredoc → `cat` ref
  - `prp-issue-investigate.prompt.md` – Phase 6 heredoc → `cat` ref
  - `prp-plan.prompt.md` – REPORT_TO_USER block → reference
  - `prp-ralph.prompt.md` – Section 4.2 code block → reference
- **Success signal**: No markdown template blocks (20+ line) remain inline in these files; each has a reference instruction

**Phase 3: Extract Agent Templates**
- **Goal**: Every agent output format template exists as a standalone file
- **Scope**: Use `text-file-content-extractor-replacer` skill in `extract` mode; content to extract is inside the ` ````markdown ` ... ` ```` ` fences in each `## Output Format` section and the `## If No Issues Found` / `## If Coverage Is Adequate` sections where relevant; extract the content between the fence markers (not the fences themselves)
- **Deliverables**: 12 new files in `.github/PRPs/templates/` (as listed in Template Inventory above)
- **Success signal**: 12 files exist; content matches original inline template blocks verbatim

**Phase 4: Update Agent Files**
- **Goal**: No inline ` ````markdown ` template blocks remain in agent files
- **Scope**: Use `text-file-content-extractor-replacer` skill in `replace` mode; replace each extracted template block (including its surrounding ` ```` ` fences) with a two-line reference instruction; for agents with two templates, add two separate reference instructions
- **Deliverables**: 10 updated agent files:
  - `code-reviewer.md` – main template block → reference
  - `code-simplifier.md` – main template block → reference
  - `codebase-analyst.md` – template block → reference
  - `codebase-explorer.md` – template block → reference
  - `comment-analyzer.md` – template block → reference
  - `gpui-researcher.md` – template block → reference
  - `pr-test-analyzer.md` – 2 template blocks → 2 references
  - `silent-failure-hunter.md` – 2 template blocks → 2 references
  - `type-design-analyzer.md` – template block → reference
  - `web-researcher.md` – template block → reference
- **Success signal**: No ` ````markdown ` template blocks remain in agent files; each has a reference instruction per template

### Parallelism Notes

Phase 1 (prompt extractions) and Phase 3 (agent extractions) are fully independent — they touch
different files. They can therefore run in parallel across subagents, with Phase 2 following only
Phase 1 and Phase 4 following only Phase 3. Within each phase, individual file operations are
independent and can also be done in parallel.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Agent template naming convention | `<name>.agent-<function>-template.md` | `<name>.prompt-<function>-template.md` (reuse) | Agent files are not prompts; `.agent-` makes the source type explicit and prevents name collisions |
| Bash heredoc extraction | Extract heredoc body only (markdown content); update bash command to `cat <file>` | Extract full bash block; keep heredoc inline | Template file contains only the human-readable markdown; bash plumbing stays in the prompt; command becomes shorter and self-documenting |
| codebase-explorer.md treatment | Extract its exploration template (README TODO had a typo; corrected to `codebase-explorer.md`) | N/A — typo confirmed and fixed by maintainer | README listed `codebase-analyst.md` twice; second entry was a typo for `codebase-explorer.md`, which holds the exploration report template |
| docs-impact-agent.md | Not in scope | Extract its template too | Not listed in README TODO; no extraction requested |
| markdown-linter validation | Skip per explicit user instruction | Run linter as in first extraction | Explicitly excluded in requirements |
| Content fidelity | Extract verbatim | Normalize/clean up | Avoids unintended behavior changes; preserves all placeholder syntax |

---

## Research Summary

**Existing Patterns**
- `.github/PRPs/templates/` directory confirmed — 20 files already exist from first extraction
- Naming convention `<prompt>.prompt-<function>-template.md` established and consistent
- Reference instruction format confirmed in `prp-prd.prompt.md`, `prp-plan.prompt.md`, and others

**Technical Context**
- `text-file-content-extractor-replacer` skill confirmed available in `.github/skills/`
- Skill operates on line ranges; exact line numbers must be confirmed by file-reading before each write
- Skill's `extract-and-replace` mode is the most efficient path: extract template to file, then replace source block in one sequence
- Windows (PowerShell) commands apply for this workspace (OS: Windows per environment info)
