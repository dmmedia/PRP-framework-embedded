# PRP Prompt Output Templates

This directory contains standalone output format templates extracted from the 13 prompt files in `.github/prompts/`.

## Purpose

Each template defines the exact output structure an agent must produce when executing a PRP prompt.
Separating templates from prompt logic lets maintainers update output formats without touching
agent instruction logic, and lets contributors find any template in under 10 seconds.

## Naming Convention

```text
<prompt-name>.prompt-<function>-template.md
```

- `<prompt-name>` — matches the source `.prompt.md` file name without the extension (e.g., `prp-prd`)
- `<function>` — derived from the phase name where the template is embedded (e.g., `generate`, `output`, `report`, `design`)

## Template Reference Pattern

When a prompt references a template, it uses this instruction block:

```markdown
> **Output Template**: See `.github/PRPs/templates/{name}.prompt-{function}-template.md`
> Load this file and use its structure exactly when generating output.
```

## Template Inventory

19 template files total across 13 source prompts:

| Template File | Source Prompt | Function (Phase) |
|---|---|---|
| `prp-codebase-question.prompt-research-template.md` | `prp-codebase-question.prompt.md` | DOCUMENT (Phase 5) |
| `prp-codebase-question.prompt-summary-template.md` | `prp-codebase-question.prompt.md` | OUTPUT (Phase 6) |
| `prp-commit.prompt-output-template.md` | `prp-commit.prompt.md` | OUTPUT (Phase 4) |
| `prp-debug.prompt-report-template.md` | `prp-debug.prompt.md` | REPORT (Phase 5) |
| `prp-implement.prompt-report-template.md` | `prp-implement.prompt.md` | REPORT (Phase 5) |
| `prp-issue-fix.prompt-report-template.md` | `prp-issue-fix.prompt.md` | OUTPUT |
| `prp-issue-investigate.prompt-artifact-template.md` | `prp-issue-investigate.prompt.md` | BLUEPRINT |
| `prp-plan.prompt-design-template.md` | `prp-plan.prompt.md` | DESIGN (Phase 4) |
| `prp-plan.prompt-plan-template.md` | `prp-plan.prompt.md` | GENERATE (Phase 6) |
| `prp-pr.prompt-pr-template.md` | `prp-pr.prompt.md` | GENERATE |
| `prp-pr.prompt-summary-template.md` | `prp-pr.prompt.md` | OUTPUT |
| `prp-prd.prompt-prd-template.md` | `prp-prd.prompt.md` | GENERATE (Phase 7) |
| `prp-prd.prompt-summary-template.md` | `prp-prd.prompt.md` | OUTPUT (Phase 8) |
| `prp-ralph-cancel.prompt-cancel-template.md` | `prp-ralph-cancel.prompt.md` | OUTPUT |
| `prp-ralph.prompt-setup-template.md` | `prp-ralph.prompt.md` | SETUP (Phase 2) |
| `prp-ralph.prompt-progress-template.md` | `prp-ralph.prompt.md` | PROGRESS |
| `prp-review-agents.prompt-summary-template.md` | `prp-review-agents.prompt.md` | SUMMARY |
| `prp-review.prompt-report-template.md` | `prp-review.prompt.md` | REPORT |
| `prp-review.prompt-summary-template.md` | `prp-review.prompt.md` | OUTPUT/SUMMARY |
