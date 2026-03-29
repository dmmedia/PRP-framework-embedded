# Feature: Migrate PRP Framework to GitHub Copilot + VS Code

## Summary

This plan migrates the PRP framework from Claude-centric workflows to native GitHub Copilot and VS Code support. It ensures all agent guidance, documentation, and prompt templates are Copilot-compatible, and that the directory structure and file placement follow the new conventions. The plan addresses all missing requirements and review feedback from the initial migration attempt.

## User Story

As a developer or agent using the PRP framework,
I want all PRP workflows, agent guidance, and documentation to be Copilot/VS Code native,
So that I can execute, extend, and maintain PRP flows without Claude dependencies or manual translation.

## Problem Statement

The PRP framework is tightly coupled to "Claude Code" conventions, with agent guidance, prompt templates, and documentation referencing Claude-specific commands and directory structures. This blocks Copilot/VS Code adoption and creates onboarding friction. The initial migration missed key requirements: agent guidance parity, correct file placement, and explicit migration of all Claude agent guides.

## Solution Statement

Migrate all agent guidance, prompt templates, and documentation to Copilot/VS Code conventions. For every deprecated Claude agent guide, create an equivalent Copilot/VS Code agent guidance file. Place migration and quickstart guides in the project root. Only agent/technology-specific guides go in `copilot_md_files/`. Update the PRD and docs to reflect these rules. Ensure all workflows are validated in-editor with Copilot.

## Metadata

| Field            | Value                                             |
| ---------------- | ------------------------------------------------- |
| Type             | REFACTOR                                          |
| Complexity       | MEDIUM                                            |
| Systems Affected | docs, agent guides, prompt templates, onboarding  |
| Dependencies     | GitHub Copilot, VS Code, PRP framework            |
| Estimated Tasks  | 8                                                 |

---

## UX Design

### Before State
```
Claude agent guides and docs scattered in claude_md_files/; migration/quickstart in wrong locations; Copilot users lack agent guidance; onboarding is confusing.
```

### After State
```
All agent/technology guides in copilot_md_files/; migration/quickstart in project root; every deprecated Claude guide has a Copilot/VS Code equivalent; onboarding and agent flows are clear and Copilot-native.
```

### Interaction Changes
| Location                        | Before                        | After                                 | User Impact                        |
|---------------------------------|-------------------------------|---------------------------------------|------------------------------------|
| claude_md_files/CLAUDE-*.md     | Claude agent guidance         | Deprecated, Copilot equivalent exists | Agents/models follow Copilot rules |
| copilot_md_files/               | (empty or human docs)         | Agent/tech-specific guides only       | Agents/models get correct context  |
| copilot-migration-guide.md      | In copilot_md_files/          | In project root                       | Humans find migration steps easily |
| copilot-prp-quickstart.md       | In copilot_md_files/          | In project root                       | Humans find quickstart easily      |
| copilot-prp-troubleshooting.md  | In copilot_md_files/          | In project root                       | Humans find troubleshooting easily |

---

## Mandatory Reading

| Priority | File                                    | Lines | Why Read This                                 |
|----------|-----------------------------------------|-------|-----------------------------------------------|
| P0       | claude_md_files/CLAUDE-*.md             | all   | Source agent guidance to migrate              |
| P1       | copilot_md_files/                       | all   | Target for Copilot/VS Code agent guides       |
| P2       | copilot-migration-guide.md              | all   | Migration steps and rationale                 |
| P3       | copilot-prp-quickstart.md               | all   | Quickstart for Copilot/VS Code                |
| P4       | copilot-prp-troubleshooting.md          | all   | Troubleshooting Copilot/VS Code integration   |
| P5       | README.md, README-for-DUMMIES.md        | all   | Onboarding and workflow context               |

**External Documentation:**
| Source | Section | Why Needed |
|--------|---------|------------|
| [Copilot Docs](https://docs.github.com/en/copilot) | All | Ensure compatibility and best practices |
| [VS Code Docs](https://code.visualstudio.com/docs) | All | Editor integration and extension usage |

---

## Patterns to Mirror

**AGENT_GUIDANCE_PARITY:**
```markdown
// SOURCE: claude_md_files/CLAUDE-*.md
// COPY THIS PATTERN:
- Each Claude agent guide must have a Copilot/VS Code equivalent with the same structure and conventions, updated for Copilot workflows.
```

**DOC_PLACEMENT_RULES:**
```markdown
// SOURCE: PR review comments
// COPY THIS PATTERN:
- Migration/quickstart/troubleshooting guides go in project root.
- Only agent/technology-specific guides go in copilot_md_files/.
```

---

## Files to Change

| File                                    | Action   | Justification                                 |
|-----------------------------------------|----------|-----------------------------------------------|
| claude_md_files/CLAUDE-*.md             | DEPRECATE| Mark as deprecated, migrate content           |
| copilot_md_files/AGENT-*.md             | CREATE   | Copilot/VS Code agent guidance                |
| copilot-migration-guide.md              | MOVE     | To project root                               |
| copilot-prp-quickstart.md               | MOVE     | To project root                               |
| copilot-prp-troubleshooting.md          | MOVE     | To project root                               |
| README.md, README-for-DUMMIES.md        | UPDATE   | Reference new guides and structure            |
| .claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md | UPDATE | Add missing requirements and migration steps   |

---

## NOT Building (Scope Limits)

- No migration of old-prp-commands/ (historical, out of scope)
- No Claude-only features that lack Copilot/VS Code equivalents
- No changes to core PRP logic outside documentation and agent guidance

---

## Step-by-Step Tasks

### Task 1: Inventory Claude Agent Guides
- **ACTION**: List all `claude_md_files/CLAUDE-*.md` files
- **IMPLEMENT**: Create migration checklist
- **VALIDATE**: All guides accounted for

### Task 2: Create Copilot/VS Code Agent Guides
- **ACTION**: For each Claude agent guide, create a Copilot/VS Code equivalent in `copilot_md_files/`
- **IMPLEMENT**: Migrate content, update for Copilot workflows
- **VALIDATE**: Parity checklist complete

### Task 3: Move Human-Facing Guides to Root
- **ACTION**: Move `copilot-migration-guide.md`, `copilot-prp-quickstart.md`, `copilot-prp-troubleshooting.md` to project root
- **IMPLEMENT**: Update references in docs and onboarding
- **VALIDATE**: Files in correct location

### Task 4: Update PRD and Documentation
- **ACTION**: Update PRD and all onboarding docs to reflect new requirements, directory structure, and migration steps
- **IMPLEMENT**: Add explicit migration steps, placement rules, and agent guidance parity
- **VALIDATE**: PRD and docs match new structure

### Task 5: Deprecate Claude Agent Guides
- **ACTION**: Mark all `claude_md_files/CLAUDE-*.md` as deprecated
- **IMPLEMENT**: Add deprecation header, reference Copilot equivalent
- **VALIDATE**: All guides marked and referenced

### Task 6: Update References in Templates and Scripts
- **ACTION**: Update all prompt templates, scripts, and adapters to reference Copilot/VS Code guides
- **IMPLEMENT**: Search/replace references, update links
- **VALIDATE**: No references to deprecated Claude guides remain

### Task 7: Validate Onboarding and Agent Flows
- **ACTION**: Test onboarding and agent flows in VS Code with Copilot
- **IMPLEMENT**: Follow quickstart, run PRP workflows
- **VALIDATE**: All flows work without Claude dependencies

### Task 8: Review and Finalize Migration
- **ACTION**: Review all changes, confirm requirements met
- **IMPLEMENT**: Human review, update plan/PRD as needed
- **VALIDATE**: All review feedback addressed

---

## Testing Strategy

| Test File | Test Cases | Validates |
|-----------|------------|-----------|
| N/A (docs/agent migration) | Migration checklist, parity, placement | All requirements met |

### Edge Cases Checklist
- [ ] All agent guides have Copilot equivalents
- [ ] No human guides in copilot_md_files/
- [ ] No references to deprecated Claude guides
- [ ] Onboarding works for Copilot/VS Code users

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
npx prettier --check . && npx markdownlint .
```
**EXPECT**: No formatting or lint errors

### Level 2: MANUAL_VALIDATION
- [ ] Human review of migration, parity, and placement

---

## Acceptance Criteria
- [ ] All Claude agent guides have Copilot/VS Code equivalents
- [ ] Migration/quickstart/troubleshooting guides in project root
- [ ] No human guides in copilot_md_files/
- [ ] All onboarding and agent flows work in Copilot/VS Code
- [ ] All review feedback from PR #1 addressed

---

## Completion Checklist
- [ ] All tasks completed in order
- [ ] Each task validated after completion
- [ ] All acceptance criteria met

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Missed agent guide | MED | MED | Use migration checklist, review all files |
| Human guides misplaced | LOW | MED | Explicit placement rules, review |
| Missed references | MED | LOW | Search/replace, manual review |

---

## Notes
- This plan incorporates all missing requirements and review feedback from PR #1.
- All agent guidance must be Copilot/VS Code native and placed according to new rules.
- Human-facing guides (migration, quickstart, troubleshooting) must be in the project root.
- No further changes to core PRP logic or old-prp-commands/.
