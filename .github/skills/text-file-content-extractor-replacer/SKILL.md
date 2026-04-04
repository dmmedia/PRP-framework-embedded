---
name: text-file-content-extractor-replacer
description: Extract a line-range content block from a text file into a new file, replace a line-range content block in a text file with new agent-provided content, or do both in sequence. Uses shell utilities (PowerShell on Windows, sed/bash on macOS/Linux). Requires exact start and end line numbers identified before execution.
---

# Text File Content Extractor / Replacer

## Overview

Three operating modes — choose the one that fits the task:

| Mode | What it does |
|---|---|
| `extract` | Copy lines START–END verbatim to a new file; source file is unchanged |
| `replace` | Substitute lines START–END in the source file with new content |
| `extract-and-replace` | Extract first (preserves the original block), then replace |

## Prerequisites

Confirm before running any command:

- Absolute or relative path to the **source file**
- **Start line** and **end line** (1-based, inclusive) — identify these precisely using a file-reading tool before touching any file
- For `extract` or `extract-and-replace`: path for the **destination file** (the extracted block)
- For `replace` or `extract-and-replace`: the **new content** to write in place of the removed block

## Step 1 — Identify the Line Range

Use file-reading tools to read the candidate range. Visually confirm:

- Line `start` is the first line of the block (nothing above it belongs to the block)
- Line `end` is the last line of the block (nothing below it belongs to the block)

Spot-check `start - 1` and `end + 1` to verify the boundaries are correct before any write operation.

## Step 2a — Extract (modes: `extract`, `extract-and-replace`)

**Windows (PowerShell):**

```powershell
$src   = "path\to\source.txt"
$dest  = "path\to\extracted.txt"
$start = <START_LINE>   # 1-based
$end   = <END_LINE>     # 1-based, inclusive

(Get-Content $src)[($start - 1)..($end - 1)] | Set-Content $dest -Encoding utf8
```

**macOS / Linux (bash):**

```bash
src="path/to/source.txt"
dest="path/to/extracted.txt"
start=<START_LINE>
end=<END_LINE>

sed -n "${start},${end}p" "$src" > "$dest"
```

Verify: `$dest` (or `$dest`) exists and its content matches the expected block exactly.

## Step 2b — Replace (modes: `replace`, `extract-and-replace`)

Write the new content to a temporary file or prepare it as an in-memory array, then splice it into the source file.

**Windows (PowerShell) — new content as an array:**

```powershell
$src      = "path\to\source.txt"
$start    = <START_LINE>      # 1-based
$end      = <END_LINE>        # 1-based, inclusive

# Build $newBlock as an array of strings — one element per line
$newBlock = @(
    "first line of new content",
    "second line of new content"
)

$lines  = Get-Content $src
$before = if ($start -gt 1)            { $lines[0..($start - 2)] } else { @() }
$after  = if ($end -lt $lines.Count)   { $lines[$end..($lines.Count - 1)] } else { @() }

($before + $newBlock + $after) | Set-Content $src -Encoding utf8
```

**Windows (PowerShell) — new content from a file:**

```powershell
$src      = "path\to\source.txt"
$newFile  = "path\to\new_content.txt"
$start    = <START_LINE>
$end      = <END_LINE>

$lines    = Get-Content $src
$before   = if ($start -gt 1)           { $lines[0..($start - 2)] } else { @() }
$after    = if ($end -lt $lines.Count)  { $lines[$end..($lines.Count - 1)] } else { @() }
$newBlock = Get-Content $newFile

($before + $newBlock + $after) | Set-Content $src -Encoding utf8
```

**macOS / Linux (bash) — new content from a file:**

```bash
src="path/to/source.txt"
new_content="path/to/new_content.txt"
start=<START_LINE>
end=<END_LINE>

tmp=$(mktemp)
{
  [ "$start" -gt 1 ] && head -n $(( start - 1 )) "$src"
  cat "$new_content"
  tail -n +$(( end + 1 )) "$src"
} > "$tmp" && mv "$tmp" "$src"
```

**macOS / Linux (bash) — new content inline (small blocks):**

```bash
src="path/to/source.txt"
start=<START_LINE>
end=<END_LINE>

tmp=$(mktemp)
{
  [ "$start" -gt 1 ] && head -n $(( start - 1 )) "$src"
  cat <<'EOF'
first line of new content
second line of new content
EOF
  tail -n +$(( end + 1 )) "$src"
} > "$tmp" && mv "$tmp" "$src"
```

Verify: the source file now contains the new content at the correct position, and all lines outside the replaced range are unchanged.

## Safety Rules

1. **Never guess line numbers** — always read and confirm the range with a tool before writing.
2. **Check the file line count first** to ensure `start` and `end` are within bounds:
   - PowerShell: `(Get-Content $src).Count`
   - bash: `wc -l < "$src"`
3. **Never overwrite the destination file** of an extraction without explicit user confirmation if the file already exists.
4. For `replace` and `extract-and-replace`, the source file is modified in-place. If the content is valuable, prefer `extract-and-replace` so the original block is preserved in the destination file before the source is altered.

## Examples

### Extract-only

```text
Source : firmware/config.c, lines 45–78 (a static lookup table)
Dest   : firmware/lookup_table.c
Mode   : extract
```

```powershell
(Get-Content "firmware\config.c")[44..77] | Set-Content "firmware\lookup_table.c" -Encoding utf8
```

---

### Replace-only

```text
Source      : docs/api.md, lines 10–25 (outdated parameter table)
New content : updated markdown table provided by the agent
Mode        : replace
```

```powershell
$lines    = Get-Content "docs\api.md"
$newBlock = @("| Param | Type | Description |", "|---|---|---|", "| id | int | Resource ID |")
$before   = $lines[0..8]
$after    = $lines[25..($lines.Count - 1)]
($before + $newBlock + $after) | Set-Content "docs\api.md" -Encoding utf8
```

---

### Extract-and-replace

```text
Source : main.c, lines 100–150 (interrupt handler implementation)
Dest   : interrupt_handler.c
Replace with : #include "interrupt_handler.c"
Mode   : extract-and-replace
```

1. Run Step 2a to copy lines 100–150 from `main.c` into `interrupt_handler.c`.
2. Run Step 2b to replace lines 100–150 in `main.c` with `#include "interrupt_handler.c"`.

## When to Use

Use this skill when:

- Splitting a large file into smaller, focused files
- Archiving an unchanged content block before rewriting it
- Replacing boilerplate or generated sections in source files with fresh output
- Any workflow requiring surgical, line-range-targeted modification of a text file

Do **not** use this skill when:

- The line boundaries are uncertain — identify exact lines first, then invoke this skill
- Modifying binary files
- Doing project-wide pattern-based search-and-replace (use `grep`/`sed` with patterns instead)
