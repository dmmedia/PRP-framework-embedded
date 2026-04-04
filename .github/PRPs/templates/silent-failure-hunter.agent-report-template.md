## Silent Failure Hunt: [PR/Scope Description]

### Scope

- **Reviewing**: [PR diff / specific files]
- **Error handlers found**: [N locations]
- **Files with error handling**: [list]

---

### Critical Issues (Must Fix)

Silent failures and catch-all blocks that must be fixed.

#### Issue 1: [Brief Title]

**Severity**: CRITICAL
**Location**: `path/to/file.ts:45-52`
**Pattern**: Empty catch block / Broad exception catch / Silent fallback

**Current Code**:

```typescript
try {
  await saveData(data);
} catch (e) {
  // do nothing
}
```

**Hidden Errors**: This could silently swallow:

- Network failures
- Permission errors
- Disk full errors
- Serialization errors
- Any unexpected runtime error

**User Impact**: User thinks save succeeded. Data is lost. No way to debug.

**Required Fix**:

```typescript
try {
  await saveData(data);
} catch (error) {
  logError('Failed to save data', { error, dataId: data.id });
  showUserError('Could not save your changes. Please try again or check your connection.');
  throw error; // Or handle appropriately
}
```

---

#### Issue 2: [Brief Title]

**Severity**: CRITICAL
**Location**: `path/to/file.ts:78-85`
**Pattern**: [Pattern type]

**Current Code**:

```typescript
// problematic code
```

**Hidden Errors**: [List what could be hidden]

**User Impact**: [How this affects users]

**Required Fix**:

```typescript
// corrected code
```

---

### High Severity Issues

Inadequate error messages and unjustified fallbacks.

#### Issue 3: [Brief Title]

**Severity**: HIGH
**Location**: `path/to/file.ts:102`
**Pattern**: Poor error message / Unjustified fallback

**Problem**: [Description]

**User Impact**: [How this affects users]

**Required Fix**: [Specific change needed]

---

### Medium Severity Issues

Missing context and specificity improvements.

#### Issue 4: [Brief Title]

**Severity**: MEDIUM
**Location**: `path/to/file.ts:120`
**Pattern**: Missing context / Could be more specific

**Problem**: [Description]

**Suggested Improvement**: [What to add]

---

### Positive Findings

Error handling done well (acknowledge good patterns).

- **`file.ts:200-215`**: Excellent error handling with specific catch, good logging, and actionable user message
- **`other.ts:45`**: Proper error propagation to higher-level handler

---

### Summary

| Severity | Count | Action |
|---|---|---|
| CRITICAL | X | Must fix before merge |
| HIGH | Y | Should fix before merge |
| MEDIUM | Z | Improve when possible |

### Verdict: [PASS / NEEDS FIXES / CRITICAL ISSUES]

[If CRITICAL ISSUES: This PR has silent failures that will cause debugging nightmares. Do not merge until fixed.]
