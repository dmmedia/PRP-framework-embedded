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
| ---------------- | ------------------------------------------------- |
| Type | NEW_CAPABILITY / ENHANCEMENT / REFACTOR / BUG_FIX |
| Complexity | LOW / MEDIUM / HIGH |
| Systems Affected | {comma-separated list} |
| Dependencies | {external libs/services with versions} |
| Estimated Tasks | {count} |

---

## UX Design

### Before State

```text

{ASCII diagram - current user experience with data flows}

```

### After State

```text

{ASCII diagram - new user experience with data flows}

```

### Interaction Changes

| Location | Before | After | User Impact |
|---|---|---|---|
| {path/component} | {old behavior} | {new behavior} | {what changes for user} |

---

## Mandatory Reading

**CRITICAL: Implementation agent MUST read these files before starting any task:**

| Priority | File | Lines | Why Read This |
|---|---|---|---|
| P0 | `path/to/critical.ts` | 10-50 | Pattern to MIRROR exactly |
| P1 | `path/to/types.ts` | 1-30 | Types to IMPORT |
| P2 | `path/to/test.ts` | all | Test pattern to FOLLOW |

**External Documentation:**
| Source | Section | Why Needed |
|---|---|---|
| [Lib Docs v{version}](url#anchor) | {section name} | {specific reason} |

---

## Patterns to Mirror

**NAMING_CONVENTION:**

```typescript
// SOURCE: src/features/example/service.ts:10-15
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**ERROR_HANDLING:**

```typescript
// SOURCE: src/features/example/errors.ts:5-20
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**LOGGING_PATTERN:**

```typescript
// SOURCE: src/features/example/service.ts:25-30
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**REPOSITORY_PATTERN:**

```typescript
// SOURCE: src/features/example/repository.ts:10-40
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**SERVICE_PATTERN:**

```typescript
// SOURCE: src/features/example/service.ts:40-80
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

**TEST_STRUCTURE:**

```typescript
// SOURCE: src/features/example/tests/service.test.ts:1-25
// COPY THIS PATTERN:
{actual code snippet from codebase}
```

---

## Files to Change

| File | Action | Justification |
| -------------------------------- | ------ | ---------------------------------------- |
| `src/features/new/models.ts` | CREATE | Type definitions - re-export from schema |
| `src/features/new/schemas.ts` | CREATE | Zod validation schemas |
| `src/features/new/errors.ts` | CREATE | Feature-specific errors |
| `src/features/new/repository.ts` | CREATE | Database operations |
| `src/features/new/service.ts` | CREATE | Business logic |
| `src/features/new/index.ts` | CREATE | Public API exports |
| `src/core/database/schema.ts` | UPDATE | Add table definition |

---

## NOT Building (Scope Limits)

Explicit exclusions to prevent scope creep:

- {Item 1 - explicitly out of scope and why}
- {Item 2 - explicitly out of scope and why}

---

## Step-by-Step Tasks

Execute in order. Each task is atomic and independently verifiable.

### Task 1: CREATE `src/core/database/schema.ts` (update)

- **ACTION**: ADD table definition to schema
- **IMPLEMENT**: {specific columns, types, constraints}
- **MIRROR**: `src/core/database/schema.ts:XX-YY` - follow existing table pattern
- **IMPORTS**: `import { pgTable, text, timestamp } from "drizzle-orm/pg-core"`
- **GOTCHA**: {known issue to avoid, e.g., "use uuid for id, not serial"}
- **VALIDATE**: `npx tsc --noEmit` - types must compile

### Task 2: CREATE `src/features/new/models.ts`

- **ACTION**: CREATE type definitions file
- **IMPLEMENT**: Re-export table, define inferred types
- **MIRROR**: `src/features/projects/models.ts:1-10`
- **IMPORTS**: `import { things } from "@/core/database/schema"`
- **TYPES**: `type Thing = typeof things.$inferSelect`
- **GOTCHA**: Use `$inferSelect` for read types, `$inferInsert` for write
- **VALIDATE**: `npx tsc --noEmit`

### Task 3: CREATE `src/features/new/schemas.ts`

- **ACTION**: CREATE Zod validation schemas
- **IMPLEMENT**: CreateThingSchema, UpdateThingSchema
- **MIRROR**: `src/features/projects/schemas.ts:1-30`
- **IMPORTS**: `import { z } from "zod/v4"` (note: zod/v4 not zod)
- **GOTCHA**: z.record requires two args in v4
- **VALIDATE**: `npx tsc --noEmit`

### Task 4: CREATE `src/features/new/errors.ts`

- **ACTION**: CREATE feature-specific error classes
- **IMPLEMENT**: ThingNotFoundError, ThingAccessDeniedError
- **MIRROR**: `src/features/projects/errors.ts:1-40`
- **PATTERN**: Extend base Error, include code and statusCode
- **VALIDATE**: `npx tsc --noEmit`

### Task 5: CREATE `src/features/new/repository.ts`

- **ACTION**: CREATE database operations
- **IMPLEMENT**: findById, findByUserId, create, update, delete
- **MIRROR**: `src/features/projects/repository.ts:1-60`
- **IMPORTS**: `import { db } from "@/core/database/client"`
- **GOTCHA**: Use `results[0]` pattern, not `.first()` - check noUncheckedIndexedAccess
- **VALIDATE**: `npx tsc --noEmit`

### Task 6: CREATE `src/features/new/service.ts`

- **ACTION**: CREATE business logic layer
- **IMPLEMENT**: createThing, getThing, updateThing, deleteThing
- **MIRROR**: `src/features/projects/service.ts:1-80`
- **PATTERN**: Use repository, add logging, throw custom errors
- **IMPORTS**: `import { getLogger } from "@/core/logging"`
- **VALIDATE**: `{type-check-cmd} && {lint-cmd}`

### Task 7: CREATE `{source-dir}/features/new/index.ts`

- **ACTION**: CREATE public API exports
- **IMPLEMENT**: Export types, schemas, errors, service functions
- **MIRROR**: `{source-dir}/features/{example}/index.ts:1-20`
- **PATTERN**: Named exports only, hide repository (internal)
- **VALIDATE**: `{type-check-cmd}`

### Task 8: CREATE `{source-dir}/features/new/tests/service.test.ts`

- **ACTION**: CREATE unit tests for service
- **IMPLEMENT**: Test each service function, happy path + error cases
- **MIRROR**: `{source-dir}/features/{example}/tests/service.test.ts:1-100`
- **PATTERN**: Use project's test framework (jest, vitest, bun:test, pytest, etc.)
- **VALIDATE**: `{test-cmd} {path-to-tests}`

---

## Testing Strategy

### Unit Tests to Write

| Test File | Test Cases | Validates |
| ---------------------------------------- | -------------------------- | -------------- |
| `src/features/new/tests/schemas.test.ts` | valid input, invalid input | Zod schemas |
| `src/features/new/tests/errors.test.ts` | error properties | Error classes |
| `src/features/new/tests/service.test.ts` | CRUD ops, access control | Business logic |

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

### Level 4: DATABASE_VALIDATION (if schema changes)

Use Supabase MCP to verify:

- [ ] Table created with correct columns
- [ ] RLS policies applied
- [ ] Indexes created

### Level 5: BROWSER_VALIDATION (if UI changes)

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
| ------------------ | ------------ | ------------ | --------------------------------------- |
| {Risk description} | LOW/MED/HIGH | LOW/MED/HIGH | {Specific prevention/handling strategy} |

---

## Notes

{Additional context, design decisions, trade-offs, future considerations}
