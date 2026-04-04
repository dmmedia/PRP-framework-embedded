# Feature: Extract Agent Output Templates — Phase 4

## Summary

Replace all inline `` ````markdown `` template blocks in 10 agent files in `.github/agents/` with
two-line reference instructions pointing to the standalone template files created in Phase 3.
All operations use the `text-file-content-extractor-replacer` skill in **replace mode only** — no
new files are created. After this phase the full extraction effort is complete: no inline template
blocks remain in any prompt or agent file.

## User Story

As a framework maintainer editing an agent output format  
I want to open a standalone template file directly  
So that I can update the output structure without touching any agent instruction logic

## Problem Statement

All 10 agent files in `.github/agents/` still contain their output format templates as inline
`` ````markdown `` fences even though the template content now exists in standalone files in
`.github/PRPs/templates/`. Any maintainer who edits a template must still navigate the full agent
file. After this phase, each inline block is replaced with a two-line reference instruction and the
agent file instruction logic can be read and edited independently of the template.

## Solution Statement

Use the `text-file-content-extractor-replacer` skill in `replace` mode to substitute each inline
`` ````markdown … ```` `` block with a two-line `> **Output Template**` reference instruction.
12 replacements across 10 agent files (pr-test-analyzer and silent-failure-hunter each have two
template blocks; gpui-researcher secondary "Validation Failed" block is explicitly out of scope
because its content was not extracted in Phase 3). Immediately re-read each file before each write
to confirm exact line numbers.

## Metadata

| Field | Value |
| ---------------- | ----------------------------------------------- |
| Type | REFACTOR |
| Complexity | LOW |
| Systems Affected | `.github/agents/` (10 files) |
| Dependencies | Phase 3 complete — all 12 template files exist |
| Estimated Tasks | 12 replacement tasks + 1 validation task = 13 |

---

## UX Design

### Before State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                              BEFORE STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Maintainer wants to update code-reviewer output format:                      ║
║                                                                               ║
║  ┌─────────────────────────┐                                                  ║
║  │ code-reviewer.md        │ open file, scroll ~105 lines                    ║
║  │ (200+ lines)            │ ──────────────────────────────►                 ║
║  │                         │                                                  ║
║  │ # Instructions...       │       ┌────────────────────────────┐            ║
║  │ ## Behavior...          │       │ ````markdown               │            ║
║  │ ## Output Format        │       │ ## Code Review Report      │            ║
║  │    ↓ (buried here)      │       │ ### Summary                │            ║
║  │                         │       │ ... (64 inline lines) ...  │            ║
║  │                         │       │ ````                       │            ║
║  └─────────────────────────┘       └────────────────────────────┘            ║
║                                                                               ║
║   USER_FLOW: open agent → scroll past 100+ lines of logic → find template    ║
║   PAIN_POINT: template is buried inside instruction logic                     ║
║   DATA_FLOW: template content inline inside agent .md file                    ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### After State

```text
╔═══════════════════════════════════════════════════════════════════════════════╗
║                               AFTER STATE                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Maintainer wants to update code-reviewer output format:                      ║
║                                                                               ║
║  ┌─────────────────────────┐                                                  ║
║  │ code-reviewer.md        │                                                  ║
║  │                         │       ┌─────────────────────────────────────┐   ║
║  │ ## Output Format        │       │ code-reviewer.agent-report-         │   ║
║  │ > **Output Template**:  │──────►│   template.md                       │   ║
║  │ > See .github/PRPs/...  │       │ (standalone, focussed file)         │   ║
║  │ > Load this file...     │       │ ## Code Review Report               │   ║
║  │                         │       │ ... (full template here)            │   ║
║  └─────────────────────────┘       └─────────────────────────────────────┘   ║
║                                                                               ║
║   USER_FLOW: see reference → open template file → edit only format            ║
║   VALUE_ADD: instruction logic and template are in separate files;            ║
║              editing one does not require touching the other                  ║
║   DATA_FLOW: agent file has 2-line reference; template file has content       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| `.github/agents/code-reviewer.md` | ` ````markdown ` block at ~L105–L170 | Two-line reference | Edit template in standalone file |
| `.github/agents/code-simplifier.md` | ` ````markdown ` block at ~L95–L168 | Two-line reference | Edit template in standalone file |
| `.github/agents/codebase-analyst.md` | ` ````markdown ` block at ~L73–L119 | Two-line reference | Edit template in standalone file |
| `.github/agents/codebase-explorer.md` | ` ````markdown ` block at ~L89–L185 | Two-line reference | Edit template in standalone file |
| `.github/agents/comment-analyzer.md` | ` ````markdown ` block at ~L95–L233 | Two-line reference | Edit template in standalone file |
| `.github/agents/gpui-researcher.md` | ` ````markdown ` block at ~L108–L192 (primary only) | Two-line reference | Edit template in standalone file |
| `.github/agents/pr-test-analyzer.md` | ` ````markdown ` block at ~L104–L221 + ` ```markdown ` block at ~L225–L246 | Two reference instructions | Edit each template in its own standalone file |
| `.github/agents/silent-failure-hunter.md` | ` ````markdown ` block at ~L122–L254 + ` ```markdown ` block at ~L259–L279 | Two reference instructions | Edit each template in its own standalone file |
| `.github/agents/type-design-analyzer.md` | ` ````markdown ` block at ~L153–L262 | Two-line reference | Edit template in standalone file |
| `.github/agents/web-researcher.md` | ` ````markdown ` block at ~L86–L128 | Two-line reference | Edit template in standalone file |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/skills/text-file-content-extractor-replacer/SKILL.md` | all | Skill `replace` mode, PowerShell commands, safety rule (re-read before each write) |
| P0 | `.github/agents/code-reviewer.md` | 100–175 | Confirm block range for Task 1 before replacing |
| P0 | `.github/agents/code-simplifier.md` | 90–175 | Confirm block range for Task 2 |
| P0 | `.github/agents/codebase-analyst.md` | 68–125 | Confirm block range for Task 3 |
| P0 | `.github/agents/codebase-explorer.md` | 84–190 | Confirm block range for Task 4 |
| P0 | `.github/agents/comment-analyzer.md` | 90–240 | Confirm block range for Task 5 |
| P0 | `.github/agents/gpui-researcher.md` | 103–200 | Confirm block range for Task 6 |
| P0 | `.github/agents/pr-test-analyzer.md` | 99–250 | Confirm both block ranges for Tasks 7–8 |
| P0 | `.github/agents/silent-failure-hunter.md` | 117–285 | Confirm both block ranges for Tasks 9–10 |
| P0 | `.github/agents/type-design-analyzer.md` | 148–268 | Confirm block range for Task 11 |
| P0 | `.github/agents/web-researcher.md` | 81–133 | Confirm block range for Task 12 |
| P1 | `.github/prompts/prp-plan.prompt.md` | 240–260 | Reference instruction already in use — copy exact two-line format |

**External Documentation:** None required — pure markdown file I/O.

---

## Patterns to Mirror

**REFERENCE_INSTRUCTION_PATTERN:**

```markdown
# SOURCE: .github/prompts/prp-plan.prompt.md:247-248
# COPY THIS FORMAT exactly — it is the established reference instruction:
> **Output Template**: See `.github/PRPs/templates/prp-plan.prompt-summary-template.md`
> Load this file and use its structure exactly when generating output.
```

For agents, substitute the template filename:

```markdown
> **Output Template**: See `.github/PRPs/templates/{agent-name}.agent-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

**SKILL_REPLACE_COMMAND (PowerShell):**

```powershell
# SOURCE: .github/skills/text-file-content-extractor-replacer/SKILL.md
# COPY THIS PATTERN for each replacement (RE-VERIFY $start/$end from fresh file read):
$src   = ".github/agents/code-reviewer.md"
$start = 105   # 1-based, inclusive — RE-VERIFY immediately before running
$end   = 170   # 1-based, inclusive — RE-VERIFY immediately before running

# Two-line reference block:
$newBlock = @(
    '> **Output Template**: See `.github/PRPs/templates/code-reviewer.agent-report-template.md`',
    '> Load this file and use its structure exactly when generating output.'
)

$lines  = Get-Content $src
$before = if ($start -gt 1) { $lines[0..($start - 2)] } else { @() }
$after  = if ($end -lt $lines.Count) { $lines[$end..($lines.Count - 1)] } else { @() }
($before + $newBlock + $after) | Set-Content $src -Encoding utf8
```

**FENCE_BOUNDARY_RULE:**

```text
# The fence markers ARE INCLUDED in the replaced block:
# Line N:   ````markdown      ← fence_open — INCLUDED in replacement range ($start)
# Line N+1: ## ReportTitle    first content line
# ...
# Line M:   last content      last content line
# Line M+1: ````              ← fence_close — INCLUDED in replacement range ($end)
#
# The two-line reference replaces everything from $start...$end (fence markers + content).
# Spot-check $start-1 and $end+1 to confirm they are NOT part of the block.
```

**SECONDARY_BLOCK_RULE (pr-test-analyzer, silent-failure-hunter):**

```text
# Secondary blocks use triple-backtick fences (```markdown ... ```)
# Apply the same replacement pattern, just confirm the fence marker is ``` not ````
# After replacing primary block, LINE NUMBERS SHIFT — re-read file before replacing secondary.
# For pr-test-analyzer secondary, its reference label differs:
#   > **Output Template (Adequate Coverage)**: See ...pr-test-analyzer.agent-adequate-template.md`
# For silent-failure-hunter secondary:
#   > **Output Template (No Issues)**: See ...silent-failure-hunter.agent-pass-template.md`
```

---

## Files to Change

| File | Action | Justification |
|------|--------|---------------|
| `.github/agents/code-reviewer.md` | UPDATE | Replace `` ````markdown `` block (~L105–L170) with reference |
| `.github/agents/code-simplifier.md` | UPDATE | Replace `` ````markdown `` block (~L95–L168) with reference |
| `.github/agents/codebase-analyst.md` | UPDATE | Replace `` ````markdown `` block (~L73–L119) with reference |
| `.github/agents/codebase-explorer.md` | UPDATE | Replace `` ````markdown `` block (~L89–L185) with reference |
| `.github/agents/comment-analyzer.md` | UPDATE | Replace `` ````markdown `` block (~L95–L233) with reference |
| `.github/agents/gpui-researcher.md` | UPDATE | Replace PRIMARY `` ````markdown `` block (~L108–L192); Validation Failed block left as-is (not extracted in Phase 3) |
| `.github/agents/pr-test-analyzer.md` | UPDATE | Replace PRIMARY `` ````markdown `` block (~L104–L221) and SECONDARY ` ```markdown ` block (~L225–L246) with two separate references |
| `.github/agents/silent-failure-hunter.md` | UPDATE | Replace PRIMARY `` ````markdown `` block (~L122–L254) and SECONDARY ` ```markdown ` block (~L259–L279) with two separate references |
| `.github/agents/type-design-analyzer.md` | UPDATE | Replace `` ````markdown `` block (~L153–L262) with reference |
| `.github/agents/web-researcher.md` | UPDATE | Replace `` ````markdown `` block (~L86–L128) with reference |

---

## NOT Building (Scope Limits)

- **gpui-researcher Validation Failed extraction**: The secondary `` ````markdown `` block at ~L199–L212 in `gpui-researcher.md` was explicitly marked "NOT IN SCOPE" in Phase 3's plan. No template file exists for it. It remains inline after Phase 4.
- **New template files**: Phase 4 is replace-only. All 12 template files already exist from Phase 3.
- **docs-impact-agent.md**: Not in the extraction scope per PRD decisions log.
- **Content normalization**: Template content is already in standalone files; no rewrites.
- **markdown-linter validation**: Explicitly excluded per PRD requirements.

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.
**SAFETY RULE**: Re-read the target file immediately before each replacement to confirm exact line numbers — do NOT rely solely on the approximate ranges in this plan.

---

### Task 1: UPDATE `code-reviewer.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/code-reviewer.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/code-reviewer.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L105–L170 (quad-backtick fences included)
- **STEP 1 — READ**: Read `.github/agents/code-reviewer.md` lines 100–175; visually confirm `````markdown` at `$start` and `` ```` `` at `$end`; spot-check `$start-1` and `$end+1`
- **STEP 2 — REPLACE**: Run PowerShell replace command (see SKILL_REPLACE_COMMAND pattern above with these values):
  ```powershell
  $src      = ".github/agents/code-reviewer.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/code-reviewer.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/code-reviewer.md" -Pattern '````markdown'` — must return **0 matches**

---

### Task 2: UPDATE `code-simplifier.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/code-simplifier.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/code-simplifier.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L95–L168 (quad-backtick fences included)
- **STEP 1 — READ**: Read `.github/agents/code-simplifier.md` lines 90–175; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/code-simplifier.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/code-simplifier.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/code-simplifier.md" -Pattern '````markdown'` — 0 matches

---

### Task 3: UPDATE `codebase-analyst.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/codebase-analyst.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/codebase-analyst.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L73–L119 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 68–125; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/codebase-analyst.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/codebase-analyst.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/codebase-analyst.md" -Pattern '````markdown'` — 0 matches

---

### Task 4: UPDATE `codebase-explorer.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/codebase-explorer.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/codebase-explorer.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L89–L185 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 84–190; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/codebase-explorer.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/codebase-explorer.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/codebase-explorer.md" -Pattern '````markdown'` — 0 matches

---

### Task 5: UPDATE `comment-analyzer.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/comment-analyzer.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/comment-analyzer.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L95–L233 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 90–240; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/comment-analyzer.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/comment-analyzer.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/comment-analyzer.md" -Pattern '````markdown'` — 0 matches

---

### Task 6: UPDATE `gpui-researcher.md` — replace PRIMARY template block only

- **ACTION**: Replace the PRIMARY `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/gpui-researcher.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/gpui-researcher.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L108–L192 (quad-backtick fences included)
- **SCOPE NOTE**: The `## If Validation Fails` block (~L199–L212) was NOT extracted in Phase 3 and has no corresponding template file. Leave it inline — do NOT replace it.
- **STEP 1 — READ**: Read lines 103–200; find the FIRST `` ````markdown `` fence (primary block), note start/end; verify that the secondary `` ## If Validation Fails `` section starts on `$end + N` lines after a blank line + header
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/gpui-researcher.md"
  $start    = <confirmed — primary block only>
  $end      = <confirmed — primary block only>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/gpui-researcher.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: After replacement, `Select-String -Path ".github/agents/gpui-researcher.md" -Pattern '````markdown'` — must return exactly **1 match** (the remaining Validation Failed block)

---

### Task 7: UPDATE `pr-test-analyzer.md` — replace PRIMARY template block

- **ACTION**: Replace the PRIMARY `` ````markdown … ```` `` block in `## Output Format` with reference to the main report template
- **SOURCE FILE**: `.github/agents/pr-test-analyzer.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/pr-test-analyzer.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L104–L221 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 99–225; confirm fence boundaries; note this file has a secondary ` ```markdown ` block further down
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/pr-test-analyzer.md"
  $start    = <confirmed — primary only>
  $end      = <confirmed — primary only>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/pr-test-analyzer.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **GOTCHA**: After this replacement the file is shorter — LINE NUMBERS SHIFT. Do NOT use pre-replacement line numbers for Task 8.
- **VALIDATE**: After Task 7 only, file still contains a ` ```markdown ` block (secondary) — that is expected; Task 8 removes it

---

### Task 8: UPDATE `pr-test-analyzer.md` — replace SECONDARY template block

- **ACTION**: Replace the SECONDARY ` ```markdown … ``` ` block inside `## If Coverage Is Adequate` with reference to the adequate template
- **SOURCE FILE**: `.github/agents/pr-test-analyzer.md` (already updated by Task 7)
- **TEMPLATE FILE**: `.github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md`
- **APPROXIMATE RANGE (POST-TASK-7 LINE NUMBERS)**: Re-read after Task 7 to find exact current lines. The secondary block is inside the `## If Coverage Is Adequate` section — search for that heading first.
- **STEP 1 — READ**: Re-read `.github/agents/pr-test-analyzer.md` fully after Task 7; find ` ```markdown ` and the matching closing ` ``` ` inside `## If Coverage Is Adequate`; confirm $start and $end
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/pr-test-analyzer.md"
  $start    = <confirmed — secondary block, post-task-7 line numbers>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template (Adequate Coverage)**: See `.github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/pr-test-analyzer.md" -Pattern '````markdown|` + '```markdown'` — 0 matches for BOTH fence types

---

### Task 9: UPDATE `silent-failure-hunter.md` — replace PRIMARY template block

- **ACTION**: Replace the PRIMARY `` ````markdown … ```` `` block in `## Output Format` with reference to the main report template
- **SOURCE FILE**: `.github/agents/silent-failure-hunter.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/silent-failure-hunter.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L122–L254 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 117–260; confirm fence boundaries; note secondary ` ```markdown ` block below
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/silent-failure-hunter.md"
  $start    = <confirmed — primary only>
  $end      = <confirmed — primary only>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/silent-failure-hunter.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **GOTCHA**: After Task 9, line numbers shift. Do NOT use these pre-Task-9 line numbers for Task 10.
- **VALIDATE**: File still contains a ` ```markdown ` block (expected — Task 10 removes it)

---

### Task 10: UPDATE `silent-failure-hunter.md` — replace SECONDARY template block

- **ACTION**: Replace the SECONDARY ` ```markdown … ``` ` block inside `## If No Issues Found` with reference to the pass template
- **SOURCE FILE**: `.github/agents/silent-failure-hunter.md` (already updated by Task 9)
- **TEMPLATE FILE**: `.github/PRPs/templates/silent-failure-hunter.agent-pass-template.md`
- **APPROXIMATE RANGE (POST-TASK-9)**: Re-read after Task 9; find ` ```markdown ` inside `## If No Issues Found`
- **STEP 1 — READ**: Re-read `.github/agents/silent-failure-hunter.md` after Task 9; locate secondary block; confirm $start/$end
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/silent-failure-hunter.md"
  $start    = <confirmed — secondary, post-task-9 line numbers>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template (No Issues)**: See `.github/PRPs/templates/silent-failure-hunter.agent-pass-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/silent-failure-hunter.md" -Pattern '````markdown|` + '```markdown'` — 0 matches for BOTH fence types

---

### Task 11: UPDATE `type-design-analyzer.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/type-design-analyzer.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/type-design-analyzer.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L153–L262 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 148–268; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/type-design-analyzer.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/type-design-analyzer.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/type-design-analyzer.md" -Pattern '````markdown'` — 0 matches

---

### Task 12: UPDATE `web-researcher.md` — replace primary template block

- **ACTION**: Replace the `` ````markdown … ```` `` block in `## Output Format` with two-line reference
- **SOURCE FILE**: `.github/agents/web-researcher.md`
- **TEMPLATE FILE**: `.github/PRPs/templates/web-researcher.agent-report-template.md`
- **APPROXIMATE RANGE**: Primary block at ~L86–L128 (quad-backtick fences included)
- **STEP 1 — READ**: Read lines 81–133; confirm fence boundaries
- **STEP 2 — REPLACE**:
  ```powershell
  $src      = ".github/agents/web-researcher.md"
  $start    = <confirmed>
  $end      = <confirmed>
  $newBlock = @(
      '> **Output Template**: See `.github/PRPs/templates/web-researcher.agent-report-template.md`',
      '> Load this file and use its structure exactly when generating output.'
  )
  ```
- **VALIDATE**: `Select-String -Path ".github/agents/web-researcher.md" -Pattern '````markdown'` — 0 matches

---

### Task 13: Final cross-file validation

- **ACTION**: Verify no inline template blocks remain in any of the 10 updated agent files (except gpui-researcher's Validation Failed secondary)
- **VALIDATE — quad-backtick scan**:
  ```powershell
  Select-String -Path ".github/agents/*.md" -Pattern "````markdown"
  ```
  **Expected**: 1 match only — `gpui-researcher.md` (the retained Validation Failed block)
  
- **VALIDATE — triple-backtick scan**:
  ```powershell
  Select-String -Path ".github/agents/*.md" -Pattern "` + '```' + `markdown"
  ```
  **Expected**: 0 matches
  
- **VALIDATE — reference instructions present**:
  ```powershell
  Select-String -Path ".github/agents/*.md" -Pattern "Output Template.*agent-.*-template"
  ```
  **Expected**: At minimum 12 matches covering all 10 agent files (pr-test-analyzer and silent-failure-hunter each contribute 2)

- **VALIDATE — reference files exist**:
  ```powershell
  $templates = @(
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
  )
  $templates | ForEach-Object { Test-Path ".github/PRPs/templates/$_" }
  ```
  **Expected**: All `True`

---

## Testing Strategy

### Edge Cases Checklist

- [ ] `gpui-researcher.md`: Only ONE ````markdown block replaced (primary); one remains (Validation Failed)
- [ ] `pr-test-analyzer.md`: Both blocks replaced (quad-backtick primary; triple-backtick secondary)
- [ ] `silent-failure-hunter.md`: Both blocks replaced (quad-backtick primary; triple-backtick secondary)
- [ ] Line numbers confirmed by re-reading immediately before each replacement (not from plan estimates)
- [ ] Secondary blocks replaced with post-Task-7/9 line numbers (line numbers shift after primary removal)
- [ ] Each reference points to a template file that actually exists

---

## Validation Commands

```powershell
# Run after all tasks complete:

# 1. Only gpui-researcher Validation Failed block remains inline (1 match)
Select-String -Path ".github/agents/*.md" -Pattern "````markdown"

# 2. No triple-backtick template blocks remain in agent files
Select-String -Path ".github/agents/*.md" -Pattern "```markdown"

# 3. All 12 reference instructions are present
Select-String -Path ".github/agents/*.md" -Pattern "Output Template.*agent-.*-template"

# 4. Spot-check first line of each template file (verify content wasn't lost)
(Get-Content ".github/PRPs/templates/code-reviewer.agent-report-template.md")[0]
(Get-Content ".github/PRPs/templates/code-simplifier.agent-report-template.md")[0]
(Get-Content ".github/PRPs/templates/silent-failure-hunter.agent-report-template.md")[0]
(Get-Content ".github/PRPs/templates/pr-test-analyzer.agent-adequate-template.md")[0]
```

---

## Decisions Log

| Decision | Choice | Rationale |
|----------|--------|-----------|
| gpui-researcher Validation Failed block | Leave inline (not replaced) | No template file exists for it — Phase 3 explicitly marked it NOT IN SCOPE; replacing without a target file would be misleading |
| Secondary block reference labels | `> **Output Template (Adequate Coverage)**` and `> **Output Template (No Issues)**` | Disambiguates the two references within the same file; maintainer can distinguish which template to open |
| Line number re-verification rule | Re-read file immediately before every replace | Skill safety rule; any intermediate write shifts subsequent line numbers |
| Task ordering for dual-template agents | Primary first, secondary second with fresh line numbers | Primary removal shifts line numbers; secondary MUST use post-primary-replacement line numbers |
