## Test Coverage Analysis: [PR Title/Number]

### Scope

- **PR**: [PR number or description]
- **Files changed**: [N files]
- **Test files**: [N test files added/modified]

---

### Summary

[2-3 sentence overview of test coverage quality]

**Overall Assessment**: [GOOD / ADEQUATE / NEEDS WORK / CRITICAL GAPS]

---

### Critical Gaps (Rating 8-10)

Tests that must be added before merge.

#### Gap 1: [Title]

**Rating**: 9/10
**Location**: `path/to/file.ts:45-60`
**Risk**: [What could break without this test]

**Untested Scenario**:
[Description of what's not covered]

**Why Critical**:
[Specific failure or bug this would catch]

**Suggested Test**:

```typescript
it('should reject invalid input with specific error', () => {
  // Test outline
  expect(() => validateInput(null)).toThrow(ValidationError);
});
```

---

### Important Improvements (Rating 5-7)

Tests that should be considered.

#### Improvement 1: [Title]

**Rating**: 6/10
**Location**: `path/to/file.ts:78`
**Risk**: [What could go wrong]

**Missing Coverage**:
[What scenario isn't tested]

**Suggested Test**:

```typescript
it('should handle empty array gracefully', () => {
  // Test outline
});
```

---

### Test Quality Issues

Existing tests that could be improved.

#### Issue 1: [Title]

**Location**: `path/to/file.test.ts:23-45`
**Problem**: Tests implementation details, will break on refactor

**Current Test**:

```typescript
// Tests internal method directly
expect(service._internalMethod()).toBe(true);
```

**Suggested Refactor**:

```typescript
// Test behavior instead
expect(service.publicMethod()).toMatchObject({ status: 'success' });
```

---

### Positive Observations

What's well-tested and follows best practices.

- **[Area 1]**: Good coverage of [specific scenarios]
- **[Area 2]**: Tests are behavioral and resilient to refactoring
- **[Area 3]**: Comprehensive error case coverage

---

### Summary Table

| Category | Count | Action |
|----------|-------|--------|
| Critical Gaps (8-10) | X | Must fix |
| Important (5-7) | Y | Should consider |
| Quality Issues | Z | Refactor when possible |
| Positive Areas | W | - |

### Recommended Priority

1. [First test to add - highest impact]
2. [Second test to add]
3. [Third test to add]
