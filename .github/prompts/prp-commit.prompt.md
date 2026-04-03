---
description: Quick commit with natural language file targeting
argument-hint: [target description] (blank = all changes)
---

# Commit

**Target**: $ARGUMENTS

---

## Your Mission

Stage files matching the target, write a concise commit message, commit.

---

## Phase 1: ASSESS

```bash
git status --short
```

If nothing to commit, stop.

---

## Phase 2: INTERPRET & STAGE

**Target interpretation:**

| Input | Action |
|-------|--------|
| (blank) | `git add -A` (all changes) |
| `staged` | Use current staging |
| `*.ts` / `typescript files` | `git add "*.ts"` |
| `files in src/X` | `git add src/X/` |
| `except tests` | Add all, then `git reset *test* *spec*` |
| `only new files` | Add only untracked files |
| `the X changes` | Interpret from diff/context |

Stage the matching files. Show what will be committed:

```bash
git diff --cached --name-only
```

---

## Phase 3: COMMIT

Write a single-line message in imperative mood:

```text
{type}: {description}
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

```bash
git commit -m "{type}: {description}"
```

---

## Phase 4: OUTPUT

> **Output Template**: See `.github/PRPs/templates/prp-commit.prompt-output-template.md`
> Load this file and use its structure exactly when generating output.

---

## Examples

```text
/prp-commit                          # All changes
/prp-commit typescript files         # *.ts only
/prp-commit except package-lock      # Exclude specific
/prp-commit only the new files       # Untracked only
/prp-commit staged                   # Already-staged only
```
