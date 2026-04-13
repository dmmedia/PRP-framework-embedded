# PRP (Product Requirement Prompts)

A collection of prompts, agents and skills for AI-assisted embedded development with Github CoPilot in VS Code.

**Migration Notice:**
The PRP framework is being migrated from Claude-specific workflows to GitHub Copilot and VS Code native flows. All Copilot quickstart, migration, and troubleshooting guides may be integrated into this README and the workspace settings. Legacy Claude documentation is deprecated and retained only for reference.

- New top-level agent guide: [`AGENTS.md`](AGENTS.md)
- Copilot user guides in `copilot_md_files/`
- Deprecated legacy docs in `claude_md_files/` with deprecation headers

**Key Migration Changes:**
- PRP flows now run via Copilot CLI/Chat and VS Code commands
- All Copilot documentation is now in this README and workspace settings
- Legacy Claude guides have been removed from the repository?

Refer to the new adapter at `PRPs/scripts/invoke_copilot.py` for Copilot CLI integration.

**TODO:**

- Guard prompts against subagent failures to retry once and then bail out. Otherwise prompt tries to do everything itself and pollutes the context.
- Although implementation prompt is defined as *autonomous*, let it go interactive or bail out if some substantial problem is encountered, that is not covered by PRD and plan.
- Review agents Markdown according to `agents_md_files/HOW-TO-WRITE-AGENT.md` guide "Syntax and XML Tags" section.
- Review remaining prompts Markdown according to `agents_md_files/HOW-TO-WRITE-AGENT.md` guide "Syntax and XML Tags" section.
    - `.github\prompts\prp-codebase-question.prompt.md`
    - `.github\prompts\prp-commit.prompt.md`
    - `.github\prompts\prp-debug.prompt.md`
    - `.github\prompts\prp-issue-fix.prompt.md`
    - `.github\prompts\prp-issue-investigate.prompt.md`
    - `.github\prompts\prp-pr.prompt.md`
    - `.github\prompts\prp-ralph-cancel.prompt.md`
    - `.github\prompts\prp-ralph.prompt.md`
    - `.github\prompts\prp-review-agents.prompt.md`
    - `.github\prompts\prp-review.prompt.md`
- Review remaining agent-to-agent templates
- Review prompts:
   - extract more templates, as it seems that the 1st and 2nd extraction did not do all of them to separate files and instruct prompts to read and use them when needed in a same way, like in the 1st extraction covered by `.claude\PRPs\prds\completed\extract-prompt-output-templates.prd.md`
   - fix heredoc template usage in:
      - `.github\prompts\prp-issue-fix.prompt.md`
      - `.github\prompts\prp-issue-investigate.prompt.md`
   - exclude project specific information already covered in `AGENTS.md`
   - remove all duplications
      - `.github\prompts\prp-issue-fix.prompt.md` - replace 6.2 write commit message duplicated template with a single template
   - minimize prompts
      - `.github\prompts\prp-issue-fix.prompt.md` - replace 3.2 decision tree ascii with mermaid or list
- Review agents:
   - extract templates to separate files and reference them
   - remove all duplications
   - minimize prompts
- Review new `AGENT.md` templates and extend content from migrated `claude_md_files/` where possible. Remove other files. Remove old `claude_md_files/`.
- Transform `.claude-plugin` and `plugins/prp-core` into VS Code or Copilot extension.
- Update all agents and replace Anthropic model choice with the list of best models for every Copilot subscription tier, beginning with the most capable one.
- Migrate all prompts, agents and skills to use language agnostic examples instead of existing TypeScript.
- Include C/C++ development best practices and reference to patterns, and coding guide (e.g. MISRA, Power of ten, etc.) in the embedded development guides.
- Include use of Cppcheck into C and C++ `AGENTS.md` templates.

## VS Code + Copilot PRP Workflow

1. Copy the `.github/` directory into your project root.
2. Initialize Python environment and install dependencies:
   ```console
   pip install uv
   uv sync
   ```
3. Open project in VS Code and install recommended extensions (workspace prompts include Copilot, Copilot Chat, GitLens, and GitHub PR).
4. Use the command palette: `Tasks: Run Task` → choose one of:
   - `PRP: Create PRD`
   - `PRP: Plan`
   - `PRP: Implement`
5. Workspace tasks are defined in `.vscode/tasks.json` and execute the `prp_workflow.py` orchestrator via `uv run`.
6. For manual usage, use:
   - `uv run .github/PRPs/scripts/prp_workflow.py "<feature>" --no-commit --no-pr`
   - `uv run .github/PRPs/scripts/prp_workflow.py --skip-create --prp-path <plan> --no-commit --no-pr`

> Note: Set `PRP_TOOL_ADAPTER=copilot` to try Copilot CLI path; fallback to `claude` is available by default.
> Optionally set `PRP_TOOL_WORKDIR=<path>` to use an alternate workspace root (e.g. `.copilot`) for `.claude` command resolution.

Heavily based on [PRP framework](https://github.com/Wirasm/PRPs-agentic-eng) by [Rasmus Widing](https://www.rasmuswiding.com/)

## What is PRP?

**Product Requirement Prompt (PRP)** = PRD + curated codebase intelligence + agent/runbook

The minimum viable packet an AI needs to ship production-ready code on the first pass.

A PRP supplies an AI coding agent with everything it needs to deliver a vertical slice of working software—no more, no less.

### How PRP Differs from Traditional PRD

A traditional PRD clarifies _what_ the product must do and _why_ customers need it, but deliberately avoids _how_ it will be built.

A PRP keeps the goal and justification sections of a PRD yet adds AI-critical layers:

- **Context**: Precise file paths, library versions, code snippet examples
- **Patterns**: Existing codebase conventions to follow
- **Validation**: Executable commands the AI can run to verify its work

---

## Quick Start

### Option 1: Copy Commands to Your Project

```console
# From your project root
cp -r /path/to/PRPs-framework-embedded/.github/ .github/
```

### Option 2: Clone Repository

```console
git clone https://github.com/dmmedia/PRP-framework-embedded.git
cd PRP-framework-embedded
```

---

## Commands

The `.github/prompts/` directory contains the core PRP workflow commands:

### Core Workflow

| Command          | Description                                              |
| ---------------- | -------------------------------------------------------- |
| `/prp-prd`       | Interactive PRD generator with implementation phases     |
| `/prp-plan`      | Create implementation plan (from PRD or free-form input) |
| `/prp-implement` | Execute a plan with validation loops                     |

### Issue & Debug Workflow

| Command                  | Description                                      |
| ------------------------ | ------------------------------------------------ |
| `/prp-issue-investigate` | Analyze GitHub issue, create implementation plan |
| `/prp-issue-fix`         | Execute fix from investigation artifact          |
| `/prp-debug`             | Deep root cause analysis with 5 Whys methodology |

### Git & Review

| Command       | Description                                       |
| ------------- | ------------------------------------------------- |
| `/prp-commit` | Smart commit with natural language file targeting |
| `/prp-pr`     | Create PR with template support                   |
| `/prp-review` | Comprehensive PR code review                      |

### Autonomous Loop

| Command             | Description                                      |
| ------------------- | ------------------------------------------------ |
| `/prp-ralph`        | Start autonomous loop until all validations pass |
| `/prp-ralph-cancel` | Cancel active Ralph loop                         |

---

## Ralph Loop (Autonomous Execution)

Based on [Geoffrey Huntley's Ralph Wiggum technique](https://ghuntley.com/ralph/) - a self-referential loop that keeps iterating until the job is actually done.

### How It Works

```console
/prp-ralph .github/PRPs/plans/my-feature.plan.md --max-iterations 20
```

1. Copilot implements the plan tasks
2. Runs all validation commands (type-check, lint, tests, build)
3. If any validation fails → fixes and re-validates
4. Loop continues until ALL validations pass
5. Outputs `<promise>COMPLETE</promise>` and exits

Each iteration, Copilot sees its previous work in files and git history. It's not starting fresh - it's debugging itself.

### Setup

The stop hook must be configured in `.github/settings.local.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".github/hooks/prp-ralph-stop.sh"
          }
        ]
      }
    ]
  }
}
```

### Usage

```console
# Create a plan
/prp-plan "add user authentication with JWT"

# Let Ralph loose
/prp-ralph .github/PRPs/plans/add-user-auth.plan.md --max-iterations 20

# Cancel if needed
/prp-ralph-cancel
```

### Tips

- Always use `--max-iterations` (default: 20) to prevent infinite loops
- Works best with plans that have clear, testable validation commands
- State is tracked in `.github/prp-ralph.state.md`
- Progress and learnings are captured in the implementation report

---

## Workflow Overview

### Large Features: PRD → Plan → Implement

```text
/prp-prd "user authentication system"
    ↓
Creates PRD with Implementation Phases table
    ↓
/prp-plan .github/PRPs/prds/user-auth.prd.md
    ↓
Auto-selects next pending phase, creates plan
    ↓
/prp-implement .github/PRPs/plans/user-auth-phase-1.plan.md
    ↓
Executes plan, updates PRD progress, archives plan
    ↓
Repeat /prp-plan for next phase
```

### Medium Features: Direct to Plan

```text
/prp-plan "add pagination to the API"
    ↓
Creates implementation plan from description
    ↓
/prp-implement .github/PRPs/plans/add-pagination.plan.md
```

### Bug Fixes: Issue Workflow

```text
/prp-issue-investigate 123
    ↓
Analyzes issue, creates investigation artifact
    ↓
/prp-issue-fix 123
    ↓
Implements fix, creates PR
```

---

## Artifacts Structure

All artifacts are stored in `.github/PRPs/`:

```text
.github/PRPs/
├── prds/              # Product requirement documents
├── plans/             # Implementation plans
│   └── completed/     # Archived completed plans
├── reports/           # Implementation reports
├── issues/            # Issue investigation artifacts
│   └── completed/     # Archived completed investigations
└── reviews/           # PR review reports
```

---

## PRD Phases

PRDs include an Implementation Phases table for tracking progress:

```markdown
| #   | Phase | Description | Status      | Parallel | Depends | PRP Plan |
| --- | ----- | ----------- | ----------- | -------- | ------- | -------- |
| 1   | Auth  | User login  | complete    | -        | -       | [link]   |
| 2   | API   | Endpoints   | in-progress | -        | 1       | [link]   |
| 3   | UI    | Frontend    | pending     | with 4   | 2       | -        |
| 4   | Tests | Test suite  | pending     | with 3   | 2       | -        |
```

- **Status**: `pending` → `in-progress` → `complete`
- **Parallel**: Phases that can run concurrently (in separate worktrees)
- **Depends**: Phases that must complete first

---

## PRP Best Practices

1. **Context is King**: Include ALL necessary documentation, examples, and caveats
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the codebase
4. **Bounded Scope**: Each plan should be completable by an AI in one loop

---

## Project Structure

```text
your-project/
├── .github/
│   ├── prompts/             # PRP commands
│   ├── PRPs/                # Generated artifacts
│   ├── agents/              # Custom subagents
│   └── skills/              # Agents skills
├── PRPs/
│   ├── templates/           # PRP templates
│   └── ai_docs/             # Library documentation
├── AGENTS.md                # Project-specific guidelines
└── src/                     # Your source code
```

---

## Parallel Development with Worktrees

When PRD phases can run in parallel:

```console
# Phase 3 and 4 can run concurrently
git worktree add -b phase-3-ui ../project-phase-3
git worktree add -b phase-4-tests ../project-phase-4

# Run Claude in each
cd ../project-phase-3 && claude
cd ../project-phase-4 && claude
```

---

## Resources

### Templates (PRPs/templates/)

- `prp_base.md` - Comprehensive PRP template
- `prp_story_task.md` - Story/task template
- `prp_planning.md` - Planning template

### AI Documentation (PRPs/ai_docs/)

Curated documentation for Github CoPilot context injection.

### Legacy Commands

Previous command versions are preserved in `old-prp-commands/` for reference.

---

## License

MIT License

---

**The goal is one-pass implementation success through comprehensive context.**
