## Implementation Complete

**Plan**: `$ARGUMENTS`
**Source Issue**: #{number} (if applicable)
**Branch**: `{branch-name}`
**Status**: ✅ Complete

### Validation Summary

| Check      | Result          |
| ---------- | --------------- |
| Type check | ✅              |
| Lint       | ✅              |
| Tests      | ✅ ({N} passed) |
| Build      | ✅              |

### Files Changed

- {N} files created
- {M} files updated
- {K} tests written

### Deviations

{If none: "Implementation matched the plan."}
{If any: Brief summary of what changed and why}

### Artifacts

- Report: `.claude/PRPs/reports/{name}-report.md`
- Plan archived to: `.claude/PRPs/plans/completed/`

{If from PRD:}
### PRD Progress

**PRD**: `{prd-file-path}`
**Phase Completed**: #{number} - {phase name}

| # | Phase | Status |
|---|-------|--------|
{Updated phases table showing progress}

**Next Phase**: {next pending phase, or "All phases complete!"}
{If next phase can parallel: "Note: Phase {X} can also start now (parallel)"}

To continue: `/prp-plan {prd-path}`

### Next Steps

1. Review the report (especially if deviations noted)
2. Create PR: `gh pr create` or `/prp-pr`
3. Merge when approved
{If more phases: "4. Continue with next phase: `/prp-plan {prd-path}`"}
