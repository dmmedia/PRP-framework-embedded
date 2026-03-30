from pathlib import Path


def test_claude_docs_have_deprecated_header():
    errors = []
    for i in Path("claude_md_files").glob("CLAUDE-*.md"):
        data = i.read_text(encoding="utf-8")
        first_nonempty = next((line for line in data.splitlines() if line.strip()), "")
        if "DEPRECATED" not in first_nonempty.upper():
            errors.append(i.name)
    assert not errors, f"Missing deprecation header in {errors}"
