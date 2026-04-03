# Feature: Extract Agent Output Templates — Phase 3

## Summary

Extract 12 inline output template blocks from 10 agent files in `.github/agents/` into standalone
markdown files under `.github/PRPs/templates/`. This is Phase 3 of 4 for the full template
extraction effort (Phase 1 and 2 for prompt files are complete; Phase 4 will replace the inline
blocks in agent files with reference instructions). All operations use the
`text-file-content-extractor-replacer` skill in **extract mode only** — source agent files are not
modified in this phase.

## User Story

As a framework maintainer editing an agent output format  
I want to find and edit the output template independently of the surrounding agent instructions  
So that I can update one concern without risking accidental changes to instruction logic

## Problem Statement

All 10 agent files in `.github/agents/` still contain their output format templates inline inside
`` ````markdown `` fences under `## Output Format`. Any maintainer who wants to update an output
format must scroll through 200–300 line agent files and edit template content alongside instruction
logic. After this phase, 12 standalone template files exist and are ready for Phase 4 source-file
updates.

## Solution Statement

Use the `text-file-content-extractor-replacer` skill to copy the template content from each agent
file's inline fenced block into a new file in `.github/PRPs/templates/`. All 12 extractions are
independent and can be done in any order. Source agent files are not modified in this phase.

## Metadata

| Field | Value |
| ---------------- | -------------------------------------------- |
| Type | REFACTOR |
| Complexity | LOW |
| Systems Affected | `.github/agents/`, `.github/PRPs/templates/` |
| Dependencies | None — pure markdown file I/O |
| Estimated Tasks | 12 extraction tasks + 1 validation task |

---

## UX Design

### Before State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────┐   scroll 150+ lines   ┌──────────────────────────┐ ║
║  │  code-reviewer.md    │ ──────────────────────►│  inline ````markdown     │ ║
║  │  (208 lines)         │                         │  ## Code Review Report   │ ║
║  └──────────────────────┘                         │  ... (63 lines)          │ ║
║                                                   └──────────────────────────┘ ║
║                                                                               ║
║  ┌──────────────────────┐   scroll 250+ lines   ┌──────────────────────────┐ ║
║  │  comment-analyzer.md │ ──────────────────────►│  inline ````markdown     │ ║
║  │  (275 lines)         │                         │  ## Comment Analysis     │ ║
║  └──────────────────────┘                         │  ... (138 lines)         │ ║
║                                                   └──────────────────────────┘ ║
║                                                                               ║
║   USER_FLOW: open agent file → scroll past instructions → find template → edit║
║   PAIN_POINT: template is buried inside instruction logic; editing one         ║
║               concern requires navigating and risking the other               ║
║   DATA_FLOW: template content lives inside .md agent file; no standalone file ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────┐                         ┌──────────────────────────┐ ║
║  │  code-reviewer.md    │  (Phase 4: reference)   │  code-reviewer.agent-    │ ║
║  │  (unchanged Ph 3)    │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─►│  report-template.md     │ ║
║  └──────────────────────┘                         │  (standalone, 63 lines)  │ ║
║                                                   └──────────────────────────┘ ║
║                                   │                                            ║
║                                   ▼                                           ║
║                    ┌──────────────────────────────────┐                       ║
║                    │  .github/PRPs/templates/          │                       ║
║                    │  12 new standalone template files │  ◄── created here    ║
║                    └──────────────────────────────────┘                       ║
║                                                                               ║
║   USER_FLOW: open template file directly → edit only the format               ║
║   VALUE_ADD: instruction logic and template are separate files;               ║
║              editing one does not require touching the other                  ║
║   DATA_FLOW: template content in .github/PRPs/templates/*.md;                 ║
║              source agent files unchanged until Phase 4                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `.github/agents/code-reviewer.md` | Template inline at L106–L168 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/code-simplifier.md` | Template inline at L96–L168 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/codebase-analyst.md` | Template inline at L74–L119 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/codebase-explorer.md` | Template inline at L90–L185 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/comment-analyzer.md` | Template inline at L96–L233 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/gpui-researcher.md` | Template inline at L109–L192 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/pr-test-analyzer.md` | 2 templates inline | Both inline (Phase 4 removes them) | Unchanged in Phase 3 |
| `.github/agents/silent-failure-hunter.md` | 2 templates inline | Both inline (Phase 4 removes them) | Unchanged in Phase 3 |
| `.github/agents/type-design-analyzer.md` | Template inline at L154–L262 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/agents/web-researcher.md` | Template inline at L87–L128 | Template inline (Phase 4 removes it) | Unchanged in Phase 3 |
| `.github/PRPs/templates/` | 25 existing templates | 37 templates (12 added) | Maintainer can open any agent template directly |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/skills/text-file-content-extractor-replacer/SKILL.md` | all | Skill operation modes, PowerShell commands, safety rules |
| P0 | `.github/agents/code-reviewer.md` | 100–175 | Confirm exact line range for Task 1 extraction |
| P0 | `.github/agents/code-simplifier.md` | 90–175 | Confirm exact line range for Task 2 extraction |
| P0 | `.github/agents/codebase-analyst.md` | 70–125 | Confirm exact line range for Task 3 extraction |
| P0 | `.github/agents/codebase-explorer.md` | 85–190 | Confirm exact line range for Task 4 extraction |
| P0 | `.github/agents/comment-analyzer.md` | 90–260 | Confirm exact line ranges for Task 5 extraction |
| P0 | `.github/agents/gpui-researcher.md` | 105–215 | Confirm exact line ranges for Task 6 extraction |
| P0 | `.github/agents/pr-test-analyzer.md` | 100–255 | Confirm exact line ranges for Tasks 7–8 extraction |
| P0 | `.github/agents/silent-failure-hunter.md` | 115–285 | Confirm exact line ranges for Tasks 9–10 extraction |
| P0 | `.github/agents/type-design-analyzer.md` | 150–265 | Confirm exact line range for Task 11 extraction |
| P0 | `.github/agents/web-researcher.md` | 80–135 | Confirm exact line range for Task 12 extraction |
| P1 | `.github/PRPs/templates/prp-plan.prompt-plan-template.md` | all | Example of raw-markdown-only template content format |
| P2 | `.claude/PRPs/prds/extract-remaining-templates.prd.md` | 101–175 | Template inventory table and naming spec |

**External Documentation:** None required — pure markdown file I/O.

---

## Patterns to Mirror

**TEMPLATE_FILE_STRUCTURE:**

```markdown
# SOURCE: .github/PRPs/templates/prp-plan.prompt-plan-template.md:1-3
# EXISTING EXTRACTED TEMPLATE — COPY THIS STRUCTURE:
# Feature: {Feature Name}

## Summary
```

Key: template files contain **raw markdown only** — no surrounding fences, no bash, no frontmatter.
The first line of the template file is the first line of content from inside the fence (not the
fence marker itself).

**FENCE_BOUNDARY_RULE:**

```text
# Line N:   ````markdown      ← fence_open — EXCLUDED from extracted content
# Line N+1: ## Code Review… ← START = fence_open + 1 (first content line)
# ...
# Line M:   last content…    ← END = fence_close - 1 (last content line)
# Line M+1: ````             ← fence_close — EXCLUDED from extracted content
#
# Extract: content lines START..END (exclusive of fence markers)
# Command: (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
```

**SKILL_EXTRACT_COMMAND (PowerShell):**

```powershell
# SOURCE: .github/skills/text-file-content-extractor-replacer/SKILL.md
# COPY THIS PATTERN for each extraction:
$src   = ".github/agents/code-reviewer.md"
$start = 106   # 1-based, inclusive — RE-VERIFY before each operation
$end   = 168   # 1-based, inclusive — RE-VERIFY before each operation
$dest  = ".github/PRPs/templates/code-reviewer.agent-report-template.md"
(Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
```

**REFERENCE_INSTRUCTION_PATTERN (for Phase 4 reference — not written in Phase 3):**

```markdown
# SOURCE: .github/prompts/prp-plan.prompt.md:247-248
# THIS IS THE TWO-LINE FORMAT USED IN PHASE 4:
> **Output Template**: See `.github/PRPs/templates/code-reviewer.agent-report-template.md`
> Load this file and use its structure exactly when generating output.
```

**NAMING_CONVENTION:**

```text
# Prompt templates (established):  <name>.prompt-<function>-template.md
# Agent templates (new, this phase): <name>.agent-<function>-template.md
#
# Function suffix examples:
#   report     → main analysis output (most agents)
#   pass       → clean/no-issues variant (silent-failure-hunter)
#   adequate   → sufficient-coverage variant (pr-test-analyzer)
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `.github/PRPs/templates/code-reviewer.agent-report-template.md` | CREATE | Main code review report template extracted from `code-reviewer.md` |
| `.github/PRPs/templates/code-simplifier.agent-report-template.md` | CREATE | Code simplification report template extracted from `code-simplifier.md` |
| `.github/PRPs/templates/codebase-analyst.agent-report-template.md` | CREATE | Codebase analysis report template extracted from `codebase-analyst.md` |
| `.github/PRPs/templates/codebase-explorer.agent-report-template.md` | CREATE | Exploration report template extracted from `codebase-explorer.md` |
| `.github/PRPs/templates/comment-analyzer.agent-report-template.md` | CREATE | Comment analysis report template extracted from `comment-analyzer.md` |
| `.github/PRPs/templates/gpui-researcher.agent-report-template.md` | CREATE | GPUI research report template extracted from `gpui-researcher.md` |
| `.github/PRPs/templates/pr-test-analyzer.agent-report-template.md` | CREATE | PR test analysis report (with gaps) extracted from `pr-test-analyzer.md` |
| `.github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md` | CREATE | Adequate coverage report extracted from `pr-test-analyzer.md` |
| `.github/PRPs/templates/silent-failure-hunter.agent-report-template.md` | CREATE | Silent failure analysis report extracted from `silent-failure-hunter.md` |
| `.github/PRPs/templates/silent-failure-hunter.agent-pass-template.md` | CREATE | No silent failures found report extracted from `silent-failure-hunter.md` |
| `.github/PRPs/templates/type-design-analyzer.agent-report-template.md` | CREATE | Type design analysis report extracted from `type-design-analyzer.md` |
| `.github/PRPs/templates/web-researcher.agent-report-template.md` | CREATE | Web research findings report extracted from `web-researcher.md` |

**Source files read but NOT modified in Phase 3:**
- `.github/agents/code-reviewer.md`
- `.github/agents/code-simplifier.md`
- `.github/agents/codebase-analyst.md`
- `.github/agents/codebase-explorer.md`
- `.github/agents/comment-analyzer.md`
- `.github/agents/gpui-researcher.md`
- `.github/agents/pr-test-analyzer.md`
- `.github/agents/silent-failure-hunter.md`
- `.github/agents/type-design-analyzer.md`
- `.github/agents/web-researcher.md`

---

## NOT Building (Scope Limits)

- **Phase 4 (Update Agent Files)**: Replacing inline blocks with reference instructions — separate phase, depends on Phase 3
- **Secondary "no-issues" templates for `code-reviewer`, `code-simplifier`, `comment-analyzer`**: These agents have `## If No Issues Found` / `## If No Simplifications Needed` sections with additional templates; they are **not listed** in the PRD template inventory of 12 files — do NOT extract them in this phase
- **`docs-impact-agent.md`**: Has multiple ```` ```markdown ```` fences but is not in the PRD extraction inventory — do NOT touch it
- **Content normalization**: Template files will contain content exactly as it appears in source (verbatim, including any indentation or blank lines)
- **Markdown linting**: Explicitly excluded per PRD's "What We're NOT Building"
- **Deduplication**: Each template gets its own file even if patterns overlap with other templates

---

## Step-by-Step Tasks

Execute in any order (all tasks are independent). Verify line numbers immediately before each write.

---

### Task 0: Verify prerequisites

- **ACTION**: Confirm `.github/PRPs/templates/` directory exists and none of the 12 target files pre-exist
- **RUN**:
  ```powershell
  (Get-ChildItem .github\PRPs\templates\ -Filter "*.md").Count
  # Expect: 25 (or adjusted if more were added since last check)
  ```
- **ALSO CHECK**:
  ```powershell
  @(
    "code-reviewer.agent-report-template.md",
    "code-simplifier.agent-report-template.md",
    "codebase-analyst.agent-report-template.md",
    "codebase-explorer.agent-report-template.md",
    "comment-analyzer.agent-report-template.md",
    "gpui-researcher.agent-report-template.md",
    "pr-test-analyzer.agent-report-template.md",
    "pr-test-analyzer.agent-adequate-template.md",
    "silent-failure-hunter.agent-report-template.md",
    "silent-failure-hunter.agent-pass-template.md",
    "type-design-analyzer.agent-report-template.md",
    "web-researcher.agent-report-template.md"
  ) | ForEach-Object { [PSCustomObject]@{ File = $_; Exists = (Test-Path ".github\PRPs\templates\$_") } }
  ```
- **EXPECT**: All `Exists = False` — if any are `True`, confirm with user before overwriting (skill safety rule)
- **VALIDATE**: Directory exists; no target files pre-exist

---

### Task 1: Extract `code-reviewer.agent-report-template.md`

**Source**: `.github/agents/code-reviewer.md`  
**Section**: `## Output Format`  
**Fence type**: Primary `` ````markdown `` (4-tick open) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L106–L168 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/code-reviewer.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/code-reviewer.md` around lines 100–175
  - Find the `` ````markdown `` line in `## Output Format` — note its line number (`fence_open`, ≈ L105)
  - Set `START` = `fence_open + 1` (first content line)
  - Find the matching closing ```` ```` ```` line — note as `fence_close` (≈ L169)
  - Set `END` = `fence_close - 1`
  - Confirm: line `START - 1` is `` ````markdown ``; line `END + 1` is ```` ```` ````

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/code-reviewer.md"
  $start = {verified START}   # RE-VERIFY — do not use plan approximation
  $end   = {verified END}     # RE-VERIFY
  $dest  = ".github/PRPs/templates/code-reviewer.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The primary template contains inner code fences (e.g., ` ```text `, ` ```typescript ` — these are NOT fence boundaries and must be copied verbatim. Only the outer 4-tick `` ````markdown `` ... ```` ```` ```` delimiters bound the block.
- **GOTCHA**: Do NOT extract the `## If No Issues Found` section (L171–L189) — that secondary template is out of scope for Phase 3.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\code-reviewer.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\code-reviewer.agent-report-template.md")[0]
  # Expect: first line of template content (NOT "````markdown")
  (Get-Content ".github\PRPs\templates\code-reviewer.agent-report-template.md")[-1]
  # Expect: last line of template content (NOT "````")
  ```

---

### Task 2: Extract `code-simplifier.agent-report-template.md`

**Source**: `.github/agents/code-simplifier.md`  
**Section**: `## Output Format`  
**Fence type**: Primary `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L96–L168 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/code-simplifier.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/code-simplifier.md` around lines 90–175
  - Find `` ````markdown `` fence at `## Output Format` (≈ L95); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L169); note `fence_close`
  - Set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/code-simplifier.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/code-simplifier.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: Do NOT extract the `## If No Simplifications Needed` section (≈ L173–L188) — out of scope.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\code-simplifier.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\code-simplifier.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 3: Extract `codebase-analyst.agent-report-template.md`

**Source**: `.github/agents/codebase-analyst.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L74–L119 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/codebase-analyst.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/codebase-analyst.md` around lines 69–125
  - Find `` ````markdown `` fence (≈ L73); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L120); set `END` = `fence_close - 1`
  - This agent has NO secondary template section.

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/codebase-analyst.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/codebase-analyst.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\codebase-analyst.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\codebase-analyst.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 4: Extract `codebase-explorer.agent-report-template.md`

**Source**: `.github/agents/codebase-explorer.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L90–L185 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/codebase-explorer.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/codebase-explorer.md` around lines 85–190
  - Find `` ````markdown `` fence at `## Output Format` (≈ L89); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L186); set `END` = `fence_close - 1`
  - This agent has NO secondary template section.

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/codebase-explorer.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/codebase-explorer.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The PRD README had a typo listing this as `codebase-analyst.md` twice. This is the **explorer** file, not analyst. The target file name is `codebase-explorer.agent-report-template.md`, not `codebase-analyst`.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\codebase-explorer.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\codebase-explorer.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  (Get-Content ".github\PRPs\templates\codebase-explorer.agent-report-template.md").Count
  # Expect: approximately 96 lines
  ```

---

### Task 5: Extract `comment-analyzer.agent-report-template.md`

**Source**: `.github/agents/comment-analyzer.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L96–L233 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/comment-analyzer.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/comment-analyzer.md` around lines 90–260
  - Find `` ````markdown `` fence (≈ L95); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L234); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/comment-analyzer.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/comment-analyzer.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: Do NOT extract the `## If No Issues Found` secondary section (≈ L238–L256) — out of scope for Phase 3 per PRD inventory.
- **GOTCHA**: This is the largest primary template (≈ 138 lines). The inner content contains multi-level code fences — copy verbatim, do not truncate.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\comment-analyzer.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\comment-analyzer.agent-report-template.md").Count
  # Expect: approximately 138 lines
  (Get-Content ".github\PRPs\templates\comment-analyzer.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 6: Extract `gpui-researcher.agent-report-template.md`

**Source**: `.github/agents/gpui-researcher.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L109–L192 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/gpui-researcher.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/gpui-researcher.md` around lines 105–215
  - Find `` ````markdown `` fence at `## Output Format` (≈ L108); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L193); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/gpui-researcher.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/gpui-researcher.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The `## If Validation Fails` secondary section (≈ L199–L213) uses 4-tick fences (unlike most secondaries which use 3-tick). It is NOT in the PRD inventory — do NOT extract it in Phase 3.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\gpui-researcher.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\gpui-researcher.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 7: Extract `pr-test-analyzer.agent-report-template.md`

**Source**: `.github/agents/pr-test-analyzer.md`  
**Section**: `## Output Format` (primary — "with gaps" report)  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L105–L221 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/pr-test-analyzer.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/pr-test-analyzer.md` around lines 100–230
  - Find `` ````markdown `` fence at `## Output Format` (≈ L104); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L222); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/pr-test-analyzer.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/pr-test-analyzer.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: This file has TWO templates. Task 8 extracts the second (`adequate` variant). Source file is NOT modified in Phase 3, so Task 8 uses the original line numbers — still re-verify.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\pr-test-analyzer.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\pr-test-analyzer.agent-report-template.md").Count
  # Expect: approximately 117 lines
  (Get-Content ".github\PRPs\templates\pr-test-analyzer.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 8: Extract `pr-test-analyzer.agent-adequate-template.md`

**Source**: `.github/agents/pr-test-analyzer.md`  
**Section**: `## If Coverage Is Adequate`  
**Fence type**: ```` ```markdown ```` (3-tick open) / ```` ``` ```` (3-tick close)  
**Approximate content range**: L227–L249 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md`

- **STEP 1 — READ**: Read `.github/agents/pr-test-analyzer.md` around lines 222–255
  - Find ```` ```markdown ```` (3-tick!) fence at `## If Coverage Is Adequate` (≈ L226); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ``` ```` (3-tick) (≈ L250); set `END` = `fence_close - 1`
  - Note: fence is 3-tick here, unlike the primary template's 4-tick. Do not confuse with inner ``` fences if any exist inside.

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/pr-test-analyzer.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: Source file is NOT modified between Task 7 and Task 8 (Phase 3 extract-only), so line numbers are stable. Still re-verify.
- **GOTCHA**: The 3-tick fence open (```` ```markdown ````) and close (```` ``` ````) must NOT appear in the template file.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\pr-test-analyzer.agent-adequate-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\pr-test-analyzer.agent-adequate-template.md").Count
  # Expect: approximately 23 lines
  (Get-Content ".github\PRPs\templates\pr-test-analyzer.agent-adequate-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 9: Extract `silent-failure-hunter.agent-report-template.md`

**Source**: `.github/agents/silent-failure-hunter.md`  
**Section**: `## Output Format` (primary — with issues)  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L123–L254 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/silent-failure-hunter.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/silent-failure-hunter.md` around lines 115–260
  - Find `` ````markdown `` fence at `## Output Format` (≈ L122); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L255); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/silent-failure-hunter.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/silent-failure-hunter.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: This is the largest primary template (≈ 132 lines). Contains inner code fences and sub-structures — copy verbatim.
- **GOTCHA**: Task 10 extracts the secondary template from the same source file. Source is not modified in Phase 3, so line numbers are stable.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\silent-failure-hunter.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\silent-failure-hunter.agent-report-template.md").Count
  # Expect: approximately 132 lines
  (Get-Content ".github\PRPs\templates\silent-failure-hunter.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 10: Extract `silent-failure-hunter.agent-pass-template.md`

**Source**: `.github/agents/silent-failure-hunter.md`  
**Section**: `## If No Issues Found`  
**Fence type**: ```` ```markdown ```` (3-tick open) / ```` ``` ```` (3-tick close)  
**Approximate content range**: L260–L281 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/silent-failure-hunter.agent-pass-template.md`

- **STEP 1 — READ**: Read `.github/agents/silent-failure-hunter.md` around lines 255–285
  - Find ```` ```markdown ```` (3-tick) fence at `## If No Issues Found` (≈ L259); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ``` ```` (3-tick) (≈ L282); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/silent-failure-hunter.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/silent-failure-hunter.agent-pass-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The secondary section use 3-tick fence (not 4-tick like the primary). Verify boundary lines are ```` ```markdown ```` and ```` ``` ````, not ```` ````markdown ```` and ```` ```` ````.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\silent-failure-hunter.agent-pass-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\silent-failure-hunter.agent-pass-template.md").Count
  # Expect: approximately 22 lines
  (Get-Content ".github\PRPs\templates\silent-failure-hunter.agent-pass-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 11: Extract `type-design-analyzer.agent-report-template.md`

**Source**: `.github/agents/type-design-analyzer.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L154–L262 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/type-design-analyzer.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/type-design-analyzer.md` around lines 148–265
  - Find `` ````markdown `` fence at `## Output Format` (≈ L153); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L263); set `END` = `fence_close - 1`

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/type-design-analyzer.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/type-design-analyzer.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The PRD Evidence states "3 agents (`pr-test-analyzer`, `silent-failure-hunter`, `type-design-analyzer`) contain two distinct templates each." However, the PRD Template Inventory only lists ONE file for `type-design-analyzer` (`type-design-analyzer.agent-report-template.md`). The `## For Multiple Types` secondary section (≈ L269–L285) is **not** in the 12-file inventory — do NOT extract it in this phase. If this is discovered to be a PRD omission, pause and confirm with the user before adding a 13th file.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\type-design-analyzer.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\type-design-analyzer.agent-report-template.md").Count
  # Expect: approximately 109 lines
  (Get-Content ".github\PRPs\templates\type-design-analyzer.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 12: Extract `web-researcher.agent-report-template.md`

**Source**: `.github/agents/web-researcher.md`  
**Section**: `## Output Format`  
**Fence type**: `` ````markdown `` (4-tick) / ```` ```` ```` (4-tick close)  
**Approximate content range**: L87–L128 (RE-VERIFY before writing)  
**Target**: `.github/PRPs/templates/web-researcher.agent-report-template.md`

- **STEP 1 — READ**: Read `.github/agents/web-researcher.md` around lines 80–135
  - Find `` ````markdown `` fence at `## Output Format` (≈ L86); note `fence_open`
  - Set `START` = `fence_open + 1`
  - Find closing ```` ```` ```` (≈ L129); set `END` = `fence_close - 1`
  - This agent has NO secondary template section.

- **STEP 2 — EXTRACT**:
  ```powershell
  $src   = ".github/agents/web-researcher.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/web-researcher.agent-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\web-researcher.agent-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\web-researcher.agent-report-template.md").Count
  # Expect: approximately 42 lines
  (Get-Content ".github\PRPs\templates\web-researcher.agent-report-template.md")[0]
  # Expect: first content line (not a fence marker)
  ```

---

### Task 13: Final Validation

- **ACTION**: Confirm all 12 template files exist, none contains a fence marker as first or last line, and no source agent file was modified

- **RUN — Count new templates**:
  ```powershell
  (Get-ChildItem .github\PRPs\templates\ -Filter "*agent*template*.md").Count
  # Expect: 12
  ```

- **RUN — Verify no fence markers in output files** (first and last lines must NOT be fence markers):
  ```powershell
  Get-ChildItem ".github\PRPs\templates\" -Filter "*agent*template*.md" | ForEach-Object {
    $lines = Get-Content $_.FullName
    [PSCustomObject]@{
      File      = $_.Name
      FirstLine = $lines[0]
      LastLine  = $lines[-1]
      LineCount = $lines.Count
    }
  }
  # All FirstLine and LastLine values must NOT equal "````markdown", "````", "```markdown", or "```"
  ```

- **RUN — Verify source agent files are unmodified** (check git status):
  ```powershell
  git status .github/agents/
  # Expect: nothing to commit (no modified files listed under .github/agents/)
  ```

- **RUN — Verify total template count increased by 12**:
  ```powershell
  (Get-ChildItem .github\PRPs\templates\ -Filter "*.md").Count
  # Expect: 37 (was 25 before Phase 3)
  ```

---

## Discovered Patterns Reference Table

| Agent File | Total Lines | Primary Fence Open | Primary Content | Secondary Section | Secondary Fence Type | Secondary Content |
|-----------|-------------|--------------------|-----------------|-------------------|-----------------------|-------------------|
| `code-reviewer.md` | 208 | ≈L105 (4-tick) | **≈L106–L168** | `## If No Issues Found` | 3-tick ≈L173 | NOT IN SCOPE |
| `code-simplifier.md` | 212 | ≈L95 (4-tick) | **≈L96–L168** | `## If No Simplifications Needed` | 3-tick ≈L173 | NOT IN SCOPE |
| `codebase-analyst.md` | 147 | ≈L73 (4-tick) | **≈L74–L119** | — | — | — |
| `codebase-explorer.md` | 226 | ≈L89 (4-tick) | **≈L90–L185** | — | — | — |
| `comment-analyzer.md` | 275 | ≈L95 (4-tick) | **≈L96–L233** | `## If No Issues Found` | 3-tick ≈L238 | NOT IN SCOPE |
| `gpui-researcher.md` | 231 | ≈L108 (4-tick) | **≈L109–L192** | `## If Validation Fails` | 4-tick ≈L199 | NOT IN SCOPE |
| `pr-test-analyzer.md` | 269 | ≈L104 (4-tick) | **≈L105–L221** | `## If Coverage Is Adequate` | 3-tick ≈L226 | **≈L227–L249** |
| `silent-failure-hunter.md` | 311 | ≈L122 (4-tick) | **≈L123–L254** | `## If No Issues Found` | 3-tick ≈L259 | **≈L260–L281** |
| `type-design-analyzer.md` | 305 | ≈L153 (4-tick) | **≈L154–L262** | `## For Multiple Types` | 3-tick ≈L269 | NOT IN SCOPE |
| `web-researcher.md` | 163 | ≈L86 (4-tick) | **≈L87–L128** | — | — | — |

> **ALL line numbers in this table are APPROXIMATE.** Always re-read and re-verify before writing.
