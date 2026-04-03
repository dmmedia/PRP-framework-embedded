# Feature: Extract Prompt Output Templates — Phase 1

## Summary

Extract 6 inline output template blocks from 5 prompt files in `.github/prompts/` into standalone
markdown files under `.github/PRPs/templates/`. This is Phase 1 of 2 for prompt-side extraction
(Phase 2 will replace the inline blocks with reference instructions). All operations use the
`text-file-content-extractor-replacer` skill in **extract mode only** — source files are not
modified in this phase.

## User Story

As a framework maintainer editing an output format  
I want to find and edit the output template independently of the surrounding prompt instructions  
So that I can update one concern without risking accidental changes to instruction logic

## Problem Statement

5 prompt files in `.github/prompts/` still contain at least one inline output template block
(a fenced markdown block or a bash heredoc body) that must be read in context of 200–400 lines of
instruction logic before it can be edited. After this phase, 6 standalone template files exist and
are ready for Phase 2 source-file updates.

## Solution Statement

Use the `text-file-content-extractor-replacer` skill to copy the template content from each source
file's inline block into a new file in `.github/PRPs/templates/`. All 6 extractions are
independent; they can be done in any order or in parallel sub-tasks.

## Metadata

| Field | Value |
| ---------------- | -------------------------------------------- |
| Type | REFACTOR |
| Complexity | LOW |
| Systems Affected | `.github/prompts/`, `.github/PRPs/templates/` |
| Dependencies | None — pure markdown file I/O |
| Estimated Tasks | 6 extraction tasks + 1 validation task |

---

## UX Design

### Before State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────┐   scroll 200+ lines   ┌──────────────────────────┐ ║
║  │  prp-implement       │ ──────────────────────►│  inline ```markdown      │ ║
║  │  .prompt.md          │                         │  ## Implementation       │ ║
║  │  (400+ lines)        │                         │  Complete ... (50 lines) │ ║
║  └──────────────────────┘                         └──────────────────────────┘ ║
║                                                                               ║
║   USER_FLOW: open file → scroll past instructions → find template → edit      ║
║   PAIN_POINT: template is buried inside instruction logic; can't edit one      ║
║               concern without seeing and risking the other                     ║
║   DATA_FLOW: template content lives inside .prompt.md; no standalone file     ║
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
║  │  prp-implement       │   (Phase 2: reference)  │  prp-implement.prompt-   │ ║
║  │  .prompt.md          │ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─►│  summary-template.md    │ ║
║  │  (unchanged in Ph 1) │                         │  (standalone, 50 lines)  │ ║
║  └──────────────────────┘                         └──────────────────────────┘ ║
║                                   │                                           ║
║                                   ▼                                           ║
║                    ┌──────────────────────────────────┐                       ║
║                    │  .github/PRPs/templates/          │                       ║
║                    │  6 new standalone template files  │  ◄── created here    ║
║                    └──────────────────────────────────┘                       ║
║                                                                               ║
║   USER_FLOW: open template file directly → edit only the format               ║
║   VALUE_ADD: instruction logic and template are separate files;               ║
║              editing one does not require touching the other                  ║
║   DATA_FLOW: template content in .github/PRPs/templates/*.md;                 ║
║              source .prompt.md files unchanged until Phase 2                  ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `.github/prompts/prp-implement.prompt.md` | Template inline at ~line 350 | Template inline (Phase 2 removes it) | Unchanged in Phase 1 |
| `.github/PRPs/templates/` | 19 existing templates | 25 templates (6 added) | Maintainer can open template file directly |
| `prp-implement.prompt-summary-template.md` | Does not exist | Exists with `## Implementation Complete` block | Editable standalone |
| `prp-issue-fix.prompt-pr-template.md` | Does not exist | Exists with PR body markdown | Editable standalone |
| `prp-issue-fix.prompt-review-template.md` | Does not exist | Exists with review comment markdown | Editable standalone |
| `prp-issue-investigate.prompt-comment-template.md` | Does not exist | Exists with GH issue comment markdown | Editable standalone |
| `prp-plan.prompt-summary-template.md` | Does not exist | Exists with `## Plan Created` block | Editable standalone |
| `prp-ralph.prompt-report-template.md` | Does not exist | Exists with `# Implementation Report` block | Editable standalone |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/skills/text-file-content-extractor-replacer/SKILL.md` | all | Skill operation modes, PowerShell commands, safety rules |
| P0 | `.github/prompts/prp-implement.prompt.md` | 345–410 | Confirm exact line range for Task 1 extraction |
| P0 | `.github/prompts/prp-issue-fix.prompt.md` | 375–440 | Confirm exact line range for Task 2 (§7.2 heredoc) |
| P0 | `.github/prompts/prp-issue-fix.prompt.md` | 470–515 | Confirm exact line range for Task 3 (§8.2 heredoc) |
| P0 | `.github/prompts/prp-issue-investigate.prompt.md` | 290–365 | Confirm exact line range for Task 4 (Phase 6 heredoc) |
| P0 | `.github/prompts/prp-plan.prompt.md` | 345–402 | Confirm exact line range for Task 5 (REPORT_TO_USER block) |
| P0 | `.github/prompts/prp-ralph.prompt.md` | 248–290 | Confirm exact line range for Task 6 (§4.2 block) |
| P1 | `.github/PRPs/templates/prp-issue-fix.prompt-report-template.md` | all | Example of what an extracted template looks like |
| P1 | `.github/PRPs/templates/prp-ralph.prompt-progress-template.md` | all | Example of a ralph prompt template structure |
| P2 | `.claude/PRPs/prds/extract-remaining-templates.prd.md` | 101–175 | Template inventory table and naming spec |

**External Documentation:** None required — pure markdown file I/O.

---

## Patterns to Mirror

**TEMPLATE_FILE_STRUCTURE:**

```markdown
# SOURCE: .github/PRPs/templates/prp-issue-fix.prompt-report-template.md:1-5
# EXISTING EXTRACTED TEMPLATE — COPY THIS STRUCTURE:
## Implementation Complete

**Issue**: #{number} - {title}
**Branch**: `{branch-name}`
**PR**: #{pr-number} - {pr-url}
```

Key: template files contain **raw markdown only** — no surrounding fences, no bash, no frontmatter.

**REFERENCE_INSTRUCTION_PATTERN:**

```markdown
# SOURCE: .github/prompts/prp-plan.prompt.md:247-248
# THIS IS THE TWO-LINE FORMAT USED IN PHASE 2 (reference only — not written in Phase 1):
> **Output Template**: See `.github/PRPs/templates/prp-plan.prompt-design-template.md`
> Load this file and use its structure exactly when generating output.
```

**SKILL_EXTRACT_COMMAND (PowerShell):**

```powershell
# SOURCE: .github/skills/text-file-content-extractor-replacer/SKILL.md
# COPY THIS PATTERN for each extraction:
$src   = ".github/prompts/prp-implement.prompt.md"
$start = 350   # 1-based, inclusive — RE-VERIFY before each operation
$end   = 402   # 1-based, inclusive — RE-VERIFY before each operation
$dest  = ".github/PRPs/templates/prp-implement.prompt-summary-template.md"
(Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
```

**HEREDOC_BOUNDARY_RULE:**

```text
# SOURCE: .claude/PRPs/prds/extract-remaining-templates.prd.md (Technical Risks section)
# Heredoc extraction boundary: exclude the EOF marker line and the )" line
# Extract ONLY the markdown content between the heredoc opener and EOF:
#   Line N:   --body "$(cat <<'EOF'    ← EXCLUDE this line
#   Line N+1: ## Summary              ← FIRST line to extract
#   ...
#   Line M:   _Automated..._          ← LAST line to extract
#   Line M+1: EOF                     ← EXCLUDE this line
#   Line M+2: )"                      ← EXCLUDE this line
```

---

## Files to Change

| File | Action | Justification |
|--------------------------------------------|--------|------------------------------------------------|
| `.github/PRPs/templates/prp-implement.prompt-summary-template.md` | CREATE | Template for Phase 6 `## Implementation Complete` block |
| `.github/PRPs/templates/prp-issue-fix.prompt-pr-template.md` | CREATE | Template for §7.2 PR body heredoc body |
| `.github/PRPs/templates/prp-issue-fix.prompt-review-template.md` | CREATE | Template for §8.2 self-review comment heredoc body |
| `.github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md` | CREATE | Template for Phase 6 GH issue comment heredoc body |
| `.github/PRPs/templates/prp-plan.prompt-summary-template.md` | CREATE | Template for REPORT_TO_USER `## Plan Created` block |
| `.github/PRPs/templates/prp-ralph.prompt-report-template.md` | CREATE | Template for §4.2 `# Implementation Report` block |

**Source files read but NOT modified in Phase 1:**
- `.github/prompts/prp-implement.prompt.md`
- `.github/prompts/prp-issue-fix.prompt.md`
- `.github/prompts/prp-issue-investigate.prompt.md`
- `.github/prompts/prp-plan.prompt.md`
- `.github/prompts/prp-ralph.prompt.md`

---

## NOT Building (Scope Limits)

- **Phase 2 (Update Prompt Files)**: Replacing inline blocks with reference instructions — separate phase, depends on Phase 1
- **Phase 3 (Extract Agent Templates)**: Agent file extractions — separate parallel phase
- **Phase 4 (Update Agent Files)**: Agent reference insertions — separate phase
- **Content normalization**: Template files will contain content exactly as it appears in source (verbatim, including any indentation)
- **Markdown linting**: Explicitly excluded per PRD's "What We're NOT Building"
- **Deduplication**: Each template gets its own file even if patterns overlap with other templates

---

## Step-by-Step Tasks

Execute in any order (all tasks are independent). Verify line numbers immediately before each write.

---

### Task 0: Verify prerequisites

- **ACTION**: Confirm `.github/PRPs/templates/` directory exists and count current templates
- **RUN**: `(Get-ChildItem .github\PRPs\templates\ -Filter "*.md").Count`
- **EXPECT**: 19 (existing files from first extraction — README.md not counted if excluded, adjust count)
- **ALSO CHECK**: None of the 6 target template files already exist — run:
  ```powershell
  @(
    "prp-implement.prompt-summary-template.md",
    "prp-issue-fix.prompt-pr-template.md",
    "prp-issue-fix.prompt-review-template.md",
    "prp-issue-investigate.prompt-comment-template.md",
    "prp-plan.prompt-summary-template.md",
    "prp-ralph.prompt-report-template.md"
  ) | ForEach-Object { Test-Path ".github\PRPs\templates\$_" }
  ```
- **EXPECT**: All `False` — if any are `True`, confirm with user before overwriting (skill safety rule)
- **VALIDATE**: Directory exists; no target files pre-exist

---

### Task 1: Extract `prp-implement.prompt-summary-template.md`

**Source**: `.github/prompts/prp-implement.prompt.md`  
**Section**: Phase 6 — OUTPUT: Report to User  
**Content**: The `## Implementation Complete` block (inside a ```` ```markdown ```` fence)  
**Target**: `.github/PRPs/templates/prp-implement.prompt-summary-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-implement.prompt.md` around lines 345–410
  - Find the ` ```markdown ` line in Phase 6 OUTPUT section — note its line number (`fence_open`)
  - Find the content-start line (`## Implementation Complete`) — note as `START` = `fence_open + 1`
  - Find the matching closing ` ``` ` line — note as `fence_close`
  - Set `END` = `fence_close - 1`
  - Approximate range: START ≈ 350, END ≈ 402 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use `text-file-content-extractor-replacer` skill in `extract` mode:
  ```powershell
  $src   = ".github/prompts/prp-implement.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-implement.prompt-summary-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The fence line (` ```markdown `) and closing fence (` ``` `) must NOT appear in the template file — extract only content between them (exclusive)
- **GOTCHA**: There is already a `prp-implement.prompt-report-template.md` (86 lines) in the templates dir — do NOT overwrite it; this is a new file with a **different** name (`summary` not `report`)
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-implement.prompt-summary-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-implement.prompt-summary-template.md")[0]
  # Expect: "## Implementation Complete"
  ```

---

### Task 2: Extract `prp-issue-fix.prompt-pr-template.md`

**Source**: `.github/prompts/prp-issue-fix.prompt.md`  
**Section**: §7.2 Create PR — heredoc body  
**Content**: Markdown inside `$(cat <<'EOF' ... EOF)` (the PR body)  
**Target**: `.github/PRPs/templates/prp-issue-fix.prompt-pr-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-issue-fix.prompt.md` around lines 375–440
  - Find the heredoc opener line: `--body "$(cat <<'EOF'` — note its line number (`heredoc_open`)
  - Set `START` = `heredoc_open + 1` (first content line: `## Summary`)
  - Find the `EOF` line immediately after the heredoc body — note as `eof_line`
  - Set `END` = `eof_line - 1` (last content line before `EOF`)
  - Approximate range: START ≈ 383, END ≈ 433 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use skill in `extract` mode:
  ```powershell
  $src   = ".github/prompts/prp-issue-fix.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-issue-fix.prompt-pr-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: The heredoc body contains a nested ` ```bash ` fence (inside the `## Validation` section). This is fine — it will be copied verbatim. Do NOT try to strip it.
- **GOTCHA**: The `EOF` line and the `)"` line are bash plumbing — they must NOT appear in the template file
- **GOTCHA**: There is already a `prp-issue-fix.prompt-report-template.md` — do NOT overwrite; this is a new `pr` (not `report`) suffix
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-issue-fix.prompt-pr-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-issue-fix.prompt-pr-template.md")[0]
  # Expect: "## Summary"
  (Get-Content ".github\PRPs\templates\prp-issue-fix.prompt-pr-template.md")[-1]
  # Expect: "_Automated implementation from investigation artifact_"
  ```

---

### Task 3: Extract `prp-issue-fix.prompt-review-template.md`

**Source**: `.github/prompts/prp-issue-fix.prompt.md`  
**Section**: §8.2 Post Review to PR — heredoc body  
**Content**: Markdown inside `$(cat <<'EOF' ... EOF)` (the review comment)  
**Target**: `.github/PRPs/templates/prp-issue-fix.prompt-review-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-issue-fix.prompt.md` around lines 470–515
  - Find the heredoc opener line containing `--body "$(cat <<'EOF'` in section 8.2 — note its line number
  - Set `START` = that line + 1 (first content line: `## 🔍 Automated Code Review`)
  - Find the `EOF` line — set `END` = `eof_line - 1`
  - Approximate range: START ≈ 478, END ≈ 505 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use skill in `extract` mode:
  ```powershell
  $src   = ".github/prompts/prp-issue-fix.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-issue-fix.prompt-review-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: Section 8.2 is in the same source file as Task 2. Read the file fresh to get current line numbers (the file was not modified in Task 2, so line numbers are unchanged — but verify anyway)
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-issue-fix.prompt-review-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-issue-fix.prompt-review-template.md")[0]
  # Expect: "## 🔍 Automated Code Review"
  (Get-Content ".github\PRPs\templates\prp-issue-fix.prompt-review-template.md")[-1]
  # Expect: "*Self-reviewed by Claude • Ready for human review*"
  ```

---

### Task 4: Extract `prp-issue-investigate.prompt-comment-template.md`

**Source**: `.github/prompts/prp-issue-investigate.prompt.md`  
**Section**: Phase 6 POST — GitHub Comment — heredoc body  
**Content**: Markdown inside `$(cat <<'EOF' ... EOF)` (the GitHub issue comment)  
**Target**: `.github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-issue-investigate.prompt.md` around lines 290–365
  - Find `## Phase 6: POST - GitHub Comment` heading
  - Find the heredoc opener line — note its line number
  - Set `START` = that line + 1 (first content line: `## 🔍 Investigation: {Title}`)
  - Find the `EOF` line — set `END` = `eof_line - 1`
  - Approximate range: START ≈ 301, END ≈ 358 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use skill in `extract` mode:
  ```powershell
  $src   = ".github/prompts/prp-issue-investigate.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: There is already a `prp-issue-investigate.prompt-artifact-template.md` — do NOT overwrite; this creates a new `comment` (not `artifact`) file
- **GOTCHA**: The heredoc body contains a nested ` ```bash ` fence (inside `### Validation`). Extract verbatim.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-issue-investigate.prompt-comment-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-issue-investigate.prompt-comment-template.md")[0]
  # Expect: "## 🔍 Investigation: {Title}"
  (Get-Content ".github\PRPs\templates\prp-issue-investigate.prompt-comment-template.md")[-1]
  # Expect: "_Investigated by Claude • {timestamp}_"
  ```

---

### Task 5: Extract `prp-plan.prompt-summary-template.md`

**Source**: `.github/prompts/prp-plan.prompt.md`  
**Section**: `<output>` block — REPORT_TO_USER section  
**Content**: The `## Plan Created` block (inside a ```` ```markdown ```` fence)  
**Target**: `.github/PRPs/templates/prp-plan.prompt-summary-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-plan.prompt.md` around lines 345–402
  - Find the `**OUTPUT_FILE**` heading and the `**REPORT_TO_USER**` label in the `<output>` block
  - Find the ` ```markdown ` fence line — note as `fence_open`
  - Set `START` = `fence_open + 1` (first content line: `## Plan Created`)
  - Find the matching ` ``` ` closing fence — note as `fence_close`
  - Set `END` = `fence_close - 1`
  - Approximate range: START ≈ 351, END ≈ 397 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use skill in `extract` mode:
  ```powershell
  $src   = ".github/prompts/prp-plan.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-plan.prompt-summary-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: `prp-plan.prompt.md` already has two extracted templates referenced (design-template, plan-template). The REPORT_TO_USER block (starting `## Plan Created`) is the third template living inline — verify by running: `Select-String -Path .github\prompts\prp-plan.prompt.md -Pattern "## Plan Created"` which should return exactly one line in the `<output>` section.
- **GOTCHA**: There is no existing `prp-plan.prompt-summary-template.md` — verify with `Test-Path` before writing
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-plan.prompt-summary-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-plan.prompt-summary-template.md")[0]
  # Expect: "## Plan Created"
  (Get-Content ".github\PRPs\templates\prp-plan.prompt-summary-template.md")[-1]
  # Expect: "**Next Step**: To execute, run: `/prp-implement .claude/PRPs/plans/{feature-name}.plan.md`"
  ```

---

### Task 6: Extract `prp-ralph.prompt-report-template.md`

**Source**: `.github/prompts/prp-ralph.prompt.md`  
**Section**: §4.2 If ALL Pass - Complete the Loop, item 1 (the `# Implementation Report` file block)  
**Content**: The `# Implementation Report` block (inside a ```` ```markdown ```` fence, indented 3 spaces)  
**Target**: `.github/PRPs/templates/prp-ralph.prompt-report-template.md`

- **STEP 1 — READ**: Read `.github/prompts/prp-ralph.prompt.md` around lines 248–290
  - Find `### 4.2` heading, then find the first ```` ```markdown ```` fence inside it — note as `fence_open`
  - Set `START` = `fence_open + 1` (first content line: `   # Implementation Report` — with 3 leading spaces)
  - Find the matching closing ` ``` ` (also indented 3 spaces: `   ``` `) — note as `fence_close`
  - Set `END` = `fence_close - 1`
  - Approximate range: START ≈ 255, END ≈ 282 — **re-verify before writing**

- **STEP 2 — EXTRACT**: Use skill in `extract` mode (verbatim — preserves 3-space indent):
  ```powershell
  $src   = ".github/prompts/prp-ralph.prompt.md"
  $start = {verified START}
  $end   = {verified END}
  $dest  = ".github/PRPs/templates/prp-ralph.prompt-report-template.md"
  (Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
  ```

- **GOTCHA**: Content lines are indented 3 spaces (source is inside a numbered list). Per PRD "verbatim extraction, no normalization" rule, the 3-space indent is preserved as-is. The template file will start with `   # Implementation Report` (3 leading spaces).
- **GOTCHA**: In CommonMark, up to 3 spaces before a `#` still renders as a heading — the 3-space indent is harmless markdown. Do NOT strip it.
- **GOTCHA**: There are already `prp-ralph.prompt-setup-template.md` and `prp-ralph.prompt-progress-template.md` — this creates a new `report` file. Also note `prp-ralph-cancel.prompt-cancel-template.md` (for `prp-ralph-cancel.prompt.md` — different source file). No collision.
- **VALIDATE**:
  ```powershell
  Test-Path ".github\PRPs\templates\prp-ralph.prompt-report-template.md"
  # Expect: True
  (Get-Content ".github\PRPs\templates\prp-ralph.prompt-report-template.md")[0]
  # Expect: "   # Implementation Report"  (3 leading spaces)
  (Get-Content ".github\PRPs\templates\prp-ralph.prompt-report-template.md")[-1]
  # Expect: "   {Any changes made}"  (3 leading spaces)
  ```

---

### Task 7: Final Validation

- **ACTION**: Verify all 6 template files exist and source files are unchanged

- **STEP 1 — File count**:
  ```powershell
  (Get-ChildItem .github\PRPs\templates\ -Filter "*.md").Count
  # Expect: 25 (19 existing + 6 new; if README.md is present, expect 26)
  ```

- **STEP 2 — All 6 created**:
  ```powershell
  @(
    "prp-implement.prompt-summary-template.md",
    "prp-issue-fix.prompt-pr-template.md",
    "prp-issue-fix.prompt-review-template.md",
    "prp-issue-investigate.prompt-comment-template.md",
    "prp-plan.prompt-summary-template.md",
    "prp-ralph.prompt-report-template.md"
  ) | ForEach-Object {
    [PSCustomObject]@{
      File   = $_
      Exists = (Test-Path ".github\PRPs\templates\$_")
      Lines  = if (Test-Path ".github\PRPs\templates\$_") { (Get-Content ".github\PRPs\templates\$_").Count } else { 0 }
    }
  } | Format-Table
  # Expect: all Exists=True, all Lines > 0
  ```

- **STEP 3 — Source files unchanged** (verify no accidental edits):
  ```powershell
  # None of the source prompt files should reference the new template files yet
  Select-String -Path .github\prompts\prp-implement.prompt.md -Pattern "prp-implement.prompt-summary-template"
  Select-String -Path .github\prompts\prp-issue-fix.prompt.md -Pattern "prp-issue-fix.prompt-pr-template|prp-issue-fix.prompt-review-template"
  Select-String -Path .github\prompts\prp-issue-investigate.prompt.md -Pattern "prp-issue-investigate.prompt-comment-template"
  Select-String -Path .github\prompts\prp-plan.prompt.md -Pattern "prp-plan.prompt-summary-template"
  Select-String -Path .github\prompts\prp-ralph.prompt.md -Pattern "prp-ralph.prompt-report-template"
  # Expect: no matches (source files not yet updated in Phase 1)
  ```

- **STEP 4 — Existing tests still pass**:
  ```powershell
  uv run pytest tests/ -v
  # Expect: all pass (no new tests — but existing tests must not regress)
  ```

- **VALIDATE**: All 6 `True`, file count correct, source files unmodified, test suite green

---

## Testing Strategy

### Unit Tests to Write

No new test code in this phase. All validation is structural (file existence, content spot-checks).

### Edge Cases Checklist

- [ ] `.github/PRPs/templates/` directory exists before running tasks
- [ ] No target template file already exists (would require user confirmation per skill safety rule)
- [ ] Heredoc EOF marker line NOT included in extracted content (last line check)
- [ ] Fence markers NOT included in extracted content (first/last line checks)
- [ ] `prp-ralph` content has 3-space indent preserved (verbatim per PRD)
- [ ] `prp-issue-fix.prompt.md` Tasks 2 and 3 extract from different line ranges of the SAME file; the file is not modified between tasks, so line numbers remain consistent
- [ ] No collision with existing template files (`prp-implement.prompt-report-template.md` vs `prp-implement.prompt-summary-template.md`, etc.)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```powershell
# No lint or type-check applies — pure markdown. Run existing Python tests instead:
uv run pytest tests/ -v
```

**EXPECT**: Exit 0, all existing tests pass (deprecation headers, doc mapping, docs links)

### Level 2: STRUCTURAL_VALIDATION

```powershell
# Count total templates
(Get-ChildItem .github\PRPs\templates\ -Filter "*.md").Count
# Expect: 25 (or 26 if README.md counted)
```

### Level 3: CONTENT_SPOT_CHECK

```powershell
# Verify first and last lines of each template
foreach ($f in @(
  @{name="prp-implement.prompt-summary-template.md"; first="## Implementation Complete"; last="{If more phases: `"4. Continue with next phase: ...`"}"},
  @{name="prp-issue-fix.prompt-pr-template.md"; first="## Summary"; last="_Automated implementation from investigation artifact_"},
  @{name="prp-issue-fix.prompt-review-template.md"; first="## `u{1F50D}` Automated Code Review"; last="*Self-reviewed by Claude • Ready for human review*"},
  @{name="prp-issue-investigate.prompt-comment-template.md"; first="## `u{1F50D}` Investigation: {Title}"; last="_Investigated by Claude • {timestamp}_"},
  @{name="prp-plan.prompt-summary-template.md"; first="## Plan Created"; last="**Next Step**: To execute, run: `/prp-implement .claude/PRPs/plans/{feature-name}.plan.md`"},
  @{name="prp-ralph.prompt-report-template.md"; first="   # Implementation Report"; last="   {Any changes made}"}
)) {
  $lines = Get-Content ".github\PRPs\templates\$($f.name)"
  Write-Host "`n$($f.name)"
  Write-Host "  First: $($lines[0])"
  Write-Host "  Last:  $($lines[-1])"
}
```

### Level 4: SOURCE_UNCHANGED

```powershell
# Confirm source files still contain the original inline blocks
Select-String -Path .github\prompts\prp-implement.prompt.md -Pattern "## Implementation Complete"
Select-String -Path .github\prompts\prp-issue-fix.prompt.md -Pattern "cat <<'EOF'"
Select-String -Path .github\prompts\prp-plan.prompt.md -Pattern "## Plan Created"
# Expect: each returns 1 match (still inline in source)
```

---

## Acceptance Criteria

- [ ] Exactly 6 new template files created in `.github/PRPs/templates/`
- [ ] Total template file count in `.github/PRPs/templates/` is 25 (excluding README.md)
- [ ] Each template file's first line matches the expected content-start (not a fence marker, not a heredoc marker)
- [ ] Each template file's last line matches the expected content-end (not `EOF`, not ` ``` `, not `)"`)
- [ ] Source files (5 prompt files) are NOT modified in any way
- [ ] `uv run pytest tests/ -v` exits 0 with no regressions
- [ ] Level 3 content spot-check passes for all 6 templates

---

## Completion Checklist

- [ ] Task 0: Prerequisites verified (dir exists, no target files pre-exist)
- [ ] Task 1: `prp-implement.prompt-summary-template.md` created and validated
- [ ] Task 2: `prp-issue-fix.prompt-pr-template.md` created and validated
- [ ] Task 3: `prp-issue-fix.prompt-review-template.md` created and validated
- [ ] Task 4: `prp-issue-investigate.prompt-comment-template.md` created and validated
- [ ] Task 5: `prp-plan.prompt-summary-template.md` created and validated
- [ ] Task 6: `prp-ralph.prompt-report-template.md` created and validated
- [ ] Task 7: Final validation — all 6 files, source files unchanged, test suite green
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------------------------------------|------------|--------|----------------------------------------------------------------------------|
| Line numbers differ from estimates | LOW | HIGH | Re-read file immediately before each extraction (skill safety rule enforced in tasks) |
| Heredoc EOF line included in extract | LOW | MED | Last-line validation step checks it is NOT `EOF` or `)"` |
| Fence marker included in extract | LOW | MED | First-line validation checks it does NOT start with ` ``` ` |
| Wrong file overwritten | LOW | HIGH | `Test-Path` check in Task 0; skill safety rule requires confirmation if file exists |
| Ralph 3-space indent unexpected | NONE | LOW | Documented in GOTCHA; PRD mandates verbatim; CommonMark allows it |

---

## Notes

**Parallelism**: Tasks 1–6 are fully independent. An agent can run them in any order or assign
multiple sub-tasks simultaneously. The validation commands in Task 7 must run after all 6 tasks
complete.

**Phase 2 readiness**: Once all 6 template files are confirmed, Phase 2
(`extract-remaining-templates-phase-2.plan.md` — to be created next) will update the 5 source
prompt files by replacing each inline block with the two-line reference instruction pattern.

**Phase 3 parallel opportunity**: Phase 3 (Extract Agent Templates — 12 files from 10 agents) is
fully independent of this phase and can run concurrently in a separate session. To plan it:
`/prp-plan .claude/PRPs/prds/extract-remaining-templates.prd.md` (it will select Phase 3 as the
next pending actionable phase after Phase 1 is marked in-progress).

**Naming cross-reference**: The PRD specifies these exact template names (use these, not any
alternatives):
- `prp-implement.prompt-summary-template.md` (not `complete`)
- `prp-plan.prompt-summary-template.md` (not `created`)
- `prp-ralph.prompt-report-template.md` (not `implementation-report`)
