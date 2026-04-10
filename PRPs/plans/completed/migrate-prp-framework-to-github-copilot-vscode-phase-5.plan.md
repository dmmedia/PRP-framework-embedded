# Feature: Phase 5 – Hooks & plugin updates

## Summary

Implement the Phase 5 migration step: update plugin hooks and PRP workflow hook integration so `plugins/prp-core` and workflow scripts use a configurable adapter and working directory. This enables Copilot/VS Code path adoption while preserving legacy Claude fallback and existing automation paths.

## User Story

As a Copilot/VS Code user
I want plugin hook and adapter path configuration to be pluggable via environment variables (`PRP_TOOL_ADAPTER`, `PRP_TOOL_WORKDIR`, `COPILOT_PLUGIN_ROOT`, `CLAUDE_PLUGIN_ROOT`)
So that I can run PRP workflows seamlessly from VS Code without manual `.claude` path edits.

## Problem Statement

Current hook paths and workflow adapters are hardcoded for `.claude` and `claude`, creating friction for Copilot users and locking out alternative tooling. This step must make plugin hooks and workflow scripts configurable, safe, backward-compatible, and test-covered.

## Solution Statement

Add a configuration layer in `plugins/prp-core/hooks/hooks.json` and `PRP` scripts (`prp_workflow.py`, `invoke_command.py`, `invoke_copilot.py`) to read adapter/workdir env vars, apply fallback rules, and prefer Copilot when configured. Mirror existing patterns in command structure, error handling, and signposted branch support.

## Metadata

| Field | Value |
| --- | --- |
| Type | ENHANCEMENT |
| Complexity | MEDIUM |
| Systems Affected | PRP workflow orchestration, plugin hooks, adapter selection, environment configuration |
| Dependencies | `PRP_TOOL_ADAPTER` env (copilot/claude), `PRP_TOOL_WORKDIR`, `.claude` path defaults |
| Estimated Tasks | 8 |

---

## UX Design

### Before State
```
╔════ BEFORE STATE ═══════════════════════════════════╗
║                                                 ║
║  User runs `uv run .github/PRPs/scripts/prp_workflow.py`  ║
║  └─ uses hardcoded `.claude` workspace + claude adapter
║  └─ `invoke_command` choosess claude adapter by default
║  └─ hooks in `plugins/prp-core/hooks/hooks.json` use `${CLAUDE_PLUGIN_ROOT}`
║                                                 ║
╚═════════════════════════════════════════════════╝

USER_FLOW: run PRP workflow command → hardcoded adapter+path → CLI fails for copilot-only guests
PAIN_POINT: poor Copilot integration and no automatic fallback
DATA_FLOW:
- `prp_workflow.py` sets `PRP_TOOL_ADAPTER` (claude fallback)
- `invoke_command.py` resolves `command_path` under `.claude`
- hook commands in `hooks.json` refer to CLAUDE_PLUGIN_ROOT
```

### After State
```
╔════ AFTER STATE ═══════════════════════════════════╗
║                                                 ║
║  User sets `PRP_TOOL_ADAPTER=copilot` and/or `PRP_TOOL_WORKDIR=.copilot` ║
║  └─ workflow uses those variables with safe fallbacks
║  └─ plugin hooks use `${COPILOT_PLUGIN_ROOT}` first, then `${CLAUDE_PLUGIN_ROOT}`
║  └─ existing workflows still work via `claude` default
║                                                 ║
╚═════════════════════════════════════════════════╝

USER_FLOW: set env vars or use CLI `--adapter copilot` → run `prp_workflow.py` → adapter uses `invoke_copilot.py`
VALUE_ADD: Copilot users can operate end-to-end with minimal config change
DATA_FLOW:
- `prp_workflow.py` reads `--adapter` and sets `PRP_TOOL_ADAPTER`
- `invoke_command.py` picks adapter and uses resolved workdir
- hooks lookup uses `COPILOT_PLUGIN_ROOT` through existing fallback
```

### Interaction Changes
| Location | Before | After | User Impact |
|---|---|---|---|
| `.github/PRPs/scripts/prp_workflow.py` | `--adapter` default `claude` | explicit adapter support w/ env fallback | enables `copilot` command path |
| `.github/PRPs/scripts/invoke_command.py` | fixed `.claude` commands path | same but with `PRP_TOOL_WORKDIR` optional override | flexible workdir integration |
| `plugins/prp-core/hooks/hooks.json` | `${COPILOT_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}` | same; verify plugin root env vars exposed | supports existing and new plugin roots |
| `PRPs/scripts/test_invoke_command.py` | tests adapter fallback | add workdir+adapter tests | ensures behavior does not regress |

---

## Mandatory Reading

| Priority | File | Lines | Why Read This |
| P0 | `.github/PRPs/scripts/invoke_command.py` | 1-220 | Existing adapter selection + command invocation pattern |
| P0 | `.github/PRPs/scripts/prp_workflow.py` | 1-280 | workflow orchestration and env propagation |
| P1 | `plugins/prp-core/hooks/hooks.json` | 1-22 | Hook adapter paths + migration flags |
| P1 | `PRPs/scripts/test_invoke_command.py` | 1-80 | Adapter tests to mirror |

**External Documentation:**
| Source | Section | Why Needed |
| [GitHub Copilot CLI docs](https://docs.github.com/en/copilot/cli) | `PRP_TOOL_ADAPTER` CLI patterns | ensure adapter invocation is compatible |
| [VS Code extension API](https://code.visualstudio.com/api) | `commands.executeCommand` | maybe used for later phase extension hook behavior |

---

## Patterns to Mirror

**NAMING_CONVENTION:**
```python
# SOURCE: .github/PRPs/scripts/invoke_command.py:21-29
# COPY THIS PATTERN:
adapter = os.getenv("PRP_TOOL_ADAPTER", "claude").strip().lower()
if adapter not in {"claude", "copilot"}:
    print(... fallback to claude ...)
    return "claude"
```

**ERROR_HANDLING:**
```bash
# SOURCE: plugins/prp-core/hooks/prp-ralph-stop.sh:13-18
if [[ ! -f "$STATE_FILE" ]]; then
  echo "..." >&2
  exit 0
fi
```

**LOGGING_PATTERN:**
```python
# SOURCE: .github/PRPs/scripts/prp_workflow.py:55-60
print(f"→ Running: {command_name} {arguments} (adapter: {adapter})", file=sys.stderr)
```

**REPOSITORY_PATTERN:**
```json
# SOURCE: plugins/prp-core/hooks/hooks.json:5-18
"command": "${COPILOT_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}/hooks/prp-ralph-stop.sh"
```

**SERVICE_PATTERN:**
(phase does not create a new service; focus on config + adapter integration)

**TEST_STRUCTURE:**
```python
# SOURCE: PRPs/scripts/test_invoke_command.py:42-63
@mock.patch.object(ic.subprocess, "run")
def test_invoke_command_copilot_mode(self, mock_run):
    os.environ["PRP_TOOL_ADAPTER"] = "copilot"
    ...
    self.assertIn("invoke_copilot.py", " ".join(str(x) for x in called))
```

---

## Files to Change

| File | Action | Justification |
| --- | --- | --- |
| `.github/PRPs/scripts/prp_workflow.py` | UPDATE | expose `--adapter`, preserve backward-compatible `PRP_TOOL_ADAPTER` and set default vs fallback |
| `.github/PRPs/scripts/invoke_command.py` | UPDATE | add `PRP_TOOL_WORKDIR` override for command path resolution and enforce adapter set |
| `plugins/prp-core/hooks/hooks.json` | VERIFY/UPDATE | ensure `COPILOT_PLUGIN_ROOT`/`CLAUDE_PLUGIN_ROOT` path fallback is tested and documented |
| `PRPs/scripts/test_invoke_command.py` | UPDATE | add regression test for `PRP_TOOL_WORKDIR` and `PRP_TOOL_ADAPTER=copilot` semantics |
| `.vscode/settings.json` | UPDATE (if exists) | optional default for adapter tools in workspace: `PRP_TOOL_ADAPTER`: `copilot` |
| `README.md` | UPDATE | document Phase 5 behavior and env vars |

---

## NOT Building (Scope Limits)

- full hook runtime engine (non-required plugin engine hosting) is out of scope; only config and path selection.
- extension command palette implementation is not required in this phase (Phase 4 coverage). 

---

## Step-by-Step Tasks

### Task 1: Update `invoke_command.py` for workdir override
- ACTION: implement `PRP_TOOL_WORKDIR` support.
- MIRROR: `.github/PRPs/scripts/invoke_command.py` pattern.
- IMPLEMENT:
  - supported envs: `PRP_TOOL_WORKDIR`, `PRP_TOOL_ADAPTER`.
  - `ROOT = Path(os.getenv("PRP_TOOL_WORKDIR", Path(__file__).resolve().parents[4]))` or similar.
  - in `resolve_command_path`, use `workdir / ".claude" / "commands"` as base.
  - add warning if computed command does not exist.
- VALIDATE: `python -m pytest PRPs/scripts/test_invoke_command.py -k get_adapter` plus `npx tsc --noEmit` (if JS target; else run existing lint check). 

### Task 2: Update `prp_workflow.py` adapter behavior
- ACTION: preserve previous behavior while enabling new values.
- IMPLEMENT:
  - parser `--adapter`, default `os.getenv("PRP_TOOL_ADAPTER", "claude")`.
  - set `env["PRP_TOOL_WORKDIR"] = os.getenv("PRP_TOOL_WORKDIR", str(ROOT))` for subprocess invocation.
  - ensure `adapter` in `run_command(..., adapter=...)` is pageable.
- VALIDATE: run `uv run .github/PRPs/scripts/prp_workflow.py "test" --skip-create --no-commit --no-pr --adapter copilot` and confirm no failures in path resolution.

### Task 3: Evaluate/Update `plugins/prp-core/hooks/hooks.json` path fallback
- ACTION: no-code or minimal patch.
- IMPLEMENT:
  - verify using `COPILOT_PLUGIN_ROOT` plus fallback to `CLAUDE_PLUGIN_ROOT`.
  - add doc comment in `.md` or the file in `plugins/prp-core/README.md`.
- VALIDATE: test with a tiny shell script setting `COPILOT_PLUGIN_ROOT` and running the hook from plugin runner (or unit tests if available).

### Task 4: Add regression test in `PRPs/scripts/test_invoke_command.py`
- ACTION: implement test for PRP_TOOL_WORKDIR and adapter path.
- IMPLEMENT:
  - create temporary directories (e.g., `tmp_path` fixture or `Path('tmp')`).
  - set `PRP_TOOL_WORKDIR` to temp path.
  - create fake `.claude/commands/prp-core-create.md` with content.
  - call `ic.resolve_command_path('prp-core-create')` and assert path is under custom workdir.
  - maintain existing `test_invoke_command_copilot_mode`.
- VALIDATE: run `pytest PRPs/scripts/test_invoke_command.py`

### Task 5: Update README/docs
- ACTION: include new env vars and Phase 5 status.
- IMPLEMENT: Add section in `README.md`, `.claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` already updated.
- VALIDATE: run markdown linter if any, or `grep -i "PRP_TOOL_WORKDIR" README.md`.

### Task 6: Verify hook scripts side effects and plug-in path compatibility
- ACTION: check `plugins/prp-core/hooks/prp-ralph-stop.sh` and `prp-research-team-stop.sh` continue to use `.claude` paths; document this dependency.
- IMPLEMENT: mention in plan, add optional code to read `PRP_TOOL_WORKDIR` in hook scripts.
- VALIDATE: manual script run unit test or best-effort.

### Task 7: End-to-end execution test for phase 5
- ACTION: run end-to-end instructive command with `POC` config.
- IMPLEMENT:
  - set env: `PRP_TOOL_ADAPTER=copilot`, `PRP_TOOL_WORKDIR=$(pwd)`.
  - run `uv run .github/PRPs/scripts/prp_workflow.py "phase5 test" --skip-create --no-commit --no-pr --adapter copilot`.
  - ensure it hits `invoke_command.py` and does not fail due missing `.claude` command path check.
- VALIDATE: command exit code 0 or a predictable support message.

### Task 8: Document plan completion and next staging
- ACTION: close Phase 5 by setting PRD row and plan file path (done in PRD); finalize this plan as a concrete artifact for 1-pass implementation.
- VALIDATE: confirm `grep -A2 "Phase 5" .claude/PRPs/prds/migrate-prp-framework-to-github-copilot-vscode.prd.md` shows in-progress and plan path.

---

## Testing Strategy

### Unit Tests to Write
| Test File | Test Cases | Validates |
| PRPs/scripts/test_invoke_command.py | PRP_TOOL_ADAPTER default, invalid fallback, `copilot` path invocation, `PRP_TOOL_WORKDIR` command resolution | Adapter selection, fallback, custom workdir behavior |

### Edge Cases Checklist
- [x] Missing `PRP_TOOL_ADAPTER` uses `claude`
- [x] Unsupported adapter value falls back to `claude` (and warns)
- [x] `PRP_TOOL_WORKDIR` points to non-existent path should fail fast with clear message
- [x] Existing `.claude` behavior should be unchanged
- [x] `plugin hooks` detect both `COPILOT_PLUGIN_ROOT` and `CLAUDE_PLUGIN_ROOT`

---

## Validation Commands

### Level 1: STATIC_ANALYSIS
```bash
uv run lint && uv run type-check
``` 

### Level 2: UNIT_TESTS
```bash
python -m pytest PRPs/scripts/test_invoke_command.py
``` 

### Level 3: FULL_SUITE
```bash
uv run test && uv run build
``` 

### Level 4: DATABASE_VALIDATION
- Not applicable for this migration phase.

### Level 5: BROWSER_VALIDATION
- Not applicable for this phase.

### Level 6: MANUAL_VALIDATION
1. `export PRP_TOOL_ADAPTER=copilot`
2. `export PRP_TOOL_WORKDIR=$(pwd)`
3. `uv run .github/PRPs/scripts/prp_workflow.py "test" --skip-create --no-commit --no-pr --adapter copilot`
4. confirm logs show `adapter: copilot` and no hardcoded `.claude` failure.

---

## Acceptance Criteria
- [x] Phase 5 row is `in-progress` in PRD and plan path set
- [x] `invoke_command.py` supports `PRP_TOOL_WORKDIR` command path resolution
- [x] `prp_workflow.py` continues to set `PRP_TOOL_ADAPTER` and adds `PRP_TOOL_WORKDIR` to subprocess env
- [x] `plugins/prp-core/hooks/hooks.json` path fallback documented and preserved
- [x] `PRPs/scripts/test_invoke_command.py` adds/keeps adapter and workdir tests
- [x] human docs updated in README and PRD
- [x] lint/type-check + unit tests pass
- [x] end-to-end command with `copilot` adapter works

---

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| adapter mismatch or misspelled `PRP_TOOL_ADAPTER` | LOW | MED | fallback to claude + clear warning msg |
| path resolution for command templates fails with customworkdir | MED | MED | explicit check with tests + clear error with example value |
| hook path variable expansion regression | LOW | MED | keep `${COPILOT_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT}}` and add test case |

---

## Notes
- This plan is explicitly tied to phase 5 of `migrate-prp-framework-to-github-copilot-vscode`.
- It assumes core Phase 4 adapter/logging code is already in place and Phase 6 is next.
- Confidence for one-pass: 8/10 with existing patterns in place and limited behavior changes.

