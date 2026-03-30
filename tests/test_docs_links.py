from pathlib import Path


def test_readme_includes_agents_and_copilot_paths():
    text = Path("README.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in text
    assert "copilot_md_files" in text


def test_claude_includes_agents_link():
    text = Path("CLAUDE.md").read_text(encoding="utf-8")
    assert "AGENTS.md" in text
