---
description: Create comprehensive feature implementation plan with codebase analysis and research
argument-hint: <feature description | path/to/prd.md>
---

# Product or Feature Implementation Plan Generator

<role>

You are a Software Engineer who:

- Transforms feature descriptions or PRD phases into **information dense** implementation plans
- Uses **codebase intelligence** to ensure solutions fit existing patterns
- Conducts **targeted research** only after understanding codebase constraints

</role>

<objective>

## Objective

Transform "$ARGUMENTS" into a battle-tested implementation plan through systematic codebase exploration, pattern extraction, and strategic research. Apply **Constraints** from the section below and validate the plan against the **Success Criteria** before saving the output file.

</objective>

<constraints>

## Constraints

- **Core Principle**: ***PLAN ONLY - no code written***. Create a context-rich document that enables one-pass implementation success.
- **Execution Order**: **CODEBASE FIRST, RESEARCH SECOND**. Solutions must fit existing patterns before introducing new ones.
- **Output Template Search**: Use `list_dir` on `.github/templates/` to verify template files are present.

</constraints>

---

<context>

**Codebase Discovery**

- Identify project type from config files (package.json, pyproject.toml, Cargo.toml, go.mod, etc.)

**IMPORTANT**: Do NOT assume `src/` exists. Common alternatives include:

- `app/` (Next.js, Rails, Laravel)
- `lib/` (Ruby gems, Elixir)
- `packages/` (monorepos)
- `cmd/`, `internal/`, `pkg/` (Go)
- Root-level source files (Python, scripts)

Discover the actual structure before proceeding.

</context>

<process>

## Phase 0: DETECT - Input Type Resolution

**Determine input type:**

| Input Pattern | Type | Action |
| --- | --- | --- |
| Ends with `.prd.md` | PRD file | Parse PRD, select next phase |
| Ends with `.md` and contains "Implementation Phases" | PRD file | Parse PRD, select next phase |
| File path that exists | Document | Read and extract feature description |
| Free-form text | Description | Use directly as feature input |
| Empty/blank | Conversation | Use conversation context as input |

### If PRD File Detected

1. **Read the PRD file**
2. **Parse the Implementation Phases table** - find rows with `Status: pending`
3. **Check dependencies** - only select phases whose dependencies are `complete`
4. **Select the next actionable phase:**

   - First pending phase with all dependencies complete
   - If multiple candidates with same dependencies, note parallelism opportunity

5. **Extract phase context:**

   ```text
   PHASE: {phase number and name}
   GOAL: {from phase details}
   SCOPE: {from phase details}
   SUCCESS SIGNAL: {from phase details}
   PRD CONTEXT: {problem statement, user, hypothesis from PRD}
   ```

6. **Report selection to user:**

   ```text
   PRD: {prd file path}
   Selected Phase: #{number} - {name}

   {If parallel phases available:}
   Note: Phase {X} can also run in parallel (in separate worktree).

   Proceeding with Phase #{number}...
   ```

### If Free-form or Conversation Context

- Proceed directly to Phase 1 with the input as feature description

**PHASE_0_CHECKPOINT:**

- [ ] Input type determined
- [ ] If PRD: next phase selected and dependencies verified
- [ ] Feature description ready for Phase 1

---

## Phase 1: PARSE - Feature Understanding

**EXTRACT from input:**

- Core problem being solved
- User value and business impact
- Feature type: NEW_CAPABILITY | ENHANCEMENT | REFACTOR | BUG_FIX
- Complexity: LOW | MEDIUM | HIGH
- Affected systems list

**FORMULATE user story:**

```text
As a <user type>
I want to <action/goal>
So that <benefit/value>
```

**PHASE_1_CHECKPOINT:**

- [ ] Problem statement is specific and testable
- [ ] User story follows correct format
- [ ] Complexity assessment has rationale
- [ ] Affected systems identified

**GATE**: **If requirements are AMBIGUOUS** then ***STOP and ASK*** user for clarification before proceeding.

---

## Phase 2: EXPLORE - Codebase Intelligence

**CRITICAL: Launch two specialized agents in parallel using multiple Task tool calls in a single message.**

### Agent 1: `prp-core:codebase-explorer`

Finds WHERE code lives and extracts implementation patterns.

Use Task tool with `subagent_type="prp-core:codebase-explorer"`:

```text
Find all code relevant to implementing: [feature description].

LOCATE:
1. Similar implementations - analogous features with file:line references
2. Naming conventions - actual examples of function/class/file naming
3. Error handling patterns - how errors are created, thrown, caught
4. Logging patterns - logger usage, message formats
5. Type definitions - relevant interfaces and types
6. Test patterns - test file structure, assertion styles, test file locations
7. Configuration - relevant config files and settings
8. Dependencies - relevant libraries already in use

Categorize findings by purpose (implementation, tests, config, types, docs).
Return ACTUAL code snippets from codebase, not generic examples.

Always wrap the output of your analysis in `<analysis>` tags.
```

### Agent 2: `prp-core:codebase-analyst`

Analyzes HOW integration points work and traces data flow.

Use Task tool with `subagent_type="prp-core:codebase-analyst"`:

```text
Analyze the implementation details relevant to: [feature description].

TRACE:
1. Entry points - where new code will connect to existing code
2. Data flow - how data moves through related components
3. State changes - side effects in related functions
4. Contracts - interfaces and expectations between components
5. Patterns in use - design patterns and architectural decisions

Document what exists with precise file:line references. No suggestions or improvements.

Always wrap the output of your analysis in `<analysis>` tags.
```

### Merge Agent Results

Extract information from both agents analysis reports and combine findings into a unified discovery table:

> | Category | File:Lines | Pattern Description | Code Snippet |
> | --- | --- | --- | --- |
> | NAMING | `src/features/X/service.ts:10-15` | camelCase functions | `export function createThing()` |
> | ERRORS | `src/features/X/errors.ts:5-20` | Custom error classes | `class ThingNotFoundError` |
> | LOGGING | `src/core/logging/index.ts:1-10` | getLogger pattern | `const logger = getLogger("domain")` |
> | TESTS | `src/features/X/tests/service.test.ts:1-30` | describe/it blocks | `describe("service", () => {` |
> | TYPES | `src/features/X/models.ts:1-20` | Drizzle inference | `type Thing = typeof things.$inferSelect` |
> | FLOW | `src/features/X/service.ts:40-60` | Data transformation | `input → validate → persist → respond` |

**PHASE_2_CHECKPOINT:**

- [ ] Both agents (`prp-core:codebase-explorer` and `prp-core:codebase-analyst`) launched in parallel and completed
- [ ] At least 3 similar implementations found with file:line refs
- [ ] Code snippets are ACTUAL (copy-pasted from codebase, not invented)
- [ ] Integration points mapped with data flow traces
- [ ] Dependencies cataloged with versions from package.json

---

## Phase 3: RESEARCH - External Documentation

**ONLY AFTER Phase 2 is complete** - solutions must fit existing codebase patterns first.

**Use Task tool with `subagent_type="prp-core:web-researcher"`:**

```text
Research external documentation relevant to implementing: [feature description].

FIND:
1. Official documentation for involved libraries (match versions from package.json: [list relevant deps and versions])
2. Known gotchas, breaking changes, deprecations for these versions
3. Security considerations and best practices
4. Performance optimization patterns

VERSION CONSTRAINTS:
- [library]: v{version} (from package.json)
- [library]: v{version}

Return findings with:
- Direct links to specific doc sections (not just homepages)
- Key insights that affect implementation
- Gotchas with mitigation strategies
- Any conflicts between docs and existing codebase patterns found in Phase 2

Always wrap the output of your analysis in `<analysis>` tags.
```

**Extract analysis results and FORMAT the agent's findings into plan references:**

```markdown
- [Library Docs v{version}](https://url#specific-section)
  - KEY_INSIGHT: {what we learned that affects implementation}
  - APPLIES_TO: {which task/file this affects}
  - GOTCHA: {potential pitfall and how to avoid}
```

**PHASE_3_CHECKPOINT:**

- [ ] `prp-core:web-researcher` agent launched and completed
- [ ] Documentation versions match package.json
- [ ] URLs include specific section anchors (not just homepage)
- [ ] Gotchas documented with mitigation strategies
- [ ] No conflicting patterns between external docs and existing codebase

---

## Phase 4: DESIGN - UX Transformation

**CREATE ASCII diagrams showing user experience before and after for report to human:**

> **Output Template**: See `.github/templates/prp-plan.prompt-design-template.md`
> Load this file and use its structure exactly when generating output.

**DOCUMENT interaction changes:**

| Location | Before | After | User_Action | Impact |
| --- | --- | --- | --- | --- |
| `/route` | State A | State B | Click X | Can now Y |
| `Component.tsx` | Missing feature | Has feature | Input Z | Gets result W |

**PHASE_4_CHECKPOINT:**

- [ ] Before state accurately reflects current system behavior
- [ ] After state shows ALL new capabilities
- [ ] Data flows are traceable from input to output
- [ ] User value is explicit and measurable

---

## Phase 5: ARCHITECT - Strategic Design

**IF Complexity == LOW (from Phase 1)**: skip Task tool calls directly to **analysis** below.

**For more complex features with multiple integration points**, use `prp-core:codebase-analyst` to trace how existing architecture works at the integration points identified in Phase 2:

Use Task tool with `subagent_type="prp-core:codebase-analyst"`:

```text
Analyze the architecture around these integration points for: [feature description].

INTEGRATION POINTS (from Phase 2):
- [entry point 1 from explorer/analyst findings]
- [entry point 2]

ANALYZE:
1. How data flows through each integration point
2. What contracts exist between components
3. What side effects occur at each stage
4. What error handling patterns are in place

Document what exists with precise file:line references. No suggestions.

Always wrap the output of your analysis in `<analysis>` tags.
```

If agent was used, extract analysis results and merge with your knowledge base.

**Then ANALYZE deeply (use extended thinking if needed):**

- ARCHITECTURE_FIT: How does this integrate with the existing architecture?
- EXECUTION_ORDER: What must happen first → second → third?
- FAILURE_MODES: Edge cases, race conditions, error scenarios?
- PERFORMANCE: Will this scale? Database queries optimized?
- SECURITY: Attack vectors? Data exposure risks? Auth/authz?
- MAINTAINABILITY: Will future devs understand this code?

**DECIDE and document:**

```markdown
APPROACH_CHOSEN: [description]
RATIONALE: [why this over alternatives - reference codebase patterns]

ALTERNATIVES_REJECTED:

- [Alternative 1]: Rejected because [specific reason]
- [Alternative 2]: Rejected because [specific reason]

NOT_BUILDING (explicit scope limits):

- [Item 1 - explicitly out of scope and why]
- [Item 2 - explicitly out of scope and why]
```

**PHASE_5_CHECKPOINT:**

- [ ] Approach aligns with existing architecture and patterns
- [ ] Dependencies ordered correctly (types → repository → service → routes)
- [ ] Edge cases identified with specific mitigation strategies
- [ ] Scope boundaries are explicit and justified

---

## Phase 6: GENERATE - Implementation Plan File

**OUTPUT_PATH**: `PRPs/plans/{kebab-case-feature-name}.plan.md`

Create directory if needed: `mkdir -p PRPs/plans`

**PLAN_STRUCTURE** (the template to fill and save):

> **Output Template**: See `.github/templates/prp-plan.prompt-plan-template.md`
> Load this file and use its structure exactly when generating output.

</process>

<output>

**OUTPUT_FILE**: `PRPs/plans/{kebab-case-feature-name}.plan.md`

**If input was from PRD file**, also update the PRD:

1. **Update phase status** in the Implementation Phases table:

   - Change the phase's Status from `pending` to `in-progress`
   - Add the plan file path to the PRP Plan column

2. **Edit the PRD file** with these changes

**REPORT_TO_USER** (display after creating plan):

> **Output Template**: See `.github/templates/prp-plan.prompt-summary-template.md`
> Load this file and use its structure exactly when generating output.

</output>

<verification>

**FINAL_VALIDATION before saving plan:**

**CONTEXT_COMPLETENESS:**

- [ ] Every task has at least one executable validation command

**IMPLEMENTATION_READINESS:**

- [ ] Tasks ordered by dependency (can execute top-to-bottom)
- [ ] Each task is atomic and independently testable
- [ ] No placeholders - all content is specific and actionable

**PATTERN_FAITHFULNESS:**

- [ ] Every new file mirrors existing codebase style exactly
- [ ] No unnecessary abstractions introduced
- [ ] Naming follows discovered conventions
- [ ] Error/logging patterns match existing
- [ ] Test structure matches existing tests

**VALIDATION_COVERAGE:**

- [ ] All 6 validation levels defined in the plan generated from the loaded template where applicable

**NO_PRIOR_KNOWLEDGE_TEST**: Could an agent unfamiliar with this codebase implement using ONLY the plan?

</verification>

<success_criteria>

## Success Criteria

- **CONTEXT_COMPLETE**: All patterns, gotchas, integration points documented from actual codebase via `prp-core:codebase-explorer` and `prp-core:codebase-analyst` agents
- **IMPLEMENTATION_READY**: Tasks executable top-to-bottom without questions, research, or clarification
- **PATTERN_FAITHFUL**: Every new file mirrors existing codebase style exactly
- **VALIDATION_DEFINED**: Every task has executable verification command
- **UX_DOCUMENTED**: Before/After transformation is visually clear with data flows
- **ONE_PASS_TARGET**: Confidence score 8+ indicates high likelihood of first-attempt success

</success_criteria>
