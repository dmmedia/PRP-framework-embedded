# The PRP Methodology

## Critical Success Patterns

1. **Context is King**: Include ALL necessary documentation, examples, and gotchas.
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix autonomously.
3. **Information Density**: Use specific keywords and patterns established in the codebase.
4. **Progressive Success**: Start simple, validate the foundation, then enhance.

## PRP Structure Requirements

A valid PRP must contain:

- **Goal**: Specific end state and desired outcome.
- **Why**: Business value and user impact.
- **What**: User-visible behavior and technical requirements.
- **Context**: Documentation URLs, code examples, gotchas, and patterns.
- **Implementation Blueprint**: Detailed pseudocode and task lists.
- **Validation Loop**: Executable commands for syntax, tests, integration.

## Validation Gates (Must be Executable)

1. **Syntax & Style**:
   - **Python**: `uv run ruff check --fix && uv run mypy .`
   - **Markdown**: use `markdown-linter` skill.
2. **Unit Tests**: `uv run pytest tests/ -v`
3. **Integration**: `uv run uvicorn main:app --reload` followed by API calls `curl -X POST http://localhost:8000/endpoint -H "Content-Type: application/json" -d '{...}'`
4. **Deployment**: MCP servers or creative self-validation methods.

## Anti-Patterns to Avoid

- **Minimal Context**: Never provide bare prompts. Context is everything; the PRP must be self-contained.
- **Skipping Validation**: Validation is critical for one-pass success. The better the AI runs the loop, the higher the success rate.
- **Ignoring Structure**: Do not deviate from the battle-tested structured PRP format.
- **Redundant Patterns**: Use existing templates rather than creating new patterns unnecessarily.
- **Hardcoding**: Avoid hardcoded values that belong in configuration.
- **Generic Exceptions**: Do not use "catch-all" exception handling; be specific.

## Working with This Framework

### When Creating new PRPs

1. **Context Assembly**: Gather documentation, code examples, and patterns. Context is King!
2. **Blueprint Development**: Draft a detailed Implementation Blueprint with pseudocode and task lists.
3. **Validation Mapping**: Define executable commands (syntax, tests, integration) for the Validation Loop.

### When Executing PRPs (Agent Instructions)

1. **Load PRP**: Read and understand all context and requirements.
2. **Think**: (Reasoning Step) Create a comprehensive plan, break it down into todos, use subagents, and check `.github/PRPs/ai_docs/`.
3. **Execute**: Implement following the provided blueprint.
4. **Validate**: Run every validation command; fix failures immediately.
5. **Complete**: Ensure every checklist item is verified as "done".
