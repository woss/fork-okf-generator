"""Tests for okf/diff.py — bundle comparison against real versioned projects."""

import json
from pathlib import Path

V1 = Path(__file__).parent / "fixtures" / "realworld" / "python" / "easy"
V2 = Path(__file__).parent / "fixtures" / "realworld" / "python" / "easy_v2"


def _scan_and_write(src, dest):
    from okf.generator import scan_codebase, write_bundle
    concepts = scan_codebase(src)
    write_bundle(concepts, dest, "project", ["test"])
    return concepts


def test_diff_identical_bundles(tmp_path):
    """Two copies of the same bundle should have no differences."""
    from okf.diff import diff_bundles
    _scan_and_write(V1, tmp_path / "a")
    _scan_and_write(V1, tmp_path / "b")
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["added"]) == 0
    assert len(result["removed"]) == 0
    assert len(result["changed"]) == 0


def test_diff_v1_to_v2_adds_concepts(tmp_path):
    """Diff between v1 and v2 shows added concepts (new function, new file)."""
    from okf.diff import diff_bundles
    _scan_and_write(V1, tmp_path / "a")
    _scan_and_write(V2, tmp_path / "b")
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["added"]) >= 2, f"Expected >=2 added, got {len(result['added'])}"
    added_titles = [c["title"] for c in result["added"]]
    assert "batched" in added_titles, f"batched not in added: {added_titles}"
    assert "validate_email" in added_titles, f"validate_email not in added: {added_titles}"


def test_diff_v1_to_v2_changes_concepts(tmp_path):
    """Diff between v1 and v2 shows changed concepts (module doc updated)."""
    from okf.diff import diff_bundles
    _scan_and_write(V1, tmp_path / "a")
    _scan_and_write(V2, tmp_path / "b")
    result = diff_bundles(tmp_path / "a", tmp_path / "b")
    assert len(result["changed"]) >= 1, f"Expected >=1 changed, got {len(result['changed'])}"


def test_diff_json_output(tmp_path):
    """JSON output is valid and contains expected keys."""
    from okf.diff import diff_bundles, fmt_json
    _scan_and_write(V1, tmp_path / "a")
    _scan_and_write(V1, tmp_path / "b")
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
