## 🔍 Investigation: {Title}

**Type**: `{TYPE}`

### Assessment

| Metric | Value | Reasoning |
|---|---|---|
| {Severity or Priority} | `{VALUE}` | {one-sentence why} |
| Complexity | `{COMPLEXITY}` | {one-sentence why} |
| Confidence | `{CONFIDENCE}` | {one-sentence why} |

---

### Problem Statement

{problem statement from artifact}

---

### Root Cause Analysis

{evidence chain, formatted for GitHub}

---

### Implementation Plan

| Step | File | Change |
|---|---|---|
| 1 | `src/x.ts:45` | {description} |
| 2 | `src/x.test.ts` | Add test for {case} |

<details>
<summary>📋 Detailed Implementation Steps</summary>

{detailed steps from artifact}

</details>

---

### Validation

```bash
# Run project's validation commands (adapt to toolchain)
{type-check-cmd} && {test-cmd} {pattern} && {lint-cmd}
```

---

### Next Step

To implement: `/prp-issue-fix {number}`

---

_Investigated by Claude • {timestamp}_
