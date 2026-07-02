"""Tests for okf/mcp_server.py — MCP protocol."""

import json
from pathlib import Path


SAMPLE = Path(__file__).parent / "fixtures" / "sample_codebase"


def _send(server, msg: dict) -> dict:
    resp = server.handle_request(json.dumps(msg))
    return json.loads(resp) if resp else {}


def test_mcp_initialize(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "initialize"})
    assert resp.get("result", {}).get("protocolVersion") == "2024-11-05"
    assert "resources" in resp["result"]["capabilities"]
    assert "tools" in resp["result"]["capabilities"]


def test_mcp_tools_list(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "tools/list"})
    tools = resp.get("result", [])
    names = {t["name"] for t in tools}
    assert "lookup" in names
    assert "bundle_info" in names
    assert "list_dependencies" in names
    assert "list_by_type" in names


def test_mcp_tool_bundle_info(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "tools/call", "params": {"name": "bundle_info", "arguments": {}}})
    text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    data = json.loads(text)
    assert data["total"] > 0
    assert "python" in data.get("languages", {})
    assert "Function" in data.get("types", {})


def test_mcp_tool_lookup(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "tools/call", "params": {"name": "lookup", "arguments": {"query": "connector"}}})
    text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    results = json.loads(text)
    assert len(results) > 0
    assert any("connector" in r["title"].lower() for r in results)


def test_mcp_tool_list_dependencies(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "tools/call", "params": {"name": "list_dependencies", "arguments": {}}})
    text = resp.get("result", {}).get("content", [{}])[0].get("text", "")
    deps = json.loads(text)
    assert isinstance(deps, list)


def test_mcp_resources_list(tmp_path):
    from okf.generator import scan_codebase, write_bundle
    from okf.mcp_server import BundleMCPServer
    concepts = scan_codebase(SAMPLE)
    write_bundle(concepts, tmp_path, "sample", ["test"])
    s = BundleMCPServer(tmp_path)
    resp = _send(s, {"id": 1, "method": "resources/list"})
    resources = resp.get("result", [])
    assert len(resources) > 0
    assert any(r["uri"].startswith("okf://") for r in resources)
