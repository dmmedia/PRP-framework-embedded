# Feature: Extract Prompt Output Templates — Phase 2: Extract

## Summary

Extract the 19 embedded output format templates from all 13 prompt files in `.github/prompts/`
into standalone markdown files under `.github/PRPs/templates/`. Each source prompt has one or two
fenced template blocks; this phase reads each block verbatim and writes it as a standalone file
named `<prompt-name>.prompt-<function>-template.md`. No prompt files are modified in this phase
— that is Phase 3.

## User Story

As a framework maintainer
I want to find any output format template as a standalone file in `.github/PRPs/templates/`
So that I can read or update a template without scrolling through 300–600 line prompt files

## Problem Statement

All 13 prompt files embed their output format templates inline as fenced code blocks. Maintainers
must scan hundreds of lines to locate a template, and editing a template risks accidental changes
to surrounding instruction logic.

## Solution Statement

Read each source prompt at the identified line ranges, extract the content between fence markers
verbatim, and write each to a dedicated file in `.github/PRPs/templates/`. 19 files total across
13 source prompts. No content is altered — extraction only.

## Metadata

| Field | Value |
|---|---|
| Type | REFACTOR |
| Complexity | MEDIUM |
| Systems Affected | `.github/PRPs/templates/` (target), `.github/prompts/` (source, read-only in this phase) |
| Dependencies | Phase 1 complete (`.github/PRPs/templates/` directory exists) ✅ |
| Estimated Tasks | 20 (19 creates + 1 validate) |

---

## UX Design

### Before State

```
╔════════════════════════════════════════════════════════════════════╗
║                           BEFORE STATE                             ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Maintainer needs to update PR body format                         ║
║                                                                    ║
║  ┌──────────────────┐   scroll 300–600 lines   ┌───────────────┐  ║
║  │ prp-pr.prompt.md │ ─────────────────────── ► │  Find block   │  ║
║  │  (344 lines)     │                           │  ~L180–L215   │  ║
║  └──────────────────┘                           └───────────────┘  ║
║                                │                                   ║
║          risk: accidentally    │                                   ║
║          edit instruction      ▼                                   ║
║          logic above/below  ┌──────────────────────────────────┐  ║
║                             │  Inline template block (bash EOF) │  ║
║                             │  surrounded by shell commands     │  ║
║                             └──────────────────────────────────┘  ║
║                                                                    ║
║  USER_FLOW: Open prompt → scroll → find template → edit carefully  ║
║  PAIN_POINT: Template mixed with agent logic, easy breakage        ║
║  DATA_FLOW: template inline → agent reads full file at runtime     ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════════╗
║                           AFTER STATE                              ║
╠════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Maintainer needs to update PR body format                         ║
║                                                                    ║
║  ┌──────────────────────────────────────────────┐                 ║
║  │ .github/PRPs/templates/                      │                 ║
║  │   prp-pr.prompt-pr-template.md  ◄── OPEN     │                 ║
║  │   prp-pr.prompt-summary-template.md          │                 ║
║  └──────────────────────────────────────────────┘                 ║
║                           │                                        ║
║                           ▼                                        ║
║               ┌───────────────────────┐                           ║
║               │  Pure template file   │                           ║
║               │  No instruction logic │                           ║
║               └───────────────────────┘                           ║
║                                                                    ║
║  USER_FLOW: Navigate to .github/PRPs/templates/ → open file        ║
║  VALUE_ADD: Find any template in under 10 seconds                  ║
║  DATA_FLOW: prompt references file → agent loads file at runtime   ║
║                                                                    ║
╚════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|---|---|---|---|
| `.github/prompts/prp-pr.prompt.md` | Template inline at L180–L215 | Template referenced | Edit template without touching agent logic |
| `.github/PRPs/templates/` | Only README.md | 19 template files | Direct access to any output format |
| Any prompt file | Mixed logic+template | Logic only (Phase 3) | Faster comprehension of agent instructions |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/PRPs/templates/README.md` | all (56 lines) | Naming convention, reference pattern, and template inventory to follow |
| P0 | `.github/prompts/prp-commit.prompt.md` | 60–80 | Simplest template block — use to calibrate extraction before tackling longer files |
| P1 | `.github/prompts/prp-ralph-cancel.prompt.md` | 30–50 | Special case: 3-space indented fence — understand before extracting |
| P1 | `.github/prompts/prp-pr.prompt.md` | 170–230 | Special case: template inside bash heredoc, not a markdown fence |
| P1 | `.github/prompts/prp-issue-investigate.prompt.md` | 255–270 | Special case: 4-backtick outer fence (contains nested code blocks) |
| P1 | `.github/prompts/prp-plan.prompt.md` | 350–370 | Special case: 4-backtick outer fence (308-line template with nested code blocks) |

---

## Patterns to Mirror

**TEMPLATE_EXTRACTION_PATTERN:**

```
// SOURCE: .github/prompts/prp-commit.prompt.md:68–73
// STANDARD CASE — copy lines BETWEEN the fence markers (not the fence lines themselves):

Source file contains:
  ``` ```markdown          ← fence start at L68 (NOT copied to template)
  **Committed**: {hash} - {message}
  **Files**: {count} files (+{add}/-{del})
  
  Next: `git push` or `/prp-pr`
  ``` ```                  ← fence end at L73 (NOT copied to template)

Result file contains:
  **Committed**: {hash} - {message}
  **Files**: {count} files (+{add}/-{del})
  
  Next: `git push` or `/prp-pr`
```

**HEREDOC_EXTRACTION_PATTERN (prp-pr PR template only):**

```
// SOURCE: .github/prompts/prp-pr.prompt.md:~L180–L230
// heredoc case — copy lines BETWEEN <<'EOF' marker and EOF terminator:

Source file contains:
  ``` ```bash
  gh pr create \
    --title "{title}" \
    --base "{base-branch}" \
    --body "$(cat <<'EOF'    ← heredoc start (NOT copied)
  ## Summary                  ← template content starts here
  ...
  EOF
  )"
  ``` ```

Result file contains:
  ## Summary
  {1-2 sentence description}
  ...
  ## Related Issues
  {Any linked issues from commit messages, or "None"}
```

**FOUR_BACKTICK_EXTRACTION_PATTERN (prp-issue-investigate and prp-plan plan template):**

```
// SOURCE: .github/prompts/prp-issue-investigate.prompt.md:~L260–L441
// 4-backtick outer fence — content starts after ````markdown line:

Source file contains:
  ```` ````markdown          ← 4-backtick fence start (NOT copied)
  # Investigation: {Title}   ← template content starts here
  ...inner code blocks like ```typescript use 3 backticks, preserved as-is...
  ```` ````                  ← 4-backtick fence end (NOT copied)

Result file contains:
  # Investigation: {Title}
  ...with inner 3-backtick code blocks intact...
```

**INDENTED_FENCE_EXTRACTION_PATTERN (prp-ralph-cancel only):**

```
// SOURCE: .github/prompts/prp-ralph-cancel.prompt.md:L37–L50
// 3-space indented fence — strip the 3-space indent from content lines:

Source file contains (each line has 3-space leading indent):
     ```markdown           ← indented fence start (NOT copied)
     ## Ralph Loop Cancelled
     **Was at**: Iteration {N}
     ...
     ```                   ← indented fence end (NOT copied)

Result file contains (no leading indent):
  ## Ralph Loop Cancelled
  **Was at**: Iteration {N}
  ...
```

---

## Files to Change

| File | Action | Source |
|------|--------|--------|
| `.github/PRPs/templates/prp-codebase-question.prompt-research-template.md` | CREATE | `prp-codebase-question.prompt.md:~L223–L274` |
| `.github/PRPs/templates/prp-codebase-question.prompt-summary-template.md` | CREATE | `prp-codebase-question.prompt.md:~L310–L336` |
| `.github/PRPs/templates/prp-commit.prompt-output-template.md` | CREATE | `prp-commit.prompt.md:L69–L72` |
| `.github/PRPs/templates/prp-debug.prompt-report-template.md` | CREATE | `prp-debug.prompt.md:~L204–L264` |
| `.github/PRPs/templates/prp-implement.prompt-report-template.md` | CREATE | `prp-implement.prompt.md:~L301–L388` |
| `.github/PRPs/templates/prp-issue-fix.prompt-report-template.md` | CREATE | `prp-issue-fix.prompt.md:~L539–L572` |
| `.github/PRPs/templates/prp-issue-investigate.prompt-artifact-template.md` | CREATE | `prp-issue-investigate.prompt.md:~L261–L440` (4-backtick fence) |
| `.github/PRPs/templates/prp-plan.prompt-design-template.md` | CREATE | `prp-plan.prompt.md:~L241–L279` (plain fence) |
| `.github/PRPs/templates/prp-plan.prompt-plan-template.md` | CREATE | `prp-plan.prompt.md:~L359–L663` (4-backtick outer fence) |
| `.github/PRPs/templates/prp-pr.prompt-pr-template.md` | CREATE | `prp-pr.prompt.md:~L186–L214` (heredoc content) |
| `.github/PRPs/templates/prp-pr.prompt-summary-template.md` | CREATE | `prp-pr.prompt.md:~L270–L298` |
| `.github/PRPs/templates/prp-prd.prompt-prd-template.md` | CREATE | `prp-prd.prompt.md:L222–L372` |
| `.github/PRPs/templates/prp-prd.prompt-summary-template.md` | CREATE | `prp-prd.prompt.md:~L382–L419` |
| `.github/PRPs/templates/prp-ralph-cancel.prompt-cancel-template.md` | CREATE | `prp-ralph-cancel.prompt.md:L38–L49` (3-space indent stripped) |
| `.github/PRPs/templates/prp-ralph.prompt-setup-template.md` | CREATE | `prp-ralph.prompt.md:L125–L149` (startup message block §2.2) |
| `.github/PRPs/templates/prp-ralph.prompt-progress-template.md` | CREATE | `prp-ralph.prompt.md:~L224–L245` |
| `.github/PRPs/templates/prp-review-agents.prompt-summary-template.md` | CREATE | `prp-review-agents.prompt.md:L123–L155` |
| `.github/PRPs/templates/prp-review.prompt-report-template.md` | CREATE | `prp-review.prompt.md:~L336–L421` (includes YAML frontmatter) |
| `.github/PRPs/templates/prp-review.prompt-summary-template.md` | CREATE | `prp-review.prompt.md:~L479–L508` |

---

## NOT Building (Scope Limits)

- **No prompt file modifications** — Phase 3 handles replacing inline blocks with references
- **No state file template extraction** (`prp-ralph.prompt.md §2.1`) — not in the 19 target files
- **No Phase 6 output blocks from `prp-debug` or `prp-implement`** — these exist but are not in the 19 target files per PRD
- **No PR body block from `prp-issue-fix` (bash heredoc)** — not in the 19 target files per PRD
- **No Phase 7 report block from `prp-issue-investigate`** — not in the 19 target files per PRD
- **No third template block from `prp-plan`** (the `<output>` tag block) — not in the 19 target files per PRD
- **No content normalization** — templates extracted as-is; deduplication is a separate concern
- **No README update** — README already lists all 19 files and was created in Phase 1

---

## Step-by-Step Tasks

Execute in order. All CREATE tasks are independent and may be executed in any order. Task 20 validates all 19 created.

---

### Task 1: CREATE `prp-codebase-question.prompt-research-template.md`

- **ACTION**: CREATE template file from embedded research document block
- **SOURCE FILE**: `.github/prompts/prp-codebase-question.prompt.md`
- **READ LINES**: ~L217–L280 (section `### 5.4 Write Research Document`)
- **FENCE START**: First ` ```markdown ` in that section
- **FENCE END**: Matching ` ``` `
- **CONTENT**: YAML frontmatter + Research sections: `# Research: {query}`, `## Research Question`, `## Summary`, `## Detailed Findings`, `## Code References`, `## Architecture Documentation`, `## Open Questions`
- **GOTCHA**: This block contains a YAML frontmatter block (`---` ... `---`) as the first part of the template — preserve it verbatim including the `---` delimiters
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-codebase-question.prompt-research-template.md`

---

### Task 2: CREATE `prp-codebase-question.prompt-summary-template.md`

- **ACTION**: CREATE template file from Phase 6 output block
- **SOURCE FILE**: `.github/prompts/prp-codebase-question.prompt.md`
- **READ LINES**: ~L305–L342 (section `## Phase 6: OUTPUT - Present to User`)
- **FENCE START**: ` ```markdown ` immediately after "```markdown" in that section
- **FENCE END**: Matching ` ``` `
- **CONTENT**: `## Research Complete`, `**Question**:`, `**Document**:`, `### Summary`, `### Key Findings`, `### Architecture`, `### Open Questions`, `### Follow-up`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-codebase-question.prompt-summary-template.md`

---

### Task 3: CREATE `prp-commit.prompt-output-template.md`

- **ACTION**: CREATE template file from Phase 4 OUTPUT block (simplest template, 4 lines)
- **SOURCE FILE**: `.github/prompts/prp-commit.prompt.md`
- **READ LINES**: L63–L78 (section `## Phase 4: OUTPUT`)
- **FENCE START**: L68 ` ```markdown `
- **FENCE END**: L73 ` ``` `
- **CONTENT** (4 lines exactly):
  ```
  **Committed**: {hash} - {message}
  **Files**: {count} files (+{add}/-{del})

  Next: `git push` or `/prp-pr`
  ```
- **GOTCHA**: File is only 85 lines total. Section immediately follows and new section immediately precedes with `---` separators
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-commit.prompt-output-template.md`; content should be exactly 4 lines

---

### Task 4: CREATE `prp-debug.prompt-report-template.md`

- **ACTION**: CREATE template file from Phase 5 REPORT template block
- **SOURCE FILE**: `.github/prompts/prp-debug.prompt.md`
- **READ LINES**: ~L198–L270 (section `### 5.2 Generate Report`)
- **FENCE START**: ` ```markdown ` after `**Path**:` instruction
- **FENCE END**: Matching ` ``` ` before `**PHASE_5_CHECKPOINT:**`
- **CONTENT**: `# Root Cause Analysis`, `## Evidence Chain`, `## Git History`, `## Fix Specification` (with inner code block using ` ```{language} ` fence)
- **GOTCHA**: Template content contains a nested ` ```{language} ` code block for implementation guidance — preserve it verbatim. The outer fence is 3-backtick, the inner fence is also 3-backtick. This is valid in a standalone .md file (no fence nesting issue since the outer fence markers are removed)
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-debug.prompt-report-template.md`

---

### Task 5: CREATE `prp-implement.prompt-report-template.md`

- **ACTION**: CREATE template file from Phase 5 REPORT template block (~87 lines)
- **SOURCE FILE**: `.github/prompts/prp-implement.prompt.md`
- **READ LINES**: ~L296–L394 (section `## Phase 5: REPORT - Create Implementation Report`)
- **FENCE START**: ` ```markdown ` after `**Path**:` instruction in §5.2
- **FENCE END**: Matching ` ``` ` before `### 5.3 Update Source PRD`
- **CONTENT**: `# Implementation Report`, `## Summary`, `## Assessment vs Reality` (table), `## Tasks Completed` (table), `## Validation Results` (table), `## Files Changed` (table), `## Deviations from Plan`, `## Issues Encountered`, `## Tests Written` (table), `## Next Steps`
- **GOTCHA**: Template contains multiple markdown tables — preserve pipe characters and alignment exactly
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-implement.prompt-report-template.md`

---

### Task 6: CREATE `prp-issue-fix.prompt-report-template.md`

- **ACTION**: CREATE template file from Phase 10 REPORT output block (~34 lines)
- **SOURCE FILE**: `.github/prompts/prp-issue-fix.prompt.md`
- **READ LINES**: ~L534–L578 (section `## Phase 10: REPORT - Output to User`)
- **FENCE START**: ` ```markdown ` immediately after the phase header
- **FENCE END**: Matching ` ``` ` before `## Handling Edge Cases`
- **CONTENT**: `## Implementation Complete`, `**Issue**:`, `**Branch**:`, `**PR**:`, `### Changes Made` (table), `### Validation` (table), `### Self-Review`, `### Artifact`, `### Next Steps`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-issue-fix.prompt-report-template.md`

---

### Task 7: CREATE `prp-issue-investigate.prompt-artifact-template.md`

- **ACTION**: CREATE template file from Phase 4 GENERATE artifact block (~180 lines)
- **SOURCE FILE**: `.github/prompts/prp-issue-investigate.prompt.md`
- **READ LINES**: ~L254–L445 (section `## Phase 4: GENERATE - Create Artifact`)
- **FENCE START**: ```` ````markdown ```` (4-backtick fence) — look for 4 backticks, NOT 3
- **FENCE END**: Matching ```` ```` ```` (4 backticks)
- **CONTENT**: Full investigation artifact structure starting with `# Investigation: {Title}`, including `### Assessment` table, `## Problem Statement`, `## Analysis` (with nested code blocks), `## Implementation Plan`, `## Patterns to Follow`, `## Edge Cases & Risks`, `## Validation`, `## Scope Boundaries`, `## Metadata`
- **GOTCHA 1**: Source uses 4-backtick outer fence to accommodate inner 3-backtick code blocks (e.g., ```` ```typescript ````, ```` ```bash ````). The standalone file will contain these inner 3-backtick blocks directly — no fence nesting issue
- **GOTCHA 2**: Template has a `<!-- HTML comment -->` block with notes on Severity vs Priority. Preserve verbatim
- **GOTCHA 3**: File is 624 lines. Phase 4 starts at L239. The 4-backtick fence for the artifact appears around L260–L261. Do NOT confuse with the Phase 7 REPORT block further in the file (around L547) — that is NOT one of the 19 targets
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-issue-investigate.prompt-artifact-template.md`; file should be ~175–185 lines

---

### Task 8: CREATE `prp-plan.prompt-design-template.md`

- **ACTION**: CREATE template file from Phase 4 DESIGN ASCII art block (~40 lines)
- **SOURCE FILE**: `.github/prompts/prp-plan.prompt.md`
- **READ LINES**: ~L236–L283 (section `## Phase 4: DESIGN - UX Transformation`)
- **FENCE START**: Plain ` ``` ` (NO language specifier) immediately after `**CREATE ASCII diagrams...:**`
- **FENCE END**: Matching ` ``` `
- **CONTENT**: Two ASCII box-drawing diagrams (BEFORE STATE + AFTER STATE) with Unicode box characters (╔, ║, ╚, ┌, ─, ┐, └, ┘, ►, ▼, etc.)
- **GOTCHA 1**: This fence has NO language tag (just ` ``` `, not ` ```markdown `). This is intentional — it is a plain code block showing ASCII art
- **GOTCHA 2**: The block immediately follows `**CREATE ASCII diagrams...:**` and ends immediately before `**DOCUMENT interaction changes:**`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-plan.prompt-design-template.md`; open and verify ASCII box characters render correctly

---

### Task 9: CREATE `prp-plan.prompt-plan-template.md`

- **ACTION**: CREATE template file from Phase 6 GENERATE full plan structure (~305 lines)
- **SOURCE FILE**: `.github/prompts/prp-plan.prompt.md`
- **READ LINES**: ~L351–L668 (section `## Phase 6: GENERATE - Implementation Plan File`)
- **FENCE START**: ` ```markdown ` line after `**PLAN_STRUCTURE** (the template to fill and save):`
- **FENCE END**: ```` ```` ```` (4-backtick close — NOT a 3-backtick close, look for exactly 4 backticks on their own line before `</process>`)
- **CONTENT**: Full plan template: `# Feature: {Feature Name}`, all `##` sections through `## Notes`; content internally uses ` ```typescript `, ` ```bash ` blocks (these are preserved as-is)
- **GOTCHA 1**: Outer closing fence is 4 backticks (```` ```` ````), NOT 3, to accommodate inner 3-backtick code blocks. Do NOT stop at the first ` ``` ` you see inside the template — scan to the ```` ```` ```` line.
- **GOTCHA 2**: This is the largest template (300+ lines). After extraction, the standalone file will have 3-backtick code blocks that are valid markdown — no fence issues
- **GOTCHA 3**: The ` ```markdown ` opening fence in the source is 3-backtick. Stop reading at the ```` ```` ```` line that appears just before `</process>` closing tag
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-plan.prompt-plan-template.md`; file should be ~300–310 lines

---

### Task 10: CREATE `prp-pr.prompt-pr-template.md`

- **ACTION**: CREATE template file from bash heredoc PR body (~30 lines)
- **SOURCE FILE**: `.github/prompts/prp-pr.prompt.md`
- **READ LINES**: ~L174–L235 (section `### 4.2 If No Template - Use Default Format`)
- **FENCE STRUCTURE**: Content is inside a ` ```bash ` block containing a `gh pr create` command with `--body "$(cat <<'EOF' ... EOF)"` heredoc
- **CONTENT TO EXTRACT**: Only the markdown lines between `<<'EOF'` and `EOF` (the heredoc body), NOT the shell script surrounding them. Content: `## Summary`, `## Changes`, `## Files Changed`, `<details>...</details>` block, `## Testing`, `## Related Issues`
- **GOTCHA 1**: Do NOT include the ```` ```bash ````, `gh pr create`, `--body`, `<<'EOF'`, `EOF`, `)"`, or closing ` ``` ` in the template file. Only the markdown PR body between those heredoc markers
- **GOTCHA 2**: Content includes an HTML `<details><summary>...</summary>...</details>` block — preserve verbatim including HTML tags
- **GOTCHA 3**: The heredoc content has indentation from the shell script. Preserve the indentation as-is (the template is the PR body, indentation is 0 in the heredoc itself)
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-pr.prompt-pr-template.md`; file should start with `## Summary`

---

### Task 11: CREATE `prp-pr.prompt-summary-template.md`

- **ACTION**: CREATE template file from Phase 6 OUTPUT summary block (~30 lines)
- **SOURCE FILE**: `.github/prompts/prp-pr.prompt.md`
- **READ LINES**: ~L265–L305 (section `## Phase 6: OUTPUT - Report to User`)
- **FENCE START**: ` ```markdown `
- **FENCE END**: Matching ` ``` `
- **CONTENT**: `## Pull Request Created`, `**PR**:`, `**URL**:`, `**Title**:`, `**Base**:`, `### Summary`, `### Changes`, `### Files`, `### Checks`, `### Next Steps`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-pr.prompt-summary-template.md`

---

### Task 12: CREATE `prp-prd.prompt-prd-template.md`

- **ACTION**: CREATE template file from Phase 7 GENERATE PRD document block (~150 lines)
- **SOURCE FILE**: `.github/prompts/prp-prd.prompt.md`
- **READ LINES**: L215–L378 (section `## Phase 7: GENERATE - Write PRD`, sub-section `### PRD Template`)
- **FENCE START**: L221 ` ```markdown `
- **FENCE END**: ~L373 ` ``` `
- **CONTENT**: Full PRD template: `# {Product/Feature Name}`, `## Problem Statement`, `## Evidence`, `## Proposed Solution`, `## Key Hypothesis`, `## What We're NOT Building`, `## Success Metrics` (table), `## Open Questions`, `## Users & Context`, `## Solution Detail` (MoSCoW table), `## Technical Approach` (risk table), `## Implementation Phases` (table with HTML comment block), `## Decisions Log`, `## Research Summary`
- **GOTCHA 1**: Template contains an HTML comment block `<!-- STATUS: pending|in-progress|complete ... -->` inside `## Implementation Phases`. Preserve verbatim
- **GOTCHA 2**: Template ends with `*Generated: {timestamp}*` and `*Status: DRAFT - needs validation*` — include these lines
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-prd.prompt-prd-template.md`; file should be ~150 lines

---

### Task 13: CREATE `prp-prd.prompt-summary-template.md`

- **ACTION**: CREATE template file from Phase 8 OUTPUT summary block (~38 lines)
- **SOURCE FILE**: `.github/prompts/prp-prd.prompt.md`
- **READ LINES**: ~L376–L425 (section `## Phase 8: OUTPUT - Summary`)
- **FENCE START**: ` ```markdown ` after `After generating, report:`
- **FENCE END**: Matching ` ``` `
- **CONTENT**: `## PRD Created`, `**File**:`, `### Summary`, `### Validation Status` (table), `### Open Questions`, `### Recommended Next Step`, `### Implementation Phases` (table), `### To Start Implementation`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-prd.prompt-summary-template.md`

---

### Task 14: CREATE `prp-ralph-cancel.prompt-cancel-template.md`

- **ACTION**: CREATE template file from cancel report block (~12 lines)
- **SOURCE FILE**: `.github/prompts/prp-ralph-cancel.prompt.md`
- **READ LINES**: L33–50 (step `3d. Report:`)
- **FENCE START**: L37 `   ```markdown` — note 3-space leading indent on the fence line
- **FENCE END**: ~L50 `   ``` ` — note 3-space leading indent on the fence line
- **CONTENT**: `## Ralph Loop Cancelled`, `**Was at**: Iteration {N}`, `**Plan**: {plan_path}`, body text about preserved work, `To resume later:` with two bullet points
- **GOTCHA**: All content lines in the source have 3-space leading indentation (artifact of being inside a nested list item). Strip the 3-space prefix from each line when creating the standalone file. The semantic content has no indentation
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-ralph-cancel.prompt-cancel-template.md`; first line should be `## Ralph Loop Cancelled` (no leading spaces)

---

### Task 15: CREATE `prp-ralph.prompt-setup-template.md`

- **ACTION**: CREATE template file from Phase 2 §2.2 startup message block (~26 lines)
- **SOURCE FILE**: `.github/prompts/prp-ralph.prompt.md`
- **READ LINES**: L120–L155 (section `### 2.2 Display Startup Message`)
- **FENCE START**: L124 ` ```markdown ` immediately after `### 2.2 Display Startup Message`
- **FENCE END**: L150 ` ``` `
- **CONTENT**: `## PRP Ralph Loop Activated`, `**Plan**: {file_path}`, `**Iteration**: 1`, `**Max iterations**: {N}`, description of stop hook behavior, `To monitor:` and `To cancel:` bullets, `CRITICAL REQUIREMENTS:` list, `Starting iteration 1...`
- **GOTCHA**: There are TWO template blocks in Phase 2 —
  - §2.1 "Create State File" block at L88–L120 (state file structure with YAML frontmatter) — this is NOT one of the 19 targets
  - §2.2 "Display Startup Message" block at L124–L150 — THIS is the target (`prp-ralph.prompt-setup-template.md`)
  Map to the §2.2 startup message, not §2.1 state file
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-ralph.prompt-setup-template.md`; first line should be `## PRP Ralph Loop Activated`

---

### Task 16: CREATE `prp-ralph.prompt-progress-template.md`

- **ACTION**: CREATE template file from Phase 3 §3.8 progress log entry block (~22 lines)
- **SOURCE FILE**: `.github/prompts/prp-ralph.prompt.md`
- **READ LINES**: ~L218–L252 (section `### 3.8 Update State File Progress Log`)
- **FENCE START**: ` ```markdown ` after `Append to Progress Log section using this format:`
- **FENCE END**: Matching ` ``` `
- **CONTENT**: `## Iteration {N} - {ISO timestamp}`, `### Completed`, `### Validation Status` (list with PASS/FAIL entries), `### Learnings`, `### Next Steps`, `---`
- **GOTCHA**: There is a SECOND template block in §3.9 "Consolidate Codebase Patterns" further down — that is NOT a target. Stop after extracting the §3.8 block
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-ralph.prompt-progress-template.md`; first line should be `## Iteration {N} - {ISO timestamp}`

---

### Task 17: CREATE `prp-review-agents.prompt-summary-template.md`

- **ACTION**: CREATE template file from `### Summary Format` block (~34 lines)
- **SOURCE FILE**: `.github/prompts/prp-review-agents.prompt.md`
- **READ LINES**: L115–L160 (section `### Summary Format`)
- **FENCE START**: L122 ` ```markdown `
- **FENCE END**: L156 ` ``` `
- **CONTENT**: `## PR Review Summary`, `### Critical Issues (X found)` (table), `### Important Issues (X found)` (table), `### Suggestions (X found)` (table), `### Strengths`, `### Documentation Issues`, `### Verdict`, `### Recommended Actions`
- **GOTCHA**: This file has NO phase headers — it uses top-level prose sections. The target block is under `## Result Aggregation` → `### Summary Format`
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-review-agents.prompt-summary-template.md`

---

### Task 18: CREATE `prp-review.prompt-report-template.md`

- **ACTION**: CREATE template file from Phase 6 REPORT template block (~86 lines)
- **SOURCE FILE**: `.github/prompts/prp-review.prompt.md`
- **READ LINES**: ~L330–L430 (section `## Phase 6: REPORT - Generate Review`, sub-section `### 6.2 Generate Report File`)
- **FENCE START**: ` ```markdown ` after `**Path**: .claude/PRPs/reviews/pr-{NUMBER}-review.md`
- **FENCE END**: Matching ` ``` ` before `**PHASE_6_CHECKPOINT:**`
- **CONTENT**: YAML frontmatter block (`---` ... `---`), `# PR Review: #{NUMBER}`, `## Summary`, `## Implementation Context` (table), `## Changes Overview` (table), `## Issues Found` (### Critical, ### High Priority, ### Medium Priority, ### Suggestions), `## Validation Results` (table), `## Pattern Compliance` (checklist), `## What's Good`, `## Recommendation`
- **GOTCHA 1**: Template STARTS with a YAML frontmatter block (`---` / `pr:`, `title:`, etc. / `---`). Include this verbatim — it is part of the template
- **GOTCHA 2**: `## Recommendation` section is the last `##` section. Content after it (the conditional APPROVE/REQUEST CHANGES/BLOCK paragraphs) is also part of the template
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-review.prompt-report-template.md`; first line should be `---` (YAML frontmatter start)

---

### Task 19: CREATE `prp-review.prompt-summary-template.md`

- **ACTION**: CREATE template file from Phase 8 OUTPUT block (~30 lines)
- **SOURCE FILE**: `.github/prompts/prp-review.prompt.md`
- **READ LINES**: ~L474–L515 (section `## Phase 8: OUTPUT - Report to User`)
- **FENCE START**: ` ```markdown ` immediately after the Phase 8 header
- **FENCE END**: Matching ` ``` `
- **CONTENT**: `## PR Review Complete`, `**PR**:`, `**URL**:`, `**Recommendation**:`, `### Issues Found` (table with severity counts), `### Validation` (table), `### Artifacts`, `### Next Steps`
- **GOTCHA**: Phase 8 is the SECOND template block in prp-review.prompt.md. The first is the report file template at Phase 6 (Task 18). Scan past Phase 7 to reach Phase 8
- **VALIDATE**: `Test-Path .github/PRPs/templates/prp-review.prompt-summary-template.md`; first line should be `## PR Review Complete`

---

### Task 20: VALIDATE All 19 Template Files Exist

- **ACTION**: Verify all 19 files were created successfully
- **IMPLEMENT**: Run the validation command and count files
- **VALIDATE**:
  ```powershell
  $templates = Get-ChildItem .github/PRPs/templates/ -Filter "*.prompt-*-template.md"
  Write-Host "Template files found: $($templates.Count)"
  $templates | ForEach-Object { Write-Host "  ✓ $($_.Name)" }
  if ($templates.Count -eq 19) { Write-Host "SUCCESS: All 19 templates created" } else { Write-Host "FAILURE: Expected 19, found $($templates.Count)" }
  ```
  **EXPECT**: `Template files found: 19` and `SUCCESS: All 19 templates created`
- **ALSO VERIFY**: `Get-ChildItem .github/PRPs/templates/ | Measure-Object` returns 20 files total (19 templates + README.md)

---

## Testing Strategy

### Verification Checklist per Template

For each of the 19 template files, verify:

- [ ] File exists at `.github/PRPs/templates/{name}`
- [ ] First line matches expected first line (documented in each task)
- [ ] No fence markers (` ``` ` or ```` ```` ````) at start or end of file — those stay in the source
- [ ] `{placeholder}` variables preserved exactly as-is (not substituted)
- [ ] All markdown tables intact (pipe characters and dashes present)
- [ ] Nested code blocks present where documented (Tasks 4, 7, 9)
- [ ] YAML frontmatter present where documented (Tasks 1, 18)

### Edge Cases Checklist

- [ ] **Task 7 (artifact)**: Inner 3-backtick code blocks intact after removing 4-backtick outer fence
- [ ] **Task 9 (plan template)**: All inner ` ```typescript ` and ` ```bash ` blocks intact after removing outer fence; file is ~300 lines
- [ ] **Task 10 (PR body)**: File starts with `## Summary`, no bash script content included
- [ ] **Task 14 (ralph-cancel)**: No 3-space leading indent on any line; starts with `## Ralph Loop Cancelled`
- [ ] **Task 15 (ralph setup)**: §2.1 state file NOT included; content is startup message only
- [ ] **Task 18 (review report)**: File starts with `---` (YAML frontmatter); includes full Recommendation section

---

## Validation Commands

### Level 1: FILE COUNT

```powershell
Get-ChildItem .github/PRPs/templates/ -Filter "*.prompt-*-template.md" | Measure-Object
```

**EXPECT**: `Count : 19`

### Level 2: SPOT CHECK CONTENT

```powershell
# Verify prp-commit template (simplest — 4 lines)
Get-Content .github/PRPs/templates/prp-commit.prompt-output-template.md

# Verify prp-review report starts with YAML frontmatter
(Get-Content .github/PRPs/templates/prp-review.prompt-report-template.md)[0]
# EXPECT: ---

# Verify prp-ralph-cancel has no leading spaces
(Get-Content .github/PRPs/templates/prp-ralph-cancel.prompt-cancel-template.md)[0]
# EXPECT: ## Ralph Loop Cancelled  (no leading spaces)

# Verify prp-pr PR template starts with ## Summary (no bash heredoc)
(Get-Content .github/PRPs/templates/prp-pr.prompt-pr-template.md)[0]
# EXPECT: ## Summary

# Verify prp-ralph setup is startup message (not state file)
(Get-Content .github/PRPs/templates/prp-ralph.prompt-setup-template.md)[0]
# EXPECT: ## PRP Ralph Loop Activated
```

**EXPECT**: Each check returns the expected first line

### Level 3: LINE COUNTS

```powershell
# Verify largest template (plan) is substantial
(Get-Content .github/PRPs/templates/prp-plan.prompt-plan-template.md).Count
# EXPECT: ~300–310 lines

# Verify artifact template is substantial
(Get-Content .github/PRPs/templates/prp-issue-investigate.prompt-artifact-template.md).Count
# EXPECT: ~175–185 lines

# Verify commit template is compact
(Get-Content .github/PRPs/templates/prp-commit.prompt-output-template.md).Count
# EXPECT: 4–5 lines
```

### Level 4: NO FENCE BLEED CHECK

```powershell
# Ensure no template file starts/ends with a fence marker
$issues = @()
Get-ChildItem .github/PRPs/templates/ -Filter "*.prompt-*-template.md" | ForEach-Object {
    $lines = Get-Content $_.FullName
    if ($lines[0] -match '^`{3,}' -or $lines[-1] -match '^`{3,}') {
        $issues += $_.Name
    }
}
if ($issues.Count -eq 0) { Write-Host "PASS: No fence bleed detected" }
else { Write-Host "FAIL: Fence bleed in: $($issues -join ', ')" }
```

**EXPECT**: `PASS: No fence bleed detected`

### Level 5: FULL INVENTORY MATCH

```powershell
$expected = @(
    "prp-codebase-question.prompt-research-template.md",
    "prp-codebase-question.prompt-summary-template.md",
    "prp-commit.prompt-output-template.md",
    "prp-debug.prompt-report-template.md",
    "prp-implement.prompt-report-template.md",
    "prp-issue-fix.prompt-report-template.md",
    "prp-issue-investigate.prompt-artifact-template.md",
    "prp-plan.prompt-design-template.md",
    "prp-plan.prompt-plan-template.md",
    "prp-pr.prompt-pr-template.md",
    "prp-pr.prompt-summary-template.md",
    "prp-prd.prompt-prd-template.md",
    "prp-prd.prompt-summary-template.md",
    "prp-ralph-cancel.prompt-cancel-template.md",
    "prp-ralph.prompt-setup-template.md",
    "prp-ralph.prompt-progress-template.md",
    "prp-review-agents.prompt-summary-template.md",
    "prp-review.prompt-report-template.md",
    "prp-review.prompt-summary-template.md"
)
$missing = $expected | Where-Object { -not (Test-Path ".github/PRPs/templates/$_") }
if ($missing.Count -eq 0) { Write-Host "PASS: All 19 templates present" }
else { $missing | ForEach-Object { Write-Host "MISSING: $_" } }
```

**EXPECT**: `PASS: All 19 templates present`

---

## Acceptance Criteria

- [ ] 19 template files exist in `.github/PRPs/templates/`
- [ ] Each file's first line matches the expected first line documented in the relevant task
- [ ] No file starts or ends with fence markers (backtick lines)
- [ ] `{placeholder}` syntax preserved verbatim throughout all templates
- [ ] `prp-ralph-cancel.prompt-cancel-template.md` has no 3-space leading indentation
- [ ] `prp-pr.prompt-pr-template.md` contains only markdown PR body (no shell script)
- [ ] `prp-ralph.prompt-setup-template.md` contains startup message (not state file)
- [ ] `prp-review.prompt-report-template.md` starts with `---` (YAML frontmatter)
- [ ] Level 1–5 validation commands all pass
- [ ] Source prompt files are unchanged (this phase is read-only for prompt files)

---

## Completion Checklist

- [ ] All 19 tasks completed
- [ ] Level 1: File count = 19 ✓
- [ ] Level 2: Spot checks pass ✓
- [ ] Level 3: Line counts in expected range ✓
- [ ] Level 4: No fence bleed ✓
- [ ] Level 5: Full inventory match ✓
- [ ] Source prompt files unmodified (verify with `git diff .github/prompts/`)

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Wrong fence end line picked (nested code blocks) | MED | HIGH | Tasks 4, 7, 9: Explicitly note 3-backtick vs 4-backtick fences; scan to the outermost closing fence |
| Including heredoc shell script in PR template | LOW | MED | Task 10: Explicitly state to extract only between `<<'EOF'` and `EOF` markers |
| Extracting §2.1 state file as ralph setup template | MED | MED | Task 15: Explicitly states target is §2.2 startup message at L124; first line test confirms |
| 3-space indent left in ralph-cancel template | MED | LOW | Task 14: Strip 3-space prefix; Level 2 spot check verifies first line has no indent |
| Off-by-one fence boundary (extra blank line) | LOW | LOW | Level 4 fence bleed check catches trailing fence markers |
| prp-plan template truncated before ## Notes | LOW | HIGH | Task 9 gotcha: scan to 4-backtick close, NOT first 3-backtick match |

---

## Notes

**Why 19 files, not more**: Six additional template blocks exist in the 13 prompts (§2.1 state file in ralph, Phase 6 output in debug and implement, Phase 7 report in issue-investigate, bash heredoc in issue-fix, third block in plan's `<output>` tag). These were explicitly excluded by the PRD design. Do not extract them.

**Line number drift**: Line numbers in this plan are approximate (~) unless the file is small and line numbers were directly confirmed. Always read the section header context to find the exact fence — do not rely solely on line numbers.

**Content fidelity guarantee**: No template content should be reformatted, normalized, or "improved". Exact whitespace, `{placeholder}` tokens, table alignment, and even stylistic inconsistencies from the original are preserved. The goal is a mechanical extraction, not an edit.

**Phase 3 dependency**: This plan creates only template files. The companion Phase 3 plan will replace the inline blocks in each prompt with reference instructions pointing to these files. Phase 2 output is a precondition for Phase 3.
