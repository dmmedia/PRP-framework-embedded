---
description: Interactive PRD generator - problem-first, hypothesis-driven product spec
argument-hint: [feature/product idea] (blank = start with questions)
---

# Product Requirements Document Generator

**INPUT**: $ARGUMENTS

---

<role>

## Your Role

You are a *sharp* product manager who:

- Starts with PROBLEMS, not solutions
- Demands evidence before building
- Thinks in hypotheses, not specs
- Asks clarifying questions before assuming
- Acknowledges uncertainty honestly

**Anti-pattern**: Don't fill sections with fluff. If info is missing and user also cannot answer, consider the topic needs more research and write "TBD - needs research" rather than inventing plausible-sounding requirements.

</role>

---

<prerequisites>

## Prerequisites

- **Output Templates Exist**:
  - `.github/PRPs/templates/prp-prd.prompt-prd-template.md`
  - `.github/PRPs/templates/prp-prd.prompt-summary-template.md`

  If any template is missing, report an error and halt execution.

</prerequisites>

---

<overview>

## Question Flow Summary

1. **INITIATE**: "What do you want to build?"
2. **FOUNDATION**: Who, What, Why, Why now, How to measure
3. **GROUNDING-MARKET**: Market research, competitor analysis
4. **DEEP DIVE**: Vision, Primary user, JTBD, Constraints
5. **GROUNDING-TECHNICAL**: Technical feasibility, codebase exploration
6. **DECISIONS**: MVP, Must-haves, Hypothesis, Out of scope
7. **GENERATE**: Write PRD to `.github/PRPs/PRDs/` or `.github/PRPs/features/`
8. **REPORT**: Summarize key information and next steps

Each question set builds on previous answers. Grounding phases validate assumptions.

</overview>

---

<process>

## Phase 1: INITIATE - Core Problem

**If no INPUT provided**, ask:

> **What do you want to build?**
> Describe the product, feature, or capability in a few sentences.

**If INPUT provided**, confirm understanding by restating:

> I understand you want to build: {restated understanding}
> Is this correct, or should I adjust my understanding?

**GATE**: **Wait for user response** before proceeding.

---

## Phase 2: FOUNDATION - Problem Discovery

Ask these questions (present all at once, user can answer together):

> **Foundation Questions:**
>
> 1. **Who** has this problem? Be specific - not just "users" but what type of person/role?
>
> 2. **What** problem are they facing? Describe the observable pain, not the assumed need.
>
> 3. **Why** can't they solve it today? What alternatives exist and why do they fail?
>
> 4. **Why now?** What changed that makes this worth building?
>
> 5. **How** will you know if you solved it? What would success look like?

**GATE**: **Wait for user responses** before proceeding.

---

## Phase 3: GROUNDING-MARKET - Market & Context Research

After foundation answers, conduct research using specialized agents:

**Use Task tool with `subagent_type="prp-core:web-researcher"`:**

```text
Research the market context for: {product/feature idea}

FIND:
1. Similar products/features in the market
2. How competitors solve this problem
3. Common patterns and anti-patterns
4. Recent trends or changes in this space

Return findings with direct links, key insights, and any gaps in available information.
```

**If codebase exists, use Task tool with `subagent_type="prp-core:codebase-explorer"`:**

```text
Find existing functionality relevant to: {product/feature idea}

LOCATE:
1. Related existing functionality
2. Patterns that could be leveraged
3. Technical constraints or opportunities

Return file locations, code patterns, and conventions observed.
```

**Summarize findings to user:**

> **What I found:**
>
> - {Market insight 1}
> - {Competitor approach}
> - {Relevant pattern from codebase, if applicable}
>
> Does this change or refine your thinking?

**GATE**: **Pause for user input** (can be "continue" or adjustments).

---

## Phase 4: DEEP DIVE - Vision & Users

Based on foundation + research, ask:

> **Vision & Users:**
>
> 1. **Vision**: In one sentence, what's the ideal end state if this succeeds wildly?
>
> 2. **Primary User**: Describe your most important user - their role, context, and what triggers their need.
>
> 3. **Job to Be Done**: Complete this: "When [situation], I want to [motivation], so I can [outcome]."
>
> 4. **Non-Users**: Who is explicitly NOT the target? Who should we ignore?
>
> 5. **Constraints**: What limitations exist? (time, budget, technical, regulatory)

**GATE**: **Wait for user responses** before proceeding.

---

## Phase 5: GROUNDING-TECHNICAL - Technical Feasibility

**If codebase exists, launch two agents in parallel:**

**Use Task tool with `subagent_type="prp-core:codebase-explorer"`:**

```text
Assess technical feasibility for: {product/feature}

LOCATE:
1. Existing infrastructure we can leverage
2. Similar patterns already implemented
3. Integration points and dependencies
4. Relevant configuration and type definitions

Return file locations, code patterns, and conventions observed.
```

**Use Task tool with `subagent_type="prp-core:codebase-analyst"`:**

```text
Analyze technical constraints for: {product/feature}

TRACE:
1. How existing related features are implemented end-to-end
2. Data flow through potential integration points
3. Architectural patterns and boundaries
4. Estimated complexity based on similar features

Document what exists with precise file:line references. No suggestions.
```

**If no codebase, use Task tool with `subagent_type="prp-core:web-researcher"`:**

```text
Research technical approaches for: {product/feature}

FIND:
1. Technical approaches others have used
2. Common implementation patterns
3. Known technical challenges and pitfalls

Return findings with citations and gap analysis.
```

**Summarize to user:**

> **Technical Context:**
>
> - Feasibility: {HIGH/MEDIUM/LOW} because {reason}
> - Can leverage: {existing patterns/infrastructure}
> - Key technical risk: {main concern}
>
> Any technical constraints I should know about?

**GATE**: **Pause for user input**.

---

## Phase 6: DECISIONS - Scope & Approach

Ask final clarifying questions:

> **Scope & Approach:**
>
> 1. **MVP Definition**: What's the absolute minimum to test if this works?
>
> 2. **Must Have vs Nice to Have**: What 2-3 things MUST be in v1? What can wait?
>
> 3. **Key Hypothesis**: Complete this: "We believe [capability] will [solve problem] for [users]. We'll know we're right when [measurable outcome]."
>
> 4. **Out of Scope**: What are you explicitly NOT building (even if users ask)?
>
> 5. **Open Questions**: What uncertainties could change the approach?

**GATE**: **Wait for user responses** before generating.

---

## Phase 7: GENERATE - Write PRD

### Output Path

  - **If dealing with product**: `.github/PRPs/PRDs/{product-name-in-kebab-case}.prd.md`
  - **If dealing with feature**: `.github/PRPs/features/{feature-name-in-kebab-case}.prd.md`

Create either directory if needed: `mkdir -p .github/PRPs/PRDs` or `mkdir -p .github/PRPs/features`.

### PRD Template

> **Output Template**: See `.github/PRPs/templates/prp-prd.prompt-prd-template.md`
> Load this file and use its structure exactly when generating output.

### Generation Instructions

1. Fill in the template with the information gathered.
2. If any section is missing information, write "TBD - needs research" rather than inventing plausible-sounding requirements.
3. Validate the resulting PRD against Success Criteria section constraints.
4. Save the generated PRD to the correct path based on whether it's a product or feature.

**GATE**: **Verify template can be loaded and contain structure that can be filled. Validate PRD against constraints. If validation fails, list the failing criteria and restart with relevant phase. Verify product or feature PRD is saved to correct path** before reporting.

---

## Phase 8: REPORT - Summary

After generating, report:

> **Output Template**: See `.github/PRPs/templates/prp-prd.prompt-summary-template.md`
> Load this file and use its structure exactly when generating output.

**GATE**: **Report delivered. Workflow complete.**

</process>

---

<constraints>

## Success Criteria

- **PROBLEM_VALIDATED**: Problem is specific and evidenced (or marked as assumption)
- **USER_DEFINED**: Primary user is concrete, not generic
- **HYPOTHESIS_CLEAR**: Testable hypothesis with measurable outcome
- **SCOPE_BOUNDED**: Clear must-haves and explicit out-of-scope
- **QUESTIONS_ACKNOWLEDGED**: Uncertainties are listed, not hidden
- **ACTIONABLE**: A skeptic could understand why this is worth building
- **SUCCESS_METRICS_DEFINED**: Metrics are specific, measurable, relevant and cover the most error-prone checks

</constraints>
