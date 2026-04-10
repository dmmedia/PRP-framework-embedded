# Feature: Extract Remaining Templates — Phase 2: Update Prompt Files

## Summary

Replace the 6 remaining inline output template blocks in 5 prompt files under `.github/prompts/`
with two-line reference instructions that point to the standalone template files created in Phase 1.
Three of the six blocks are bash heredoc commands; they receive a reference comment above the shell
command and the heredoc is replaced with a `$(cat <template-file>)` call. The other three are
plain fenced markdown blocks replaced verbatim with the reference instruction. All operations use
the `text-file-content-extractor-replacer` skill in **replace mode** (PowerShell array-splice).

## User Story

As a framework maintainer editing an output format  
I want to find and edit the output template independently of the surrounding prompt instructions  
So that I can update one concern without risking accidental changes to instruction logic

## Problem Statement

5 prompt files still contain at least one inline output template block that must be read in context
of 200–400 lines of instruction logic before it can be edited. Phase 1 created 6 standalone
template files but did NOT update the source files. After this phase every prompt has a two-line
reference with no inline template content.

## Solution Statement

Use the `text-file-content-extractor-replacer` skill's `replace` mode to splice out each inline
block and splice in the two-line reference (or reference + cat-based bash command for heredoc
blocks). Operations on different files are independent and can be executed in parallel. The two
operations on `prp-issue-fix.prompt.md` must be sequential to avoid line-number drift.

## Metadata

| Field | Value |
| ---------------- | ------------------------------------------------------- |
| Type | REFACTOR |
| Complexity | LOW |
| Systems Affected | `.github/prompts/` (5 files) |
| Dependencies | Phase 1 complete (6 template files exist) |
| Estimated Tasks | 6 replace tasks + 1 validation task = 7 tasks |

---

## UX Design

### Before State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────┐   scroll 200+ lines   ┌──────────────────────────┐ ║
║  │  prp-plan.prompt.md  │ ──────────────────────►│  inline ```markdown      │ ║
║  │  (450 lines)         │                         │  ## Plan Created         │ ║
║  │                      │                         │  (49 inline lines)       │ ║
║  └──────────────────────┘                         └──────────────────────────┘ ║
║                                                             │                 ║
║                                                     edit template             ║
║                                              (alongside instruction logic)    ║
║                                                                               ║
║   USER_FLOW: open prompt → scroll past phases → find template → edit in-place ║
║   PAIN_POINT: changing output format requires touching instruction logic file  ║
║   DATA_FLOW: template content embedded inside .prompt.md                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌──────────────────────┐   read reference      ┌──────────────────────────┐ ║
║  │  prp-plan.prompt.md  │ ──────────────────────►│ > Output Template: See   │ ║
║  │  (2 reference lines) │                         │   prp-plan.prompt-       │ ║
║  │                      │                         │   summary-template.md    │ ║
║  └──────────────────────┘                         └──────────┬───────────────┘ ║
║                                                              │  open file     ║
║                                                              ▼                ║
║                                          ┌───────────────────────────────────┐ ║
║                                          │ .github/PRPs/templates/            │ ║
║                                          │ prp-plan.prompt-summary-           │ ║
║                                          │ template.md  (standalone)          │ ║
║                                          └───────────────────────────────────┘ ║
║                                                                               ║
║   USER_FLOW: open prompt → read 2-line reference → open template file alone   ║
║   VALUE_ADD: edit output format without touching instruction logic             ║
║   DATA_FLOW: template content lives in standalone file; prompt has pointer     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `prp-implement.prompt.md` Phase 6 | 55-line `````markdown` block inline | 2-line reference | Edit format in `prp-implement.prompt-summary-template.md` |
| `prp-issue-fix.prompt.md` §7.2 | 57-line heredoc `gh pr create` | reference + cat bash | Edit PR body in `prp-issue-fix.prompt-pr-template.md` |
| `prp-issue-fix.prompt.md` §8.2 | 33-line heredoc `gh pr comment` | reference + cat bash | Edit review comment in `prp-issue-fix.prompt-review-template.md` |
| `prp-issue-investigate.prompt.md` Phase 6 | 64-line heredoc `gh issue comment` | reference + cat bash | Edit issue comment in `prp-issue-investigate.prompt-comment-template.md` |
| `prp-plan.prompt.md` `<output>` | 49-line `````markdown` block inline | 2-line reference | Edit plan summary in `prp-plan.prompt-summary-template.md` |
| `prp-ralph.prompt.md` §4.2 Step 1 | 30-line indented `````markdown` block | 2-line indented reference | Edit report in `prp-ralph.prompt-report-template.md` |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/skills/text-file-content-extractor-replacer/SKILL.md` | all | Skill interface — replace mode commands (PowerShell) |
| P0 | `.github/prompts/prp-implement.prompt.md` | 346–405 | Verify Task 1 block boundaries before replacing |
| P0 | `.github/prompts/prp-issue-fix.prompt.md` | 378–440 | Verify Task 2 block boundaries before replacing |
| P0 | `.github/prompts/prp-issue-fix.prompt.md` | 470–512 | Verify Task 3 block boundaries (re-read AFTER Task 2) |
| P0 | `.github/prompts/prp-issue-investigate.prompt.md` | 295–366 | Verify Task 4 block boundaries before replacing |
| P0 | `.github/prompts/prp-plan.prompt.md` | 346–401 | Verify Task 5 block boundaries before replacing |
| P0 | `.github/prompts/prp-ralph.prompt.md` | 248–287 | Verify Task 6 block boundaries before replacing |
| P1 | `.github/prompts/prp-prd.prompt.md` | 222–226 | MIRROR reference instruction format exactly |

**External Documentation:**

| Source | Section | Why Needed |
|--------|---------|------------|
| None required | — | Pure markdown text operations, no external libs |

---

## Patterns to Mirror

**REFERENCE_INSTRUCTION for markdown blocks (COPY EXACTLY):**

```markdown
# SOURCE: .github/prompts/prp-prd.prompt.md:224-225
# COPY THIS PATTERN:
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

**REFERENCE_INSTRUCTION for bash heredoc blocks (COPY EXACTLY):**

```markdown
# SOURCE: .github/PRPs/prds/extract-remaining-templates.prd.md — Template Reference Pattern
# COPY THIS PATTERN (reference comment above bash command):
> **{Label} Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file for the {label} content structure.

````bash
{original-gh-command} --body "$(cat .github/PRPs/templates/{name}.prompt-{function}-template.md)"
````
```

**SKILL REPLACE MODE — PowerShell (COPY EXACTLY):**

```powershell
# SOURCE: .github/skills/text-file-content-extractor-replacer/SKILL.md
# COPY THIS PATTERN (array form):
$src   = ".github\prompts\{filename}"
$start = <START_LINE>   # 1-based
$end   = <END_LINE>     # 1-based, inclusive

$newBlock = @(
    "> **Output Template**: See ```.github/PRPs/templates/{template-name}.md```",
    "> Load this file and use its structure exactly when generating output."
)

$lines  = Get-Content $src
$before = if ($start -gt 1)           { $lines[0..($start - 2)] } else { @() }
$after  = if ($end -lt $lines.Count)  { $lines[$end..($lines.Count - 1)] } else { @() }

($before + $newBlock + $after) | Set-Content $src -Encoding utf8
```

---

## Files to Change

| File | Action | Task |
|------|--------|------|
| `.github/prompts/prp-implement.prompt.md` | UPDATE | Task 1 |
| `.github/prompts/prp-issue-fix.prompt.md` | UPDATE | Task 2, Task 3 |
| `.github/prompts/prp-issue-investigate.prompt.md` | UPDATE | Task 4 |
| `.github/prompts/prp-plan.prompt.md` | UPDATE | Task 5 |
| `.github/prompts/prp-ralph.prompt.md` | UPDATE | Task 6 |

---

## NOT Building (Scope Limits)

- **Agent file updates** — that is Phase 3 (separate plan)
- **Template content changes** — content was extracted verbatim in Phase 1; no editing now
- **Markdown linting** — explicitly out of scope per PRD requirements
- **New template naming conventions** — follow the established `<name>.prompt-<function>-template.md` pattern

---

## Step-by-Step Tasks

Execute in order. Tasks 1, 4, 5, 6 are fully independent. Task 2 must complete before Task 3
(same file — line numbers shift after Task 2). All tasks must verify line numbers by re-reading
immediately before executing the skill command.

---

### Task 1: UPDATE `prp-implement.prompt.md` — Replace Phase 6 markdown block

- **ACTION**: REPLACE inline `````markdown` block with two-line reference
- **FILE**: `.github/prompts/prp-implement.prompt.md` (454 lines)
- **CONFIRM LINES**: Read lines 346–406 to confirm block boundaries before replacing
  - Expected: line 349 = ` ```markdown `, line 350 = `## Implementation Complete`, line 403 = ` ``` `
- **BLOCK TO REPLACE**: lines 349–403 (55 lines, the entire fenced block including fences)
- **REPLACEMENT** (2 lines):
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-implement.prompt-summary-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **MIRROR**: `.github/prompts/prp-prd.prompt.md:224-225` — exact reference instruction format
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-implement.prompt-summary-template.md` ✓
- **GOTCHA**: The block uses plain triple backticks (not quadruple). Include both the opening ` ```markdown ` and closing ` ``` ` lines in the start–end range.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-implement.prompt.md") | Select-String "Implementation Complete"` → should return 0 matches

---

### Task 2: UPDATE `prp-issue-fix.prompt.md` — Replace §7.2 heredoc block

- **ACTION**: REPLACE quadruple-backtick bash block containing `gh pr create` heredoc with reference comment + cat-based bash command
- **FILE**: `.github/prompts/prp-issue-fix.prompt.md` (596 lines)
- **CONFIRM LINES**: Read lines 378–440 to confirm block boundaries before replacing
  - Expected: line 379 = `### 7.2 Create PR`, line 381 = ` ````bash `, line 382 starts with `gh pr create`, line 437 = ` ```` `
- **BLOCK TO REPLACE**: lines 381–437 (57 lines, including outer quadruple-backtick fences)
- **REPLACEMENT** (6 lines):
  ```
  > **PR Body Template**: See `.github/PRPs/templates/prp-issue-fix.prompt-pr-template.md`
  > Load this file for the PR body content structure.
  
  ````bash
  gh pr create --base "{base-branch}" --title "Fix: {title} (#{number})" --body "$(cat .github/PRPs/templates/prp-issue-fix.prompt-pr-template.md)"
  ````
  ```
- **MIRROR**: PRD `extract-remaining-templates.prd.md` — "Template Reference Pattern" heredoc replacement pattern
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-issue-fix.prompt-pr-template.md` ✓
- **GOTCHA**: The outer fence is quadruple-backtick (` ```` `), not triple. Preserve the quadruple-backtick fence in the replacement. The closing ` ```` ` at line 437 is the END of the replace range — include it in the replacement block.
- **GOTCHA**: `gh pr create` full command line must be read from the source file (line 382) before writing the replacement — do not invent flags.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-issue-fix.prompt.md") | Select-String "cat <<'EOF'"` → should return 0 matches for §7.2 (§8.2 may still match until Task 3)

---

### Task 3: UPDATE `prp-issue-fix.prompt.md` — Replace §8.2 heredoc block

**MUST EXECUTE AFTER TASK 2** — line numbers shifted after Task 2 replaced 57 lines with 6 lines
(net -51 lines). Re-read the file to get new §8.2 line numbers.

- **ACTION**: REPLACE triple-backtick bash block containing `gh pr comment` heredoc with reference comment + cat-based bash command
- **FILE**: `.github/prompts/prp-issue-fix.prompt.md` (line count changed after Task 2)
- **CONFIRM LINES**: Re-read file lines 420–465 (approx.) after Task 2 to find `### 8.2 Post Review to PR` and the bash fence boundaries
  - Expected context: `### 8.2 Post Review to PR` → blank → ` ```bash ` → `gh pr comment --body "$(cat <<'EOF'"` → ... → `EOF` → `)` → ` ``` `
- **BLOCK TO REPLACE**: the entire ` ```bash ... ``` ` block (triple-backtick, ~33 lines including fences) 
- **REPLACEMENT** (6 lines):
  ```
  > **Review Comment Template**: See `.github/PRPs/templates/prp-issue-fix.prompt-review-template.md`
  > Load this file for the review comment content structure.
  
  ```bash
  gh pr comment --body "$(cat .github/PRPs/templates/prp-issue-fix.prompt-review-template.md)"
  ```
  ```
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-issue-fix.prompt-review-template.md` ✓
- **GOTCHA**: Triple-backtick fence (not quadruple). The replacement code fence must also use triple backticks.
- **GOTCHA**: `gh pr comment` full command must be read from the source line before writing — do not invent flags.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-issue-fix.prompt.md") | Select-String "cat <<'EOF'"` → 0 matches

---

### Task 4: UPDATE `prp-issue-investigate.prompt.md` — Replace Phase 6 heredoc block

- **ACTION**: REPLACE quadruple-backtick bash block containing `gh issue comment` heredoc with reference comment + cat-based bash command
- **FILE**: `.github/prompts/prp-issue-investigate.prompt.md` (448 lines)
- **CONFIRM LINES**: Read lines 296–365 to confirm block boundaries before replacing
  - Expected: line 299 = ` ````bash `, line 300 = `gh issue comment {number} --body "$(cat <<'EOF'"`, line 362 = ` ```` `
- **BLOCK TO REPLACE**: lines 299–362 (64 lines, including outer quadruple-backtick fences)
- **REPLACEMENT** (6 lines):
  ```
  > **Issue Comment Template**: See `.github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md`
  > Load this file for the GitHub comment content structure.
  
  ````bash
  gh issue comment {number} --body "$(cat .github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md)"
  ````
  ```
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-issue-investigate.prompt-comment-template.md` ✓
- **GOTCHA**: Outer fence is quadruple-backtick. Preserve in replacement.
- **GOTCHA**: `gh issue comment {number}` — the `{number}` placeholder must be preserved exactly as-is.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-issue-investigate.prompt.md") | Select-String "cat <<'EOF'"` → 0 matches

---

### Task 5: UPDATE `prp-plan.prompt.md` — Replace REPORT_TO_USER markdown block

- **ACTION**: REPLACE inline `````markdown` block in `<output>` section with two-line reference
- **FILE**: `.github/prompts/prp-plan.prompt.md` (450 lines)
- **CONFIRM LINES**: Read lines 347–402 to confirm block boundaries before replacing
  - Expected: line 350 = ` ```markdown `, line 351 = `## Plan Created`, line 398 = ` ``` `
- **BLOCK TO REPLACE**: lines 350–398 (49 lines, including fences)
- **REPLACEMENT** (2 lines):
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-plan.prompt-summary-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **MIRROR**: `.github/prompts/prp-prd.prompt.md:224-225` — exact reference instruction format
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-plan.prompt-summary-template.md` ✓
- **GOTCHA**: Note that `prp-plan.prompt.md` already has reference instructions at lines 247–248 (Phase 4 design template) and 331–332 (Phase 6 plan template) from Phase 1. Those are NOT touched. Only the REPORT_TO_USER block in `<output>` is replaced.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-plan.prompt.md") | Select-String "## Plan Created"` → 0 matches

---

### Task 6: UPDATE `prp-ralph.prompt.md` — Replace §4.2 Step 1 indented markdown block

- **ACTION**: REPLACE 3-space-indented `````markdown` block with 3-space-indented two-line reference
- **FILE**: `.github/prompts/prp-ralph.prompt.md` (424 lines)
- **CONFIRM LINES**: Read lines 248–287 to confirm block boundaries before replacing
  - Expected: line 254 = `   ```markdown ` (3-space indent), line 255 = `   # Implementation Report`, line 283 = `   ``` ` (3-space indent)
- **BLOCK TO REPLACE**: lines 254–283 (30 lines, including indented fences)
- **REPLACEMENT** (2 lines, 3-space indented to match surrounding list context):
  ```
     > **Output Template**: See `.github/PRPs/templates/prp-ralph.prompt-report-template.md`
     > Load this file and use its structure exactly when generating output.
  ```
  **Note**: Each line begins with exactly 3 spaces to match the indentation of the surrounding numbered-list item.
- **TEMPLATE EXISTS**: `.github/PRPs/templates/prp-ralph.prompt-report-template.md` ✓
- **GOTCHA**: The existing `prp-ralph.prompt.md` already has references at lines 128–129 (Phase 2.2) and lines 207–208 (Phase 3.8) from Phase 1. Only the §4.2 Step 1 block at lines 254–283 is the target.
- **GOTCHA**: Must preserve 3-space indentation on both reference lines so the blockquote renders correctly inside the numbered-list step context.
- **VALIDATE**: `(Get-Content ".github\prompts\prp-ralph.prompt.md") | Select-String "# Implementation Report"` → 0 matches

---

### Task 7: Final Validation

Run all validation checks to confirm every inline block is removed.

- **VALIDATE_ALL_HEREDOCS**: 
  ```powershell
  Select-String -Path ".github\prompts\*.prompt.md" -Pattern "cat <<'EOF'" | Select-Object Path, LineNumber, Line
  ```
  Expected: **0 matches**

- **VALIDATE_NO_INLINE_MARKDOWN_BLOCKS** (look for multi-line template indicators):
  ```powershell
  Select-String -Path ".github\prompts\*.prompt.md" -Pattern "## Implementation Complete|## Plan Created|# Implementation Report" | Select-Object Path, LineNumber
  ```
  Expected: **0 matches**

- **VALIDATE_REFERENCES_EXIST** (confirm reference instructions were added):
  ```powershell
  Select-String -Path ".github\prompts\*.prompt.md" -Pattern "Output Template.*prp-implement|PR Body Template|Review Comment Template|Issue Comment Template|Output Template.*prp-plan|Output Template.*prp-ralph" | Select-Object Path, LineNumber
  ```
  Expected: **6 matches** (one per replaced block)

- **VALIDATE_TEMPLATE_FILES** (confirm Phase 1 templates are untouched):
  ```powershell
  Get-ChildItem ".github\PRPs\templates\" -Filter "*.md" | Where-Object { $_.Name -match "prompt-(summary|pr|review|comment|report)" } | Select-Object Name
  ```
  Expected: 6 files listed

- **VALIDATE_LINE_COUNTS** (confirm file sizes decreased):
  ```powershell
  @("prp-implement.prompt.md","prp-issue-fix.prompt.md","prp-issue-investigate.prompt.md","prp-plan.prompt.md","prp-ralph.prompt.md") | ForEach-Object {
      $count = (Get-Content ".github\prompts\$_").Count
      Write-Output "$_ : $count lines"
  }
  ```
  Expected approximate post-edit line counts (pre-edit → post-edit):
  - `prp-implement.prompt.md`: 454 → ~403
  - `prp-issue-fix.prompt.md`: 596 → ~508 (two replacements: -51 + -27 ≈ -88)
  - `prp-issue-investigate.prompt.md`: 448 → ~390
  - `prp-plan.prompt.md`: 450 → ~403
  - `prp-ralph.prompt.md`: 424 → ~396

---

## Testing Strategy

### Verification Checks

| Check | Command | Expected |
|-------|---------|----------|
| No heredoc remnants | `Select-String -Path ".github\prompts\*.prompt.md" -Pattern "cat <<'EOF'"` | 0 matches |
| No inline template markers | `Select-String -Path ".github\prompts\*.prompt.md" -Pattern "## Implementation Complete\|## Plan Created\|# Implementation Report"` | 0 matches |
| References added | `Select-String -Path ".github\prompts\*.prompt.md" -Pattern "Output Template\|PR Body Template\|Review Comment Template\|Issue Comment Template"` | 6 matches |
| Template files intact | `Get-ChildItem ".github\PRPs\templates\" \| Measure-Object` | ≥ 26 files |

### Edge Cases Checklist

- [ ] `prp-issue-fix.prompt.md` Task 2 line numbers confirmed before Task 3 (same file)
- [ ] 3-space indent preserved in `prp-ralph.prompt.md` replacement
- [ ] Quadruple-backtick fences preserved for `prp-issue-fix.prompt.md` §7.2 and `prp-issue-investigate.prompt.md`
- [ ] Existing Phase 1 references in `prp-plan.prompt.md` (lines ~247, ~331) untouched
- [ ] Existing Phase 1 references in `prp-ralph.prompt.md` (lines ~128, ~207) untouched
- [ ] Template file content unchanged (only source files modified)

---

## Validation Commands

### Level 1: STATIC_ANALYSIS

```powershell
# No heredocs remain
Select-String -Path ".github\prompts\*.prompt.md" -Pattern "cat <<'EOF'"
# Expect: no output

# No inline template content remains
Select-String -Path ".github\prompts\*.prompt.md" -Pattern "## Implementation Complete|## Plan Created|# Implementation Report"
# Expect: no output
```

**EXPECT**: Exit with no matches (0 results)

### Level 2: REFERENCE_VERIFICATION

```powershell
# All 6 reference instructions exist
Select-String -Path ".github\prompts\*.prompt.md" -Pattern "Output Template|PR Body Template|Review Comment Template|Issue Comment Template" | Select-Object Path, LineNumber, Line
# Expect: exactly 6 results (one per replaced block)
```

**EXPECT**: 6 matches across 5 files

### Level 3: FILE_INTEGRITY

```powershell
# Template files from Phase 1 still exist and are non-empty
@(
  "prp-implement.prompt-summary-template.md",
  "prp-issue-fix.prompt-pr-template.md",
  "prp-issue-fix.prompt-review-template.md",
  "prp-issue-investigate.prompt-comment-template.md",
  "prp-plan.prompt-summary-template.md",
  "prp-ralph.prompt-report-template.md"
) | ForEach-Object {
    $f = ".github\PRPs\templates\$_"
    if (Test-Path $f) { Write-Output "OK: $_ ($((Get-Content $f).Count) lines)" }
    else { Write-Output "MISSING: $_" }
}
```

**EXPECT**: All 6 show `OK:` with non-zero line counts

### Level 4: MANUAL_SPOT_CHECK

Open each updated file and confirm visually:
1. `prp-implement.prompt.md` — Phase 6 shows only two `>` reference lines, no ` ```markdown ` block
2. `prp-issue-fix.prompt.md` — §7.2 has reference + one-liner `gh pr create`; §8.2 has reference + one-liner `gh pr comment`
3. `prp-issue-investigate.prompt.md` — Phase 6 has reference + one-liner `gh issue comment {number}`
4. `prp-plan.prompt.md` — `<output>` section has two `>` reference lines, no ` ```markdown ` block
5. `prp-ralph.prompt.md` — §4.2 Step 1 has two indented `>` reference lines, no ` ```markdown ` block

---

## Approach

**APPROACH_CHOSEN**: Use `text-file-content-extractor-replacer` skill in `replace` mode
(PowerShell array-splice) for each block.

**RATIONALE**: The skill is the mandated approach per PRD requirements. Its line-number-based
replacement is reliable for multi-line blocks with special characters (backticks, bashisms,
emoji) that would trip up string-matching tools. The PowerShell `Set-Content -Encoding utf8`
preserves file encoding.

**ALTERNATIVES_REJECTED**:
- `replace_string_in_file` tool: Rejected — heredoc and multi-line backtick blocks with special
  characters risk match failure; multi-line context including emoji (§8.2) is fragile with
  exact-string matching.
- Direct `gh pr create` heredoc-to-cat conversion only: Rejected — PRD requires reference comment
  ABOVE the bash command, not just updating the command itself.

**NOT_BUILDING** (explicit scope limits):
- Agent file updates (Phase 3 / Phase 4) — separate plans
- Template content normalization — verbatim only
- Markdown linting — explicitly excluded
