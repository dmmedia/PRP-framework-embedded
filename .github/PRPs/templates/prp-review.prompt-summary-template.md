## PR Review Complete

**PR**: #{NUMBER} - {TITLE}
**URL**: {PR_URL}
**Recommendation**: {APPROVE/REQUEST CHANGES/BLOCK}

### Issues Found

| Severity | Count |
|----------|-------|
| Critical | {N} |
| High | {N} |
| Medium | {N} |
| Suggestions | {N} |

### Validation

| Check | Result |
|-------|--------|
| Type Check | {PASS/FAIL} |
| Lint | {PASS/FAIL} |
| Tests | {PASS/FAIL} |
| Build | {PASS/FAIL} |

### Artifacts

- Report: `.claude/PRPs/reviews/pr-{NUMBER}-review.md`
- PR Comment: {comment_url}

### Next Steps

{Based on recommendation:}

- APPROVE: "PR is ready for merge"
- REQUEST CHANGES: "Author should address {N} high-priority issues"
- BLOCK: "Fundamental issues need resolution before proceeding"
