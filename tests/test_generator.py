"""Tests for okf.generator — scan, write, summary."""

import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures" / "sample_codebase"


@pytest.fixture
def bundle_dir(tmp_path):
    """Generate a fresh OKF bundle into a temp dir."""
    from okf.generator import scan_codebase, write_bundle, write_summary, _dedup_concept_ids
    concepts = scan_codebase(FIXTURES)
    concepts = _dedup_concept_ids(concepts)
    write_bundle(
        concepts=concepts,
        output_dir=tmp_path,
        bundle_name="sample",
        log_entries=["test run"],
    )
    write_summary("sample", concepts, tmp_path, {})
    return tmp_path, concepts


# ── scan_codebase ────────────────────────────────────────────────────────────

def test_scan_finds_concepts():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    assert len(concepts) > 0


def test_scan_finds_python_functions():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    funcs = [c for c in concepts if c.type == "Function"]
    names = [c.title for c in funcs]
    assert "add" in names
    assert "greet" in names


def test_scan_finds_python_classes():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    classes = [c for c in concepts if c.type == "Class"]
    names = [c.title for c in classes]
    assert "Calculator" in names
    assert "WorldBankConnector" in names


def test_scan_extracts_docstrings():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    calc = next((c for c in concepts if c.title == "Calculator"), None)
    assert calc is not None
    assert "calculator" in calc.description.lower() or "calculator" in calc.docstring.lower()


def test_scan_extracts_signatures():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    add_fn = next((c for c in concepts if c.title == "add" and c.type == "Function"), None)
    assert add_fn is not None
    assert "def add" in add_fn.signature
    assert "int" in add_fn.signature


def test_scan_extracts_params():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    add_fn = next((c for c in concepts if c.title == "add" and c.type == "Function"), None)
    assert add_fn is not None
    param_names = [p["name"] for p in add_fn.params]
    assert "a" in param_names
    assert "b" in param_names


def test_scan_extracts_return_type():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    add_fn = next((c for c in concepts if c.title == "add" and c.type == "Function"), None)
    assert add_fn is not None
    assert add_fn.returns == "int"


def test_scan_concept_ids_are_path_based():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    for c in concepts:
        # concept_id must not use old flat layout
        assert not c.concept_id.startswith("functions/"), f"Old layout: {c.concept_id}"
        assert not c.concept_id.startswith("classes/"),   f"Old layout: {c.concept_id}"
        assert not c.concept_id.startswith("modules/"),   f"Old layout: {c.concept_id}"


def test_scan_tags_are_standardised():
    from okf.generator import scan_codebase
    concepts = scan_codebase(FIXTURES)
    for c in concepts:
        tag_str = " ".join(c.tags)
        assert "lang:" in tag_str, f"Missing lang: tag on {c.title}: {c.tags}"
        assert "type:" in tag_str, f"Missing type: tag on {c.title}: {c.tags}"


# ── write_bundle ─────────────────────────────────────────────────────────────

def test_bundle_creates_index(bundle_dir):
    tmp, _ = bundle_dir
    assert (tmp / "index.md").exists()


def test_bundle_creates_summary(bundle_dir):
    tmp, _ = bundle_dir
    assert (tmp / "SUMMARY.md").exists()


def test_bundle_creates_log(bundle_dir):
    tmp, _ = bundle_dir
    assert (tmp / "log.md").exists()


def test_bundle_layout_mirrors_source(bundle_dir):
    tmp, _ = bundle_dir
    # concept files should live under a path mirroring the source
    md_files = list(tmp.rglob("*.md"))
    non_index = [f for f in md_files if f.name not in {"index.md", "log.md", "SUMMARY.md"}]
    assert len(non_index) > 0


def test_bundle_concept_files_have_frontmatter(bundle_dir):
    tmp, _ = bundle_dir
    import yaml
    md_files = list(tmp.rglob("*.md"))
    non_index = [f for f in md_files if f.name not in {"index.md", "log.md", "SUMMARY.md"}]
    for f in non_index[:5]:   # check first 5
        text = f.read_text()
        assert text.startswith("---"), f"{f} missing frontmatter"
        parts = text.split("---", 2)
        fm = yaml.safe_load(parts[1])
        assert fm.get("type"), f"{f} missing type in frontmatter"
        assert fm.get("title"), f"{f} missing title in frontmatter"


def test_bundle_summary_has_domain_map(bundle_dir):
    tmp, _ = bundle_dir
    summary = (tmp / "SUMMARY.md").read_text()
    assert "## Domain Map" in summary
    assert "## Stats" in summary


# ── SUMMARY.md standalone ────────────────────────────────────────────────────

def test_write_summary_standalone(tmp_path):
    from okf.generator import scan_codebase, write_summary, _dedup_concept_ids
    concepts = scan_codebase(FIXTURES)
    concepts = _dedup_concept_ids(concepts)
    out = write_summary("sample", concepts, tmp_path, {})
    assert out.exists()
    content = out.read_text()
    assert "sample" in content
    assert "## Stats" in content
