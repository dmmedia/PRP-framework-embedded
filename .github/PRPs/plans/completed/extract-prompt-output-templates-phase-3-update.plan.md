# Feature: Extract Prompt Output Templates — Phase 3: Update Prompts

## Summary

Update all 13 prompt files in `.github/prompts/` to replace their inline output template blocks
with a two-line blockquote reference pointing to the corresponding standalone template file in
`.github/PRPs/templates/`. Phase 1 (directory creation) and Phase 2 (template file extraction)
are already complete — all 19 template files exist. This phase performs the final text-replacement
pass that makes prompts shorter, single-concern, and independently maintainable.

## User Story

As a framework maintainer
I want each prompt file to reference its output template file instead of embedding the template inline
So that I can find, read, and update any output format in under 10 seconds without touching agent instruction logic

## Problem Statement

All 13 prompt files in `.github/prompts/` still embed their output templates inline. The 19 extracted
template files in `.github/PRPs/templates/` are unused — no prompt file references them yet. Until
the references are added, the templates are duplicated (once inline, once in the template file),
which defeats the purpose of the extraction.

## Solution Statement

For each of the 13 prompt files, locate each embedded template block (the fenced markdown code block
that contains the output format) and replace the entire block with the two-line blockquote reference
instruction. 19 total replacements across 13 files. Surrounding instruction text (phase headings,
path annotations, checkpoint lists) is never touched.

## Metadata

| Field            | Value                               |
| ---------------- | ----------------------------------- |
| Type             | REFACTOR                            |
| Complexity       | MEDIUM                              |
| Systems Affected | `.github/prompts/` (13 files)       |
| Dependencies     | Phase 2 complete — 19 template files exist in `.github/PRPs/templates/` |
| Estimated Tasks  | 13 (one per prompt file)            |

---

## UX Design

### Before State

```
╔══════════════════════════════════════════════════════════════════════════╗
║                            BEFORE STATE                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   Maintainer needs to update the PR body output format                   ║
║                                                                          ║
║   ┌───────────────────────┐      ┌───────────────────────────────────┐  ║
║   │ prp-pr.prompt.md      │      │ scroll 300+ lines to find the     │  ║
║   │ (344 lines)           │ ──►  │ heredoc template block buried     │  ║
║   │                       │      │ inside a bash code block          │  ║
║   └───────────────────────┘      └────────────────┬──────────────────┘  ║
║                                                    │                     ║
║                                                    ▼                     ║
║                                    ┌───────────────────────────────┐    ║
║                                    │ Edit template content         │    ║
║                                    │ ⚠ Risk: accidentally modify   │    ║
║                                    │ surrounding agent logic        │    ║
║                                    └───────────────────────────────┘    ║
║                                                                          ║
║   USER_FLOW: Open prompt → scroll → find template buried in prose       ║
║   PAIN_POINT: Two concerns (logic + format) in one file; easy to        ║
║               accidentally damage logic while editing format             ║
║   DATA_FLOW: Template inline → agent reads it directly from prompt      ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### After State

```
╔══════════════════════════════════════════════════════════════════════════╗
║                             AFTER STATE                                   ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║   Maintainer needs to update the PR body output format                   ║
║                                                                          ║
║   ┌───────────────────────────────────────────────────┐                 ║
║   │ .github/PRPs/templates/prp-pr.prompt-pr-template.md │               ║
║   │ (30 lines — template only)                          │               ║
║   └────────────────────────┬──────────────────────────┘                 ║
║                             │ open directly, edit in isolation           ║
║                             ▼                                            ║
║                  ┌──────────────────────┐                               ║
║                  │ Edit template format │  (no risk to prompt logic)    ║
║                  └──────────────────────┘                               ║
║                                                                          ║
║   prp-pr.prompt.md now contains:                                         ║
║   > **Output Template**: See `.github/PRPs/templates/...`                ║
║   > Load this file and use its structure exactly when generating output. ║
║                                                                          ║
║   USER_FLOW: Open template file → edit → done (10 seconds)              ║
║   VALUE_ADD: Zero risk of modifying agent logic; clear file purpose      ║
║   DATA_FLOW: Prompt references template → agent loads template file      ║
║               → agent uses template structure for output                 ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

### Interaction Changes

| Location | Before | After | User Impact |
|----------|--------|-------|-------------|
| Each of 13 prompt files | Contains inline ```` ```markdown ```` template block | Contains 2-line blockquote reference | Prompts are 8–334 lines shorter; single-concern |
| `.github/PRPs/templates/` | 19 template files exist but unreferenced | Each template file is pointed to by its source prompt | Maintainer can navigate directly to any template |
| Template editing workflow | Must open prompt, scroll, edit carefully | Open template file directly in isolation | Faster, safer, no accidental logic damage |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|----------|------|-------|---------------|
| P0 | `.github/PRPs/templates/README.md` | all | Contains the confirmed reference pattern and naming convention |
| P0 | `.github/prompts/prp-commit.prompt.md` | 60–80 | Simplest example — understand what you are replacing before tackling complex files |
| P1 | `.github/prompts/prp-plan.prompt.md` | 236–298 | Design template (plain fence); understand what stays and what goes |
| P1 | `.github/prompts/prp-plan.prompt.md` | 350–695 | Plan template (4-backtick fence); largest replacement |
| P1 | `.github/prompts/prp-pr.prompt.md` | 165–225 | PR body template in bash heredoc — special case |
| P2 | `.github/prompts/prp-issue-investigate.prompt.md` | 255–350 | 4-backtick fence — second special case |
| P2 | `.github/prompts/prp-ralph-cancel.prompt.md` | 30–50 | Indented fence — third special case |

---

## Patterns to Mirror

**REFERENCE_INSTRUCTION_PATTERN:**

```markdown
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

SOURCE: `.github/PRPs/templates/README.md` — this is the confirmed pattern.

**REPLACEMENT_RULE — Standard case (````markdown` fence):**

```
FIND (example from prp-commit.prompt.md):
## Phase 4: OUTPUT

```markdown
**Committed**: {hash} - {message}
**Files**: {count} files (+{add}/-{del})

Next: `git push` or `/prp-pr`
```

REPLACE WITH:
## Phase 4: OUTPUT

> **Output Template**: See `.github/PRPs/templates/prp-commit.prompt-output-template.md`
> Load this file and use its structure exactly when generating output.
```

**REPLACEMENT_RULE — 4-backtick fence (prp-plan.prompt.md plan template, prp-issue-investigate.prompt.md):**

The opening fence is ```` ````markdown ```` (4 backticks) and the closing fence is ```` ```` ```` (4 backticks).
Replace the entire fenced block (opening `` ````markdown `` through closing `` ```` ``) with the reference instruction.

**REPLACEMENT_RULE — Plain fence (prp-plan.prompt.md design template):**

The opening fence is ` ``` ` (no language label). Replace only the fenced block (` ``` ` through ` ``` `).
The surrounding "**CREATE ASCII diagrams...**" instruction and "**DOCUMENT interaction changes:**" table stay.

**REPLACEMENT_RULE — Bash heredoc (prp-pr.prompt.md PR body template):**

The PR body template is embedded inside a ` ```bash ` block as a heredoc body.
Replace the ENTIRE ` ```bash `...` ``` ` code block with the reference instruction.
Add a prose note so the agent still knows to use `gh pr create`:

```markdown
> **Output Template**: See `.github/PRPs/templates/prp-pr.prompt-pr-template.md`
> Load this file and use its content as the `--body` value for `gh pr create`.
```

**REPLACEMENT_RULE — Indented fence (prp-ralph-cancel.prompt.md):**

The fence is indented 3 spaces: `   ```markdown` ... `   ``` `.
Replace the indented block (including its 3-space indent) with the reference instruction (no indent needed).

**WHAT TO PRESERVE:**
- Phase headings (`## Phase N: ...`, `### N.N ...`)  
- Path annotations (`**Path**: \`.claude/PRPs/...\``)
- Checkpoint lists (`**PHASE_N_CHECKPOINT:**`)
- ALL prose instruction text before/after the template block
- Any code blocks that are NOT the extracted template (e.g., bash `mkdir` commands)

**WHAT TO CONFIRM STAYS INLINE (not replaced):**

These blocks exist in some prompts but were NOT extracted — they stay exactly as-is:

| Prompt | Block that STAYS | Location |
|--------|-----------------|----------|
| `prp-debug.prompt.md` | `## Root Cause Analysis Complete` output summary | Phase 6 (~line 277) |
| `prp-implement.prompt.md` | `## Implementation Complete` output summary | Phase 6 (~line 422) |
| `prp-issue-investigate.prompt.md` | `## Investigation Complete` output summary | Phase 7 (~line 549) |
| `prp-plan.prompt.md` | `REPORT_TO_USER` output summary | `<output>` tag (~line 708) |
| `prp-ralph.prompt.md` | State file YAML structure | Phase 2.1 (~line 88) |
| `prp-ralph.prompt.md` | Codebase patterns example | Phase 3.9 (~line 252) |
| `prp-ralph.prompt.md` | Completion report (indented) | Phase 4.2 (~line 290) |
| `prp-ralph.prompt.md` | CLAUDE.md pattern example (indented) | Phase 4.3 (~line 350) |

---

## Files to Change

| File | Action | Templates to Replace |
|------|--------|---------------------|
| `.github/prompts/prp-commit.prompt.md` | UPDATE | 1 — output template block |
| `.github/prompts/prp-ralph-cancel.prompt.md` | UPDATE | 1 — cancel template block (indented) |
| `.github/prompts/prp-issue-fix.prompt.md` | UPDATE | 1 — report template block |
| `.github/prompts/prp-debug.prompt.md` | UPDATE | 1 — report template block only |
| `.github/prompts/prp-implement.prompt.md` | UPDATE | 1 — report template block only |
| `.github/prompts/prp-review-agents.prompt.md` | UPDATE | 1 — summary template block |
| `.github/prompts/prp-issue-investigate.prompt.md` | UPDATE | 1 — artifact template block (4-backtick) |
| `.github/prompts/prp-ralph.prompt.md` | UPDATE | 2 — setup template + progress template |
| `.github/prompts/prp-codebase-question.prompt.md` | UPDATE | 2 — research template + summary template |
| `.github/prompts/prp-pr.prompt.md` | UPDATE | 2 — pr-body template (bash heredoc) + summary template |
| `.github/prompts/prp-prd.prompt.md` | UPDATE | 2 — prd template + summary template |
| `.github/prompts/prp-review.prompt.md` | UPDATE | 2 — report template + summary template |
| `.github/prompts/prp-plan.prompt.md` | UPDATE | 2 — design template (plain fence) + plan template (4-backtick) |

---

## NOT Building (Scope Limits)

- **Template content changes** — templates are extracted verbatim; do NOT edit `.github/PRPs/templates/*.md` files
- **Normalizing prompt structure** — only the template blocks are replaced; do NOT rewrite surrounding instruction text
- **README updates** — `.github/PRPs/templates/README.md` already documents the naming convention; no changes needed
- **Deduplication of shared template patterns** — out of scope (separate concern)

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

---

### Task 1: UPDATE `prp-commit.prompt.md`

- **ACTION**: Replace 1 inline template block with reference
- **FIND**: The `## Phase 4: OUTPUT` section (~line 66) containing:
  ```
  ```markdown
  **Committed**: {hash} - {message}
  **Files**: {count} files (+{add}/-{del})
  
  Next: `git push` or `/prp-pr`
  ```
  ```
- **REPLACE** the entire fenced block (` ```markdown ` through ` ``` `) with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-commit.prompt-output-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: The `## Phase 4: OUTPUT` heading, the surrounding `---` dividers, and the `## Examples` section below
- **GOTCHA**: The section ends at `---` and then `## Examples` — make sure the `---` dividers remain after the replacement
- **VALIDATE**: 
  ```bash
  grep -n "Output Template.*prp-commit" .github/prompts/prp-commit.prompt.md
  # Expected: One line showing the reference
  grep -c "```markdown" .github/prompts/prp-commit.prompt.md
  # Expected: 0
  ```

---

### Task 2: UPDATE `prp-ralph-cancel.prompt.md`

- **ACTION**: Replace 1 inline template block (indented 3 spaces) with reference
- **FIND**: The `   d. Report:` step (~line 35) followed by the indented fence:
  ```
     ```markdown
     ## Ralph Loop Cancelled
     ...
     ```
  ```
  Block runs approximately lines 37–50 (inclusive of the indented backtick fences).
- **REPLACE** the entire indented fenced block (including `   ```markdown` and `   ``` `) with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-ralph-cancel.prompt-cancel-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
  (No indent needed on the reference; blockquote `>` is flush left.)
- **PRESERVE**: `d. Report:` line above the block stays untouched
- **GOTCHA**: The closing ```` ``` ```` is indented; make sure there is no trailing whitespace and that the replacement is flush with the left margin
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-ralph-cancel" .github/prompts/prp-ralph-cancel.prompt.md
  # Expected: One line with the reference
  grep -c "Ralph Loop Cancelled" .github/prompts/prp-ralph-cancel.prompt.md
  # Expected: 0 (template content is now only in the template file)
  ```

---

### Task 3: UPDATE `prp-issue-fix.prompt.md`

- **ACTION**: Replace 1 inline template block with reference
- **FIND**: The `## Phase 10: REPORT - Output to User` section (~line 536) containing:
  ```
  ```markdown
  ## Implementation Complete
  
  **Issue**: #{number} - {title}
  ...
  ```
  ```
  Block runs approximately lines 538–571.
- **REPLACE** the entire fenced block with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-issue-fix.prompt-report-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: The `## Phase 10: REPORT - Output to User` heading above; the `---` and `## Handling Edge Cases` section below
- **GOTCHA**: Do NOT touch any other code blocks in this file (there are many preceding phases with their own instruction blocks)
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-issue-fix" .github/prompts/prp-issue-fix.prompt.md
  # Expected: One line with the reference
  grep -c "Implementation Complete" .github/prompts/prp-issue-fix.prompt.md
  # Expected: 0
  ```

---

### Task 4: UPDATE `prp-debug.prompt.md`

- **ACTION**: Replace 1 inline template block with reference (leave Phase 6 output summary untouched)
- **FIND**: The `### 5.2 Generate Report` section (~line 203) containing:
  ```
  **Path**: `.claude/PRPs/debug/rca-{issue-slug}.md`
  
  ```markdown
  # Root Cause Analysis
  
  **Issue**: {One-line symptom description}
  ...
  ```
  ```
  Block runs approximately lines 205–254.
- **REPLACE** the entire fenced block (` ```markdown ` through ` ``` `) with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-debug.prompt-report-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: `### 5.2 Generate Report` heading, `**Path**: ...` annotation above the block, `**PHASE_5_CHECKPOINT:**` below — all stay intact
- **DO NOT TOUCH**: The `## Phase 6: OUTPUT - Report to User` block (~line 277) with the `## Root Cause Analysis Complete` summary — this is NOT extracted and stays inline
- **GOTCHA**: There are other ````markdown` blocks in this file that are NOT templates (e.g., small inline examples in earlier phases). Only replace the one specific block in `### 5.2 Generate Report`.
- **IDENTIFY**: The correct block starts with `# Root Cause Analysis` on the first content line after the opening fence
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-debug" .github/prompts/prp-debug.prompt.md
  # Expected: One line with the reference
  grep -c "# Root Cause Analysis$" .github/prompts/prp-debug.prompt.md
  # Expected: 0
  grep -c "Root Cause Analysis Complete" .github/prompts/prp-debug.prompt.md
  # Expected: 1 (the Phase 6 summary stays inline — do NOT touch it)
  ```

---

### Task 5: UPDATE `prp-implement.prompt.md`

- **ACTION**: Replace 1 inline template block with reference (leave Phase 6 output summary untouched)
- **FIND**: The `### 5.2 Generate Report` section (~line 300) containing:
  ```
  **Path**: `.claude/PRPs/reports/{plan-name}-report.md`
  
  ```markdown
  # Implementation Report
  
  **Plan**: `$ARGUMENTS`
  ...
  ```
  ```
  Block runs approximately lines 302–365.
- **REPLACE** the entire fenced block with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-implement.prompt-report-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: `### 5.2 Generate Report` heading, `**Path**:` annotation, `### 5.3 Update Source PRD (if applicable)` section below — all stay
- **DO NOT TOUCH**: The `## Phase 6: OUTPUT - Report to User` block (~line 422) with `## Implementation Complete` summary — this is NOT extracted and stays inline
- **GOTCHA**: There are multiple ````markdown` blocks in this large file. Target only the one in `### 5.2 Generate Report` with `# Implementation Report` as its first content line
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-implement" .github/prompts/prp-implement.prompt.md
  # Expected: One line with the reference
  grep -c "# Implementation Report$" .github/prompts/prp-implement.prompt.md
  # Expected: 0
  grep -c "## Implementation Complete" .github/prompts/prp-implement.prompt.md
  # Expected: 1 (Phase 6 summary stays inline)
  ```

---

### Task 6: UPDATE `prp-review-agents.prompt.md`

- **ACTION**: Replace 1 inline template block with reference
- **FIND**: The `### Summary Format` section (~line 120) containing:
  ```
  ```markdown
  ## PR Review Summary
  
  ### Critical Issues (X found)
  ...
  ```
  ```
  Block runs approximately lines 124–154.
- **REPLACE** the entire fenced block with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-review-agents.prompt-summary-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: The `### Summary Format` heading above; `## Post to GitHub` section below
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-review-agents" .github/prompts/prp-review-agents.prompt.md
  # Expected: One line with the reference
  grep -c "PR Review Summary" .github/prompts/prp-review-agents.prompt.md
  # Expected: 0
  ```

---

### Task 7: UPDATE `prp-issue-investigate.prompt.md`

- **ACTION**: Replace 1 inline template block with reference (4-backtick fence — special case)
- **FIND**: The `### 4.2 Artifact Template` section (~line 251) containing:
  ````
  ````markdown
  # Investigation: {Title}
  
  **Issue**: #{number} ({url})
  ...
  ````
  ````
  Block uses `` ````markdown `` (4 backticks) because the template content contains nested `` ``` `` blocks.
  The opening fence is `` ````markdown `` and the closing fence is `` ```` `` (4 backticks).
  Block runs approximately lines 262–343.
- **REPLACE** the entire fenced block (opening `` ````markdown `` through closing `` ```` ``) with:
  ```
  > **Output Template**: See `.github/PRPs/templates/prp-issue-investigate.prompt-artifact-template.md`
  > Load this file and use its structure exactly when generating output.
  ```
- **PRESERVE**: `### 4.2 Artifact Template` heading, `Write this structure to the artifact file.` instruction above, `**PHASE_4_CHECKPOINT:**` below
- **DO NOT TOUCH**: The Phase 7 `## Investigation Complete` output summary block (~line 549) — stays inline
- **GOTCHA**: The 4-backtick fence means both opening and closing fences use 4 backticks `` ```` ``, not 3. Be careful not to confuse with other code blocks in the file.
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-issue-investigate" .github/prompts/prp-issue-investigate.prompt.md
  # Expected: One line with the reference
  grep -c "# Investigation: {Title}" .github/prompts/prp-issue-investigate.prompt.md
  # Expected: 0
  grep -c "Investigation Complete" .github/prompts/prp-issue-investigate.prompt.md
  # Expected: 1 (Phase 7 summary stays inline)
  ```

---

### Task 8: UPDATE `prp-ralph.prompt.md` (2 replacements)

- **ACTION**: Replace 2 inline template blocks with references (both standard `` ```markdown `` fences)
- **REPLACEMENT A** — Setup message template (~line 124):
  - **FIND**: The `### 2.2 Display Startup Message` section containing:
    ```
    ```markdown
    ## PRP Ralph Loop Activated
    
    **Plan**: {file_path}
    ...
    ```
    ```
    Block runs approximately lines 124–149.
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-ralph.prompt-setup-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `### 2.2 Display Startup Message` heading above; `**PHASE_2_CHECKPOINT:**` below

- **REPLACEMENT B** — Iteration progress log template (~line 223):
  - **FIND**: The `### 3.8 Update State File Progress Log` section containing:
    ```
    Append to Progress Log section using this format:
    
    ```markdown
    ## Iteration {N} - {ISO timestamp}
    
    ### Completed
    ...
    ```
    ```
    Block runs approximately lines 223–246.
  - **REPLACE** the fenced block with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-ralph.prompt-progress-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `### 3.8 Update State File Progress Log` heading, `Append to Progress Log section using this format:` instruction above; `### 3.9 Consolidate Codebase Patterns` below

- **DO NOT TOUCH** (4 blocks in this file that stay inline):
  - State file YAML structure block (~line 88)
  - Codebase patterns example block (`## Codebase Patterns`) (~line 252)
  - Indented completion report block (~line 290)
  - Indented CLAUDE.md pattern block (~line 350)

- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-ralph.prompt" .github/prompts/prp-ralph.prompt.md
  # Expected: 2 lines (one for setup, one for progress)
  grep -c "PRP Ralph Loop Activated" .github/prompts/prp-ralph.prompt.md
  # Expected: 0
  grep -c "## Iteration {N}" .github/prompts/prp-ralph.prompt.md
  # Expected: 0
  ```

---

### Task 9: UPDATE `prp-codebase-question.prompt.md` (2 replacements)

- **ACTION**: Replace 2 inline template blocks with references
- **REPLACEMENT A** — Research document template (~line 222):
  - **FIND**: The `### 5.4 Write Research Document` section containing:
    ```
    ```markdown
    ---
    date: {ISO timestamp with timezone}
    git_commit: {short hash}
    ...
    ```
    ```
    Block runs approximately lines 222–275 (YAML frontmatter + full research structure, ~52 lines).
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-codebase-question.prompt-research-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `### 5.4 Write Research Document` heading above; `### 5.5 Add GitHub Permalinks` section below

- **REPLACEMENT B** — Output summary template (~line 309):
  - **FIND**: The `## Phase 6: OUTPUT - Present to User` section containing:
    ```
    ```markdown
    ## Research Complete
    
    **Question**: {original question}
    ...
    ```
    ```
    Block runs approximately lines 309–337.
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-codebase-question.prompt-summary-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 6: OUTPUT - Present to User` heading, surrounding `---` dividers, `## Usage Examples` section below

- **GOTCHA**: The file contains multiple `` ```markdown `` blocks (e.g., a smaller example block in `### 5.6 Handle Follow-ups`). Target only the two described above.
  - Research template: first content line is `---` (YAML frontmatter)
  - Summary template: first content line is `## Research Complete`
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-codebase-question" .github/prompts/prp-codebase-question.prompt.md
  # Expected: 2 lines
  grep -c "## Research Complete" .github/prompts/prp-codebase-question.prompt.md
  # Expected: 0
  grep -c "^date: {ISO timestamp" .github/prompts/prp-codebase-question.prompt.md
  # Expected: 0
  ```

---

### Task 10: UPDATE `prp-pr.prompt.md` (2 replacements)

- **ACTION**: Replace 2 inline template blocks with references — SPECIAL CASE for template A

- **REPLACEMENT A** — PR body template in bash heredoc (~line 181):
  - **FIND**: The `### 4.2 If No Template - Use Default Format` section containing the entire ` ```bash ` block:
    ````
    ```bash
    gh pr create \
      --title "{title}" \
      --base "{base-branch}" \
      --body "$(cat <<'EOF'
    ## Summary
    
    {1-2 sentence description of what this PR accomplishes}
    ...
    EOF
    )"
    ```
    ````
    Block runs approximately lines 181–217.
  - **REPLACE** the entire ` ```bash ` code block (opening ` ```bash ` through closing ` ``` `) with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-pr.prompt-pr-template.md`
    > Load this file and use its content as the `--body` value for `gh pr create`.
    ```
  - **PRESERVE**: `### 4.2 If No Template - Use Default Format` heading above; `### 4.3 Extract Issue References` section below

- **REPLACEMENT B** — Output summary template (~line 269):
  - **FIND**: The `## Phase 6: OUTPUT - Report to User` section containing:
    ```
    ```markdown
    ## Pull Request Created
    
    **PR**: #{number}
    ...
    ```
    ```
    Block runs approximately lines 269–298.
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-pr.prompt-summary-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 6: OUTPUT - Report to User` heading, surrounding `---` dividers, `## Handling Edge Cases` below

- **GOTCHA for A**: This is the only bash heredoc template in the codebase. The referenced template file has the PR body format. The reference note differs from the standard phrasing — use `use its content as the \`--body\` value` to preserve the action context.
- **GOTCHA**: Another ` ```bash ` block exists nearby that checks for `PULL_REQUEST_TEMPLATE.md` — do NOT touch that block.
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-pr" .github/prompts/prp-pr.prompt.md
  # Expected: 2 lines
  grep -c "Pull Request Created" .github/prompts/prp-pr.prompt.md
  # Expected: 0
  grep -c "1-2 sentence description of what this PR accomplishes" .github/prompts/prp-pr.prompt.md
  # Expected: 0
  ```

---

### Task 11: UPDATE `prp-prd.prompt.md` (2 replacements)

- **ACTION**: Replace 2 inline template blocks with references
- **REPLACEMENT A** — Full PRD file template (~line 221):
  - **FIND**: The `## Phase 7: GENERATE - Write PRD` section, after `### PRD Template` heading (~line 219):
    ```
    ```markdown
    # {Product/Feature Name}
    
    ## Problem Statement
    
    {2-3 sentences: Who has what problem...}
    ...
    ```
    ```
    Block runs approximately lines 221–373 (~153 lines).
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-prd.prompt-prd-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 7: GENERATE - Write PRD` heading, `**Output path**:` annotation, `### PRD Template` sub-heading above (keep the sub-heading as context); `---` and `## Phase 8: OUTPUT - Summary` below

- **REPLACEMENT B** — Output summary template (~line 381):
  - **FIND**: The `## Phase 8: OUTPUT - Summary` section containing:
    ```
    ```markdown
    ## PRD Created
    
    **File**: `.claude/PRPs/prds/{name}.prd.md`
    ...
    ```
    ```
    Block runs approximately lines 381–418.
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-prd.prompt-summary-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 8: OUTPUT - Summary` heading; `---` and `## Question Flow Summary` below

- **GOTCHA**: This is the second-largest file-template replacement at ~153 lines. Read the file carefully to confirm the fence boundaries before editing.
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-prd" .github/prompts/prp-prd.prompt.md
  # Expected: 2 lines
  grep -c "# {Product/Feature Name}" .github/prompts/prp-prd.prompt.md
  # Expected: 0
  grep -c "## PRD Created" .github/prompts/prp-prd.prompt.md
  # Expected: 0
  ```

---

### Task 12: UPDATE `prp-review.prompt.md` (2 replacements)

- **ACTION**: Replace 2 inline template blocks with references
- **REPLACEMENT A** — Full review report template (~line 336):
  - **FIND**: The `### 6.2 Generate Report File` section containing:
    ```
    **Path**: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`
    
    ```markdown
    ---
    pr: {NUMBER}
    title: "{TITLE}"
    ...
    ```
    ```
    Block runs approximately lines 336–420 (~99 lines with YAML frontmatter).
  - **REPLACE** the fenced block with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-review.prompt-report-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `### 6.2 Generate Report File` heading, `**Path**:` annotation above; `**PHASE_6_CHECKPOINT:**` below

- **REPLACEMENT B** — Output summary template (~line 478):
  - **FIND**: The `## Phase 8: OUTPUT - Report to User` section containing:
    ```
    ```markdown
    ## PR Review Complete
    
    **PR**: #{NUMBER} - {TITLE}
    ...
    ```
    ```
    Block runs approximately lines 478–518.
  - **REPLACE** with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-review.prompt-summary-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 8: OUTPUT - Report to User` heading; `---` and `## Critical Reminders` below

- **GOTCHA**: First template content line starts with `---` (YAML frontmatter for the review file). Confirm the fence opens immediately before `---`.
- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-review.prompt.md" .github/prompts/prp-review.prompt.md
  # Expected: 2 lines
  grep -c "PR Review Complete" .github/prompts/prp-review.prompt.md
  # Expected: 0
  grep -c "^pr: {NUMBER}" .github/prompts/prp-review.prompt.md
  # Expected: 0
  ```

---

### Task 13: UPDATE `prp-plan.prompt.md` (2 replacements — both special fence cases)

This is the most complex file. Read lines 236–298 (design template) and lines 350–695 (plan template) before making any edits.

- **REPLACEMENT A** — UX Design template (~line 240, plain ` ``` ` fence):
  - **FIND**: The `## Phase 4: DESIGN - UX Transformation` section, under `**CREATE ASCII diagrams showing user experience before and after:**`, the plain code fence block:
    ````
    ```
    ╔═══════════════════════════════════════════════════════════════════════════════╗
    ║                              BEFORE STATE                                      ║
    ...
    ╚═══════════════════════════════════════════════════════════════════════════════╝
    ```
    ````
    Block runs approximately lines 240–275 (plain fence, no language label).
    The block contains ONLY the ASCII box diagrams — the interaction table BELOW stays.
  - **REPLACE** the fenced block (plain ` ``` ` open through plain ` ``` ` close) with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-plan.prompt-design-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 4: DESIGN - UX Transformation` heading above; `**CREATE ASCII diagrams...:**` instruction above; `**DOCUMENT interaction changes:**` + interaction table + `**PHASE_4_CHECKPOINT:**` all below — these stay intact
  - **GOTCHA**: The plain ` ``` ` fence has NO language label. Do not accidentally target other ` ```bash ` or ` ```markdown ` fences nearby. The ASCII diagrams content starting with `╔═══` is the unique identifier.

- **REPLACEMENT B** — Full plan template (~line 358, 4-backtick `` ````markdown `` fence):
  - **FIND**: The `## Phase 6: GENERATE - Implementation Plan File` section, after `**PLAN_STRUCTURE** (the template to fill and save):` (~line 356), the 4-backtick code fence:
    `````
    ````markdown
    # Feature: {Feature Name}
    
    ## Summary
    
    {One paragraph: What we're building and high-level approach}
    ...
    ````
    `````
    The opening fence is `` ````markdown `` (4 backticks) and closing is `` ```` `` (4 backticks).
    Block runs approximately lines 358–691 (~334 lines — the largest replacement in this task set).
  - **REPLACE** the entire 4-backtick fenced block (opening `` ````markdown `` through closing `` ```` ``) with:
    ```
    > **Output Template**: See `.github/PRPs/templates/prp-plan.prompt-plan-template.md`
    > Load this file and use its structure exactly when generating output.
    ```
  - **PRESERVE**: `## Phase 6: GENERATE - Implementation Plan File` heading, `**OUTPUT_PATH**:` annotation, `Create directory if needed:` bash command, `**PLAN_STRUCTURE** (the template to fill and save):` instruction above; `</process>` closing tag and `<output>` block below
  - **GOTCHA**: The file has XML-like `<process>` and `<output>` tags. The 4-backtick block sits inside `<process>`. The `<output>` block (~line 695+) containing the `REPORT_TO_USER` summary stays intact — do NOT touch it.
  - **CRITICAL**: After replacement, the `</process>` tag should immediately follow with just a blank line after the blockquote reference.

- **VALIDATE**:
  ```bash
  grep -n "Output Template.*prp-plan" .github/prompts/prp-plan.prompt.md
  # Expected: 2 lines
  grep -c "# Feature: {Feature Name}" .github/prompts/prp-plan.prompt.md
  # Expected: 0
  grep -c "BEFORE STATE" .github/prompts/prp-plan.prompt.md
  # Expected: 0 (ASCII diagrams now only in template file)
  # Confirm process/output tags are intact:
  grep -c "</process>" .github/prompts/prp-plan.prompt.md
  # Expected: 1
  grep -c "<output>" .github/prompts/prp-plan.prompt.md
  # Expected: 1
  ```

---

## Testing Strategy

### Unit Tests to Write

None — this is a pure markdown refactoring task with no executable code. Validation is via grep/file checks.

### Edge Cases Checklist

- [ ] `prp-ralph-cancel.prompt.md`: indented fence replaced correctly, blockquote is flush-left (not indented)
- [ ] `prp-issue-investigate.prompt.md`: 4-backtick opening AND closing fence both removed
- [ ] `prp-plan.prompt.md` REPLACEMENT A: plain fence replaced; interaction table and DOCUMENT instruction preserved
- [ ] `prp-plan.prompt.md` REPLACEMENT B: 4-backtick fence removed; `</process>` and `<output>` tags intact
- [ ] `prp-pr.prompt.md` REPLACEMENT A: entire `bash` block replaced (not just the heredoc body)
- [ ] `prp-debug.prompt.md`: Phase 6 `Root Cause Analysis Complete` block preserved
- [ ] `prp-implement.prompt.md`: Phase 6 `Implementation Complete` block preserved
- [ ] `prp-issue-investigate.prompt.md`: Phase 7 `Investigation Complete` block preserved
- [ ] No template files in `.github/PRPs/templates/` were modified

---

## Validation Commands

### Level 1: REFERENCE COUNT VERIFICATION

```bash
# Count prompts that now contain the Output Template reference
# Expected: 13 (all prompts)
grep -l "Output Template" .github/prompts/*.prompt.md | wc -l

# Count total Output Template references across all prompts
# Expected: 19 (one per extracted template)
grep -r "Output Template" .github/prompts/*.prompt.md | wc -l
```

**EXPECT**: `13` for prompts with references; `19` for total reference count

### Level 2: INLINE TEMPLATE ELIMINATION (per-prompt spot checks)

```bash
# These should all return 0 — content that was extracted must no longer be inline
grep -r "# Feature: {Feature Name}" .github/prompts/
grep -r "# Root Cause Analysis$" .github/prompts/
grep -r "# Implementation Report$" .github/prompts/
grep -r "# Investigation: {Title}" .github/prompts/
grep -r "PRP Ralph Loop Activated" .github/prompts/
grep -r "## PRD Created" .github/prompts/
grep -r "## Research Complete" .github/prompts/
grep -r "## PR Review Summary" .github/prompts/
grep -r "## PR Review Complete" .github/prompts/
grep -r "## Pull Request Created" .github/prompts/
```

**EXPECT**: 0 matches for each command

### Level 3: PRESERVED CONTENT VERIFICATION (blocks that must NOT be removed)

```bash
# These stay inline and must still be present
grep -c "Root Cause Analysis Complete" .github/prompts/prp-debug.prompt.md
# Expected: 1

grep -c "## Implementation Complete" .github/prompts/prp-implement.prompt.md
# Expected: 1 (Phase 6 output summary stays)

grep -c "Investigation Complete" .github/prompts/prp-issue-investigate.prompt.md
# Expected: 1 (Phase 7 output summary stays)

grep -c "</process>" .github/prompts/prp-plan.prompt.md
# Expected: 1 (XML tag intact)

grep -c "<output>" .github/prompts/prp-plan.prompt.md
# Expected: 1 (output block intact)
```

**EXPECT**: All return the expected count

### Level 4: TEMPLATE FILES UNCHANGED

```bash
# All 19 template files must still exist and be unmodified
ls .github/PRPs/templates/*.template.md | wc -l
# Expected: 19

# Line count spot check — template contents must not be altered
wc -l .github/PRPs/templates/prp-plan.prompt-plan-template.md
# Expected: ~331 lines
wc -l .github/PRPs/templates/prp-codebase-question.prompt-research-template.md
# Expected: ~52 lines
```

**EXPECT**: 19 files exist; line counts match pre-task values

### Level 5: STRUCTURAL INTEGRITY

```bash
# No broken markdown fences (unmatched backtick blocks)
# Run a basic fence-balance check on the most complex edited file
python -c "
content = open('.github/prompts/prp-plan.prompt.md').read()
triple = content.count('\`\`\`')
quad = content.count('\`\`\`\`')
print(f'3-backtick fences: {triple} (should be even)')
print(f'4-backtick fences: {quad} (should be even)')
print('OK' if triple % 2 == 0 and quad % 2 == 0 else 'WARNING: unmatched fences')
"
```

**EXPECT**: Both fence counts are even (no unmatched fences)

---

## Acceptance Criteria

- [ ] All 13 prompt files contain at least one `> **Output Template**:` reference
- [ ] Total of 19 `Output Template` references across all prompts
- [ ] No extracted template content remains embedded inline in prompts
- [ ] All preserved "stay-inline" blocks (`Root Cause Analysis Complete`, `Implementation Complete`, `Investigation Complete`, `REPORT_TO_USER` output block, Ralph state YAML, etc.) are untouched
- [ ] All 19 template files in `.github/PRPs/templates/` are unmodified
- [ ] `prp-plan.prompt.md` structural tags (`</process>`, `<output>`) are intact
- [ ] Level 1–5 validation commands all pass

---

## Completion Checklist

- [ ] All 13 tasks completed in order
- [ ] Each task validated immediately after completion with the per-task validate commands
- [ ] Level 1: Reference count verification passes (13 prompts, 19 references)
- [ ] Level 2: All inline template content eliminated (grep returns 0)
- [ ] Level 3: All preserved blocks still present
- [ ] Level 4: Template files unchanged (19 files, correct line counts)
- [ ] Level 5: No unmatched markdown fences
- [ ] PRD phase 3 status updated to `complete`

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|----|--------|------|-----------|
| Accidentally removing surrounding instruction text | MED | HIGH | Use minimal-scope replacements: replace only the fenced block, never the heading or annotations above/below |
| 4-backtick fence incorrectly matched | MED | HIGH | Identify 4-backtick blocks by unique content (first line: `# Feature:` or `# Investigation:`), not just fence type |
| prp-plan.prompt.md plain fence confused with other fences | MED | MED | Identify by unique content: `╔═══` ASCII box diagrams |
| prp-pr.prompt.md bash block partial replacement | LOW | HIGH | Replace entire `\`\`\`bash` block (not just heredoc body) as defined in Task 10 |
| Preserved "stay-inline" blocks accidentally removed | LOW | HIGH | Run Level 3 validation after every file edit |
| Template files accidentally modified | LOW | HIGH | Do not open template files for editing; run Level 4 check after all tasks |

---

## Notes

**Implementation order rationale**: Tasks 1–7 are single-replacement edits per file (simpler);
Tasks 8–13 are dual-replacement edits. This ordering builds confidence before tackling the complex files.

**Parallelism**: All 13 tasks are independent of each other (no ordering dependencies between files).
If running sub-agents, all 13 prompts could be updated concurrently. However, sequential execution
with immediate per-task validation is recommended to catch errors early.

**Why no external research**: This task is pure markdown file editing — no library API, no runtime
environment, no tooling changes. All required context is in the codebase.

**Reference phrasing variation**: Task 10 (prp-pr.prompt.md, Replacement A) uses a modified
reference phrase to preserve the bash `gh pr create` action context. All other 18 replacements
use the standard phrasing: `Load this file and use its structure exactly when generating output.`
