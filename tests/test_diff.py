"""Tests for okf/diff.py — bundle comparison."""

import json
from pathlib import Path


def test_diff_identical_bundles(tmp_path):
    """Two copies of the same bundle should have no differences."""
    from okf.generator import scan_codebase, write_bundle
    from okf.diff import diff_bundles
    src = Path(__file__).parent / "fixtures" / "sample_codebase"
    concepts = scan_codebase(src)
    write_bundle(concepts, tmp_path / "a", "sample", ["test"])
    write_bundle(concepts, tmp_path / "b", "sample", ["test"])
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["added"]) == 0
    assert len(result["removed"]) == 0
    assert len(result["changed"]) == 0


def test_diff_added_concept(tmp_path):
    """Adding a new concept file shows as added."""
    from okf.generator import scan_codebase, write_bundle
    from okf.diff import diff_bundles
    src = Path(__file__).parent / "fixtures" / "sample_codebase"
    concepts_a = scan_codebase(src)
    write_bundle(concepts_a, tmp_path / "a", "sample", ["test"])

    # Create a modified version with an extra concept
    import shutil
    shutil.copytree(tmp_path / "a", tmp_path / "b")
    fake = tmp_path / "b" / "new_func.md"
    fake.write_text("---\ntype: Function\ntitle: new_func\ndescription: A new function\nresource: new.py\n---\n\n# new_func\n")
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["added"]) == 1
    assert result["added"][0]["title"] == "new_func"


def test_diff_removed_concept(tmp_path):
    """Removing a concept file shows as removed."""
    from okf.generator import scan_codebase, write_bundle
    from okf.diff import diff_bundles
    src = Path(__file__).parent / "fixtures" / "sample_codebase"
    concepts = scan_codebase(src)
    write_bundle(concepts, tmp_path / "a", "sample", ["test"])

    import shutil
    shutil.copytree(tmp_path / "a", tmp_path / "b")
    # Remove the first concept file found
    md_files = list((tmp_path / "b").rglob("*.md"))
    for f in md_files:
        if f.name not in ("index.md", "log.md", "SUMMARY.md"):
            f.unlink()
            break
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["removed"]) == 1


def test_diff_changed_concept(tmp_path):
    """Modifying a concept's description shows as changed."""
    from okf.generator import scan_codebase, write_bundle
    from okf.diff import diff_bundles
    src = Path(__file__).parent / "fixtures" / "sample_codebase"
    concepts = scan_codebase(src)
    write_bundle(concepts, tmp_path / "a", "sample", ["test"])

    import shutil
    shutil.copytree(tmp_path / "a", tmp_path / "b")
    # Modify a concept file
    for f in (tmp_path / "b").rglob("*.md"):
        if f.name not in ("index.md", "log.md", "SUMMARY.md"):
            content = f.read_text()
            content = content.replace("description:", "description: MODIFIED-")
            f.write_text(content)
            break
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["changed"]) >= 1


def test_diff_json_output(tmp_path):
    """JSON output is valid and contains expected keys."""
    from okf.generator import scan_codebase, write_bundle
    from okf.diff import diff_bundles, fmt_json
    src = Path(__file__).parent / "fixtures" / "sample_codebase"
    concepts = scan_codebase(src)
    write_bundle(concepts, tmp_path / "a", "sample", ["test"])
    write_bundle(concepts, tmp_path / "b", "sample", ["test"])
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    raw = fmt_json(result)
    data = json.loads(raw)
    assert "old_count" in data
    assert "new_count" in data
    assert "added" in data
    assert "removed" in data
    assert "changed" in data


def test_diff_concept_hash_stable(tmp_path):
    """Same content produces same hash."""
    from okf.diff import _concept_hash
    c1 = {"description": "test", "sections": {"signature": "fn"}, "tags": ["a", "b"], "body_extra": {}}
    c2 = {"description": "test", "sections": {"signature": "fn"}, "tags": ["b", "a"], "body_extra": {}}
    assert _concept_hash(c1) == _concept_hash(c2)
    c3 = {"description": "other", "sections": {"signature": "fn"}, "tags": ["a", "b"], "body_extra": {}}
    assert _concept_hash(c1) != _concept_hash(c3)
