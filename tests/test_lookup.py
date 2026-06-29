"""Tests for okf.lookup — load_bundle, search, formatters."""

import pytest
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures" / "sample_codebase"


@pytest.fixture(scope="module")
def bundle(tmp_path_factory):
    """Generate a bundle once for all lookup tests."""
    tmp = tmp_path_factory.mktemp("bundle")
    from okf.generator import scan_codebase, write_bundle, _dedup_concept_ids
    concepts = scan_codebase(FIXTURES)
    concepts = _dedup_concept_ids(concepts)
    write_bundle(concepts, tmp, "sample", ["test"])
    return tmp


# ── load_bundle ───────────────────────────────────────────────────────────────

def test_load_bundle_returns_concepts(bundle):
    from okf.lookup import load_bundle
    concepts = load_bundle(bundle)
    assert len(concepts) > 0


def test_load_bundle_skips_index_files(bundle):
    from okf.lookup import load_bundle
    concepts = load_bundle(bundle)
    types = {c["type"] for c in concepts}
    assert "Index" not in types
    assert "Log" not in types


def test_load_bundle_concept_has_required_fields(bundle):
    from okf.lookup import load_bundle
    concepts = load_bundle(bundle)
    for c in concepts:
        assert "type" in c
        assert "title" in c
        assert "concept_id" in c
        assert "resource" in c


def test_load_bundle_concept_id_from_path(bundle):
    from okf.lookup import load_bundle
    concepts = load_bundle(bundle)
    for c in concepts:
        # concept_id must be a relative path, no leading slash
        assert not c["concept_id"].startswith("/"), f"Bad concept_id: {c['concept_id']}"
        assert ".md" not in c["concept_id"], f"concept_id should not have .md: {c['concept_id']}"


# ── search ────────────────────────────────────────────────────────────────────

def test_search_exact_name(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["Calculator"])
    assert len(results) > 0
    assert results[0]["title"] == "Calculator"


def test_search_fuzzy_name(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["calc"])
    titles = [r["title"] for r in results]
    assert "Calculator" in titles


def test_search_by_file(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=[], file_filter="connector.py")
    assert len(results) > 0
    for r in results:
        assert "connector" in r["resource"].lower()


def test_search_by_type(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=[], type_filter="Class")
    for r in results:
        assert r["type"] == "Class"


def test_search_by_tag(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=[], tag_filters=["lang:python"])
    assert len(results) > 0
    for r in results:
        assert "lang:python" in r["tags"]


def test_search_empty_query_returns_all(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=[], limit=1000)
    assert len(results) == len(concepts)


def test_search_limit(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=[], limit=2)
    assert len(results) <= 2


def test_search_no_results(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["xyznonexistent123"])
    assert len(results) == 0


def test_search_world_bank_connector(bundle):
    from okf.lookup import load_bundle, search
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["WorldBankConnector"])
    assert len(results) > 0
    assert results[0]["title"] == "WorldBankConnector"


# ── formatters ────────────────────────────────────────────────────────────────

def test_fmt_compact(bundle):
    from okf.lookup import load_bundle, search, fmt_compact
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["Calculator"])
    line = fmt_compact(results[0])
    assert "Calculator" in line
    assert len(line.split("\n")) == 1   # single line


def test_fmt_detail(bundle):
    from okf.lookup import load_bundle, search, fmt_detail
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["Calculator"])
    detail = fmt_detail(results[0])
    assert "Calculator" in detail
    assert "CLASS" in detail or "Class" in detail


def test_fmt_json(bundle):
    import json
    from okf.lookup import load_bundle, search, fmt_json
    concepts = load_bundle(bundle)
    results = search(concepts, tokens=["Calculator"])
    out = fmt_json(results)
    parsed = json.loads(out)
    assert isinstance(parsed, list)
    assert len(parsed) > 0
    assert "title" in parsed[0]
    assert "type" in parsed[0]
    assert "concept_id" in parsed[0]
