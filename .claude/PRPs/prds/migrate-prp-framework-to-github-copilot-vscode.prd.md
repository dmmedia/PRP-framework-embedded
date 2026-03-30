# Migrate PRP Framework to GitHub Copilot + VS Code

## Problem Statement

The repository and PRP framework are tightly coupled to "Claude Code" (Anthropic) tooling: CLI calls, `.claude/` conventions, and many prompt templates and docs reference Claude-specific commands. This prevents teams using GitHub Copilot and Visual Studio Code from adopting the PRP workflow without manual translation, leading to onboarding friction, automation breakage, and duplicated documentation.

## Evidence

- [CLAUDE.md](CLAUDE.md#L1-L30): root guide explicitly written for "Claude Code" and `.claude/commands/`.
- `claude_md_files/` contains multiple language-specific CLAUDE guides (e.g., CLAUDE-PYTHON-BASIC.md, CLAUDE-REACT.md) that assume Claude tooling.
- `.github/prompts/`, `plugins/prp-core/`, and `PRPs/scripts/` include scripts that shell out to a `claude` CLI and expect `.claude/*` state files.
- Example runtime entrypoints discovered: `.github/PRPs/scripts/invoke_command.py` and `.github/PRPs/scripts/prp_workflow.py` which call the `claude` binary.
- `.github/agents/` contains Claude specific AI model selection.

If these artifacts are not migrated, VS Code + Copilot users cannot run PRP workflows natively.

## Proposed Solution

Create a migration that replaces Claude-specific runtime and documentation with GitHub Copilot + Visual Studio Code specifics. Deliverables:
- An adapter layer (e.g., `invoke_copilot.py`) that maps existing command templates to Copilot Chat or Copilot CLI invocations, used by `prp_workflow.py` and related scripts.
- Re-author prompt templates as Copilot Chat-compatible prompts and store them in a discoverable location (e.g., `.github/prompts/`).
- Add VS Code workspace integration: `.vscode/extensions.json`, `.vscode/settings.json`, and optionally a small extension to register command-palette entries that call Copilot Chat with prefilled prompts.
- Update documentation: create `AGENTS.md` guide with the same intent as `CLAUDE.md`, but adapted for Copilot, update `README.md`, and migrate language-specific guides from `claude_md_files/` to show Copilot + VS Code workflows.
- Every Claude agent guide in `claude_md_files/CLAUDE-*.md` must have a Copilot/VS Code equivalent in `copilot_md_files/`, with the similar structure and conventions, updated for Copilot workflows.
- Add a deprecation header to each legacy Claude guide, referencing the new Copilot equivalent.
- Provide a compatibility/feature-flag (e.g., `PRP_TOOL_ADAPTER=claude|copilot`) to allow incremental migration and rollback.

## Key Hypothesis

We believe providing a lightweight adapter plus VS Code integration will make the PRP workflow usable for VS Code + Copilot users and reduce context switching. We'll know we're right when at least 80% of core PRP workflows can be executed from VS Code (without invoking a `claude` binary) and on-board time for a new developer falls below 60 minutes in our checklist.

## What We're NOT Building

- `old-prp-commands/` — explicitly excluded from migration (kept for historical reference).  
- Full feature parity for proprietary Claude-only behaviours — where parity is impossible, we'll provide a documented manual step or compatibility shim.

## Success Metrics

| Metric | Target | How Measured |
|--------|--------|--------------|
| Number of files referencing "Claude" | 0 (or archived) | `git grep -i claude` automated check |
| % core PRP workflows runnable from VS Code | >= 80% | runtime integration tests + manual verification |
| New developer onboarding time | < 60 minutes | onboarding checklist & timed trial |

## Open Questions

- [x] Does the organization have Copilot / Copilot Chat entitlements for CI/automation? — Answer: This PRP framework is intentionally generic and supports use with either personal or organization GitHub accounts, and with free or paid Copilot subscriptions. The framework assumes only that Copilot (the extension or service) is available to users, but it does NOT assume organization-level entitlements for CI/automation. Any CI-level automation that requires service/machine accounts, Copilot CLI access, or paid seats must be implemented as optional components and documented as requiring additional entitlements.
- [x] Which `prp-*` commands are critical for v1? — Answer: The critical commands for v1 are `prp-prd`, `prp-plan`, and `prp-implement`. These cover the core PRP lifecycle: PRD creation, plan generation, and implementation/execution. The adapter, prompt templates, and docs should prioritize these flows and include tests verifying end-to-end behavior.
- [x] Do we prefer renaming directories (e.g., `claude_md_files/` → `copilot_md_files/`) or keeping them for a transition period? — Answer: Keep the directories for a transition period. Create a new `copilot_md_files/` for Copilot-specific guidance, add a clear deprecation header to existing `claude_md_files/*` pointing to the new location, and prefer the new path in updated docs and adapter while falling back to the legacy path for compatibility. Schedule removal of legacy files after a defined transition window (suggestion: 1–2 releases) once CI, plugins, and consumers have migrated.

---

## Users & Context

**Primary User**
- **Who**: VS Code-based developer or engineering PM using GitHub Copilot in a code-first workflow with personal or organization accounts and with free or paid Copilot subscriptions and does not assume CI/automation entitlements.  
- **Current behavior**: They must run shell scripts or external CLIs (e.g., `claude`) or follow Claude-specific docs to execute PRP flows.  
- **Trigger**: Need to create or execute a PRP (PRD → plan → implementation) from their local dev environment.  
- **Success state**: Can run create/execute/commit PRP flows entirely from within VS Code using Copilot-assisted prompts and workspace commands.

**Job to Be Done**
When I need to run the PRP workflow, I want to invoke it from VS Code with Copilot assistance, so I can stay in context and deliver validated changes faster.

**Non-Users**
Owners of `old-prp-commands/` (historical scripts) — these are intentionally not migrated.

---

## Solution Detail

### Core Capabilities (MoSCoW)

| Priority | Capability | Rationale |
|----------|------------|-----------|
| Must | Adapter to map existing command templates to Copilot/VS Code | Enables runtime migration without breaking existing templates |
| Must | Support 3 command-palette v1 commands (`prp-prd`, `prp-plan`, `prp-implement`) wired to Copilot Chat or adapter | Core developer flows must be available in VS Code, adapter, prompt templates, command palette, and tests |
| Must | Updated docs + `.vscode/extensions.json` | Onboarding and extension recommendations are essential |
| Should | Convert prompt templates to Copilot Chat-compatible prompts in `.github/prompts/` | Makes prompts discoverable to Copilot Chat and reusable |
| Could | Small VS Code extension that registers extra UI & telemetry | Improves discoverability and integration |
| Should | Keep legacy docs during transition | Retain `claude_md_files/` and `CLAUDE.md`, introduce `copilot_md_files/` and `AGENTS.md` to minimize disruption during migration |
| Must | Interactive fallback mode | Adapter must work without CI entitlements; CI automation optional |
| Won't | Migrate `old-prp-commands/` | Historical; out of scope per requirements |

### MVP Scope

The minimum to validate the hypothesis: 1) `invoke_copilot.py` adapter, 2) wire `prp_workflow.py` to adapter, 3) document three core flows in `README.md`, 4) add `.vscode/extensions.json` recommending Copilot extensions 5) create `copilot_md_files/` with one-to-one migrated guides, following the same structure and conventions, while adding deprecation headers to legacy `claude_md_files/` and, 6) create `AGENTS.md` with the migrated agent guide content from `CLAUDE.md` adapted for Copilot.

### User Flow

1. Developer opens the workspace in VS Code.  
2. From the command palette, they choose `PRP: Create PRD` (registered command).  
3. Copilot Chat opens with a prefilled context and template prompt (or the adapter triggers Copilot CLI).
4. The adapter writes PRP artifacts to `.github/PRPs/prds/`.  
5. Developer reviews results and uses `PRP: Plan` to create an implementation plan (from PRD or free-form input).
6. The adapter writes plan artifacts to `.github/PRPs/plans/`.
7. Developer reviews results and uses `PRP: Implement` to execute a plan with validation loops.
8. Upon successful implementation, after running tests and creating or updating documentation, the adapter moves the implementation plan from `.github/PRPs/plans/` to `.github/PRPs/plans/completed/`.

---

## Technical Approach

**Feasibility**: MEDIUM — Documentation and templates are straightforward to update, but runtime parity requires adapting flows to Copilot Chat/CLI patterns and validating authentication and enterprise constraints.

**Architecture Notes**
- Add adapter module `PRPs/scripts/invoke_copilot.py` that: 1) accepts a command template and context, 2) calls Copilot Chat via VS Code command or Copilot CLI, 3) returns output to the workflow.  
- Add `.vscode/extensions.json` (recommend `GitHub.copilot`, `GitHub.copilot-chat`, `GitLens`, `GitHub.vscode-pull-request-github`).  
- Make `.claude` paths configurable (via `PRP_TOOL_WORKDIR` or `PRP_TOOL_ADAPTER`) for gradual migration.
- The adapter must support an interactive/manual fallback mode when CI/automation entitlements are not available; optional CI integrations should be gated behind configuration and feature flags.
- Adapter responsibilities (v1): map `prp-prd`, `prp-plan`, and `prp-implement` to Copilot Chat or Copilot CLI invocations; produce the same PRP artifact layout (`.claude/PRPs/*` or configurable path) and include end-to-end tests that validate generated PRD, plan, and implementation artifacts.
- Provide a docs-mapping shim and fallback: adapters and tooling should prefer `copilot_md_files/` for new content but support a mapping or lookup that resolves legacy `claude_md_files/` paths to the new location. Include a small `docs_map.json` or script to maintain compatibility during the transition.
- Only agent/technology-specific guides go in `copilot_md_files/`.
- No human-facing guides should remain in `copilot_md_files/`—these are for agent/technology-specific content only.
- All human-facing documents should be placed in the project root.

**Technical Risks**

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Copilot auth/entitlement not present in org | H | Validate and document required entitlements; provide a limited local adapter mode (manual prompts) |
| Prompt output differs from Claude (behavior drift) | M | Add validation gates and acceptance tests; iteratively tune prompts |
| No programmatic REST API for chat workflows outside VS Code | M | Use `vscode.commands.executeCommand` inside extension or Copilot CLI for automation |

---

## Implementation Phases

| # | Phase | Description | Status | Parallel | Depends | PRP Plan |
|---|-------|-------------|--------|----------|---------|----------|
| 1 | Inventory & design | Full grep of Claude artifacts and design adapter API | complete | - | - | - |
| 2 | Adapter scaffold | Implement `invoke_copilot.py` adapter and minimal integration | complete | - | 1 | .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-2-v-2.plan.md |
| 3 | Docs & prompts | Write `AGENTS.md` based on `CLAUDE.md` and convert guides from `claude_md_files/` | complete | - | 2 | .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-3.plan.md |
| 4 | VS Code integration | Add `.vscode` settings, `extensions.json`, and register command-palette entries (small extension or tasks) | complete | with 5 | 2 | .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-4.plan.md |
| 5 | Hooks & plugins update | Update `plugins/prp-core` hooks to use configurable workdir and adapter env vars | complete | with 4 | 2 | .claude/PRPs/plans/completed/migrate-prp-framework-to-github-copilot-vscode-phase-5.plan.md |
| 6 | Remaining agent guides | Migrate remaining agent guides from `claude_md_files/` to `copilot_md_files/` with deprecation headers in legacy files | in-progress | - | 3 | .claude/PRPs/plans/migrate-prp-framework-to-github-copilot-vscode-phase-6.plan.md |

### Phase Details

**Phase 1: Inventory & design**
- **Goal**: Identify all Claude-specific files and define adapter contract.  
- **Scope**: File inventory and migration priority list, plus entitlements validation and fallback strategy.  
- **Success signal**: List of files + adapter API design approved; entitlements validation and fallback strategy defined.

**Phase 2: Adapter scaffold**
- **Goal**: Provide a drop-in adapter that accepts existing templates and returns results from Copilot Chat/CLI.  
- **Scope**: `PRPs/scripts/invoke_copilot.py` + tests for `prp-prd`, `prp-plan`, and `prp-implement` mappings; include support for interactive fallback when CI/automation entitlements are not available.  
- **Success signal**: Adapter supports interactive fallback and `prp_workflow.py` can run `prp-prd`, `prp-plan`, and `prp-implement` via the adapter locally.

**Phase 3: Docs & prompts**
- **Goal**: Update user-facing docs, prompt templates, and examples to Copilot + VS Code idioms.  
- **Scope**: Copy/convert `CLAUDE.md` to `AGENTS.md` retaining the guide structure, updates to `README.md`, create `copilot_md_files/` and copy/convert three language guides from `claude_md_files/` into it, add deprecation headers to the legacy `claude_md_files/` entries, and update references in top-level docs, templates, and adapters.
- **Deliverables**:
  - Create `copilot_md_files/` and migrate three representative guides (e.g., Python, Node, React).  
  - Add a deprecation header to each file in `claude_md_files/` pointing to the new location and the migration schedule.
  - Update top-level `README.md` and `CLAUDE.md` to reference new docs and include a migration note.  
  - Provide a `docs_map.json` or small mapping script and update the adapter to consult it for legacy→new resolution.

**Phase 4: VS Code integration**
- **Goal**: Make PRP flows discoverable and runnable from VS Code.  
- **Scope**: `.vscode/extensions.json`, `.vscode/settings.json`, and a minimal extension or tasks to register command-palette entries.

**Phase 5: Hooks & plugin updates**
- **Goal**: Update plugin hooks to use configurable adapter paths and ensure backward compatibility.  

**Phase 6: Remaining agent guides**
- **Goal**: Migrate remaining agent guides from `claude_md_files/` to `copilot_md_files/` following the same structure and conventions, adapted to Copilot, with deprecation headers in legacy files. Also migrate `CLAUDE.md` to `AGENTS.md` with the same approach. Check that initially migrated guides have proper content and update them as needed to achieve success signal.
- **Scope**: Files located in `claude_md_files/` that are agent/technology specific. Destination folder is `copilot_md_files/`. Files should be migrated one-to-one, maintaining the same structure and conventions, but updated to reflect Copilot workflows and capabilities. `CLAUDE.md` is located in the root and should be migrated to `AGENTS.md` also located in the root and following the same approach as the files from `claude_md_files/`.
- **Success signal**: All agent guides have Copilot equivalents in `copilot_md_files/`, with deprecation headers in legacy files, and all references updated to prefer the new location. `AGENTS.md` is created as the new root agent guide, with `CLAUDE.md` updated to reference it and marked as deprecated. All new guides have about similar file size, but the content is updated to reflect Copilot workflow and capabilities.

### Parallelism Notes

Phases 3 and 4 can run in parallel (docs + VS Code integration) since they touch onboarding and UI respectively and do not require the adapter to be fully feature-complete.

---

## Decisions Log

| Decision | Choice | Alternatives | Rationale |
|----------|--------|--------------|-----------|
| Adapter vs rename | Adapter with feature-flag | Full rename of `claude_*` → `copilot_*` | Adapter preserves backward compatibility and enables incremental migration |
| Copilot entitlements assumption | Assume only Copilot availability; do not assume CI/automation entitlements | Require org admins to provision CI seats and machine accounts for automation | Keeps framework broadly usable across personal and org accounts; CI automation implemented opt-in |
| v1 commands | `prp-prd`, `prp-plan`, `prp-implement` | Implement all `prp-*` commands | Prioritize the minimal end-to-end PRD → Plan → Implement flow to validate the approach quickly |
| Directory rename approach | Keep legacy `claude_md_files/` during transition; create `copilot_md_files/` | Full rename | Minimizes disruption and preserves compatibility while migration proceeds |

---

## Research Summary

**Market Context**
- GitHub Copilot (Copilot and Copilot Chat) provides the natural VS Code integration for agent-driven workflows; Copilot CLI enables scripted/autonomous runs. (See Copilot Chat marketplace and Copilot CLI docs.)  
- Recommended extensions: `GitHub.copilot`, `GitHub.copilot-chat`, `GitHub.vscode-pull-request-github`, `eamodio.gitlens`.

**Technical Context**
- Key files to update (sample):  
  - `.github/PRPs/scripts/invoke_command.py` — calls `claude` binary (replace with adapter).  
  - `.github/PRPs/scripts/prp_workflow.py` — orchestrator to point to adapter.  
  - `CLAUDE.md`, `claude_md_files/*` — agent guides to replace.  
  - `plugins/prp-core/hooks/*` and `plugins/prp-core/commands/*` — many references to `.claude`.  
- Primary technical risks: auth/entitlements, prompt drift, and automation surface mismatch between Claude APIs and Copilot extension/CLI.
- Priority mapping note: the migration should prioritize support for `prp-prd` (PRD generation), `prp-plan` (plan generation), and `prp-implement` (implementation) as the minimal end-to-end validation surface for Copilot/VS Code adapters.
- Agent guides rename approach: staged transition — create `copilot_md_files/` for new Copilot-specific guides, copy/convert the key guides, add deprecation headers to `claude_md_files/`, and update adapters/docs to prefer the new location. Remove legacy files after a short, announced transition window (1–2 releases).

**Entitlements note**: This framework is intentionally license-agnostic and designed to work with personal or organization accounts and with free or paid Copilot subscriptions. The PRP core assumes only that Copilot access exists for interactive users; it does not assume organization-level entitlements for CI/automation. Any automation requiring seats, machine/service accounts, or Copilot CLI access must be implemented as optional, clearly documented components and gated behind configuration and feature flags.

---

*Generated: 2026-03-29T18:21:11Z*
*Status: DRAFT - needs validation*
