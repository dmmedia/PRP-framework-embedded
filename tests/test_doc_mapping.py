import json
from pathlib import Path


def test_docs_map_contains_all_legacy_claude_files():
    docs_map_path = Path("docs_map.json")
    assert docs_map_path.exists(), "docs_map.json should exist"

    docs_map = json.loads(docs_map_path.read_text(encoding="utf-8"))

    claude_files = sorted(p.name.replace(".md", "") for p in Path("claude_md_files").glob("CLAUDE-*.md"))
    mapped_keys = sorted(docs_map.keys())

    assert set(claude_files) == set(mapped_keys), f"Mapping keys mismatch: missing {set(claude_files)-set(mapped_keys)} extra {set(mapped_keys)-set(claude_files)}"


def test_docs_map_targets_exist():
    docs_map = json.loads(Path("docs_map.json").read_text(encoding="utf-8"))
    missing = []
    for key, target in docs_map.items():
        if not Path(target).exists():
            missing.append((key, target))
    assert not missing, f"Missing mapped files: {missing}"
