# Feature: {Feature Name}

## Summary

{One paragraph: What we're building and high-level approach}

## User Story

As a {user type}
I want to {action}
So that {benefit}

## Problem Statement

{Specific problem this solves - must be testable}

## Solution Statement

{How we're solving it - architecture overview}

## Metadata

| Field | Value |
| --- | --- |
| Type | NEW_CAPABILITY / ENHANCEMENT / REFACTOR / BUG_FIX |
| Complexity | LOW / MEDIUM / HIGH |
| Systems Affected | {comma-separated list} |
| Dependencies | {external libs/services with versions} |
| Estimated Tasks | {count} |
| Source PRD | {prd-file-path or N/A} |

---

## UX Design

### Interaction Changes

| Location | Before | After | User Impact |
| --- | --- | --- | --- |
| {path/component} | {old behavior} | {new behavior} | {what changes for user} |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
| --- | --- | --- | --- |
| P0 | `path/to/critical/module` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types/definitions` | 1-30 | Types/interfaces to IMPORT |
| P2 | `path/to/tests/example` | all | Test pattern to FOLLOW |

**External Documentation:**
| Source | Section | Why Needed |
| --- | --- | --- |
| [Lib Docs v{version}](url#anchor) | {section name} | {specific reason} |

---

## Patterns to Mirror

<!--
  PATTERN_NAME_N: An actual pattern from this codebase in all caps with underscores, e.g., (NAMING_CONVENTION, ERROR_HANDLING, LOGGING_PATTERN, etc.)
-->

**{PATTERN_NAME_1}:**

```{language}
// SOURCE: path/to/source/file1:10-15
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**{PATTERN_NAME_2}:**

```{language}
// SOURCE: path/to/source/file2:5-20
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

---

## Files to Change

| File | Action | Justification |
| --- | --- | --- |
| `{source-dir}/{feature}/models.{ext}` | CREATE | Data models / type definitions |
| `{source-dir}/{feature}/service.{ext}` | CREATE | Business logic |
| `{source-dir}/{feature}/tests/test_{feature}.{ext}` | CREATE | Unit tests |
| `{source-dir}/{config-file}` | UPDATE | Register new module |

{verbatim: This table is a map only -- all execution details are in tasks below.}

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- {Item 1 - explicitly out of scope and why}
- {Item 2 - explicitly out of scope and why}

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

<!--
  TASK_FIELDS: Use only the fields relevant to each task.
  Required: ACTION, IMPLEMENT, VALIDATE
  Optional: MIRROR, IMPORTS, GOTCHA, TYPES (language-specific), PATTERN
-->

### Task 1: {ACTION} `{path/to/file.ext}`

- **ACTION**: CREATE / UPDATE / DELETE
- **IMPLEMENT**: {What to build or change — data structures, logic, behavior}
- **MIRROR**: `{path/to/similar/existing/file.ext}:{start}-{end}`
- **IMPORTS**: `{import statement for this language}`
- **GOTCHA**: {Known pitfall for this task}
- **VALIDATE**: `{validation-cmd-from-Validation-Commands-section}`

### Task 2: {ACTION} `{path/to/file.ext}`

- **ACTION**: CREATE / UPDATE / DELETE
- **IMPLEMENT**: {What to build}
- **MIRROR**: `{path/to/similar/existing/file.ext}:{start}-{end}`
- **VALIDATE**: `{validation-cmd-from-Validation-Commands-section}`
- **PATTERN**: {Codebase or custom pattern to follow}

---

## Testing Strategy

### Unit Tests to Write

<!--
  Adapt test file naming/paths to the project's test conventions
  (e.g., tests/test_feature.py, src/feature/__tests__/service.test.ts, feature_test.go)
-->

| Test File | Test Cases | Validates |
|---|---|---|
| `{tests-dir}/test_{feature}.{ext}` | happy path, error cases | Core business logic |
| `{tests-dir}/test_{feature}_edge.{ext}` | boundary inputs, missing fields | Input validation |

### Edge Cases Checklist

- [ ] Empty string inputs
- [ ] Missing required fields
- [ ] Unauthorized access attempts
- [ ] Not found scenarios
- [ ] Duplicate creation attempts
- [ ] {feature-specific edge case}

---

## Validation Commands

**IMPORTANT**: Replace these placeholders with actual commands from the project's package.json/config.

### Level 1: STATIC_ANALYSIS

```bash
{runner} run lint && {runner} run type-check
# Examples: npm run lint, pnpm lint, ruff check . && mypy ., cargo clippy
```

**EXPECT**: Exit 0, no errors or warnings

### Level 2: UNIT_TESTS

```bash
{runner} test {path/to/feature/tests}
# Examples: npm test, pytest tests/, cargo test, go test ./...
```

**EXPECT**: All tests pass, coverage >= 80%

### Level 3: FULL_SUITE

```bash
{runner} test && {runner} run build
# Examples: npm test && npm run build, cargo test && cargo build
```

**EXPECT**: All tests pass, build succeeds

### Level 4: DATABASE_VALIDATION (if schema changes) (OPTIONAL: if project has database)

Use Supabase MCP to verify:

- [ ] Table created with correct columns
- [ ] RLS policies applied
- [ ] Indexes created

### Level 5: BROWSER_VALIDATION (if UI changes) (OPTIONAL: if project has browser-based UI)

Use Browser MCP to verify:

- [ ] UI renders correctly
- [ ] User flows work end-to-end
- [ ] Error states display properly

### Level 6: MANUAL_VALIDATION

{Step-by-step manual testing specific to this feature}

---

## Acceptance Criteria

- [ ] All specified functionality implemented per user story
- [ ] Level 1-3 validation commands pass with exit 0
- [ ] Unit tests cover >= 80% of new code
- [ ] Code mirrors existing patterns exactly (naming, structure, logging)
- [ ] No regressions in existing tests
- [ ] UX matches "After State" diagram

---

## Completion Checklist

- [ ] All tasks completed in dependency order
- [ ] Each task validated immediately after completion
- [ ] Level 1: Static analysis (lint + type-check) passes
- [ ] Level 2: Unit tests pass
- [ ] Level 3: Full test suite + build succeeds
- [ ] Level 4: Database validation passes (if applicable)
- [ ] Level 5: Browser validation passes (if applicable)
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| {Risk description} | LOW/MED/HIGH | LOW/MED/HIGH | {Specific prevention/handling strategy} |

---

## Notes

{Additional context, design decisions, trade-offs, future considerations}
