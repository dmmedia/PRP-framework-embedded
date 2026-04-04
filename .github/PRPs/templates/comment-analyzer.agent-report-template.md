## Comment Analysis: [Scope Description]

### Scope
- **Analyzing**: [git diff / specific files / PR diff]
- **Files**: [list of files with comments]
- **Comment count**: [N comments analyzed]

---

### Critical Issues (Must Fix)

Factually incorrect or highly misleading comments.

#### Issue 1: [Brief Title]
**Location**: `path/to/file.ts:45-52`
**Type**: Inaccurate / Misleading / Outdated

**Current Comment**:
```typescript
/**
 * Returns the user's full name
 */
```

**Actual Behavior**:
The function returns only the first name, not the full name.

**Evidence**: Line 48 returns `user.firstName` only.

**Suggested Fix**:

```typescript
/**
 * Returns the user's first name
 */
```

---

### Improvement Opportunities

Comments that would benefit from enhancement.

#### Opportunity 1: [Brief Title]

**Location**: `path/to/file.ts:78-85`
**Issue**: Missing error handling documentation

**Current Comment**:

```typescript
/**
 * Fetches user data from the API
 */
```

**Suggested Enhancement**:

```typescript
/**
 * Fetches user data from the API
 * @throws {NetworkError} When the API is unreachable
 * @throws {AuthError} When the token is invalid
 */
```

---

### Recommended Removals

Comments that add no value or create confusion.

#### Removal 1: [Brief Title]

**Location**: `path/to/file.ts:102`

**Current Comment**:

```typescript
// increment counter
counter++;
```

**Rationale**: Restates obvious code. The code is self-explanatory.

---

### Stale Markers

TODOs, FIXMEs, and similar markers that need attention.

| Location | Marker | Status | Recommendation |
|----------|--------|--------|----------------|
| `file.ts:23` | `// TODO: add validation` | May be done | Verify and remove if complete |
| `file.ts:89` | `// FIXME: race condition` | Unclear | Investigate current state |

---

### Positive Examples

Well-written comments that serve as good patterns.

#### Example 1: [Brief Title]

**Location**: `path/to/file.ts:120-128`

**Why It's Good**:

- Explains the "why" not just the "what"
- Captures non-obvious business logic
- Will remain accurate as code evolves

```typescript
/**
 * Rate limiting uses a sliding window algorithm instead of fixed windows
 * to prevent burst traffic at window boundaries. This matches the behavior
 * expected by our API gateway.
 */
```

---

### Summary

| Category | Count |
|----------|-------|
| Critical Issues | X |
| Improvements | Y |
| Removals | Z |
| Stale Markers | W |
| Positive Examples | V |

**Overall Assessment**: [GOOD / NEEDS ATTENTION / SIGNIFICANT ISSUES]

**Priority Actions**:

1. [First thing to fix]
2. [Second thing to fix]
