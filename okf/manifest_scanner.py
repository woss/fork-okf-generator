"""
okf/manifest_scanner.py

Extracts dependency/build-manifest concepts (type: Dependency) from
known manifest files. Zero external deps for the first pass (requirements.txt,
pyproject.toml, package.json) — stdlib only.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib  # type: ignore[no-redef]


MANIFEST_HANDLERS: dict[str, str] = {
    "requirements.txt": "parse_requirements_txt",
    "pyproject.toml": "parse_pyproject_toml",
    "package.json": "parse_package_json",
}


def is_manifest_file(path: Path) -> bool:
    return path.name in MANIFEST_HANDLERS


def scan_manifest(path: Path, repo_root: Path) -> list[dict[str, Any]]:
    """Dispatch to the right parser and return Dependency concept dicts.
    Caller converts to Concept objects to avoid circular imports."""
    handler_name = MANIFEST_HANDLERS.get(path.name)
    if handler_name is None:
        return []
    handler = globals()[handler_name]
    raw_deps = handler(path)

    resource = str(path.relative_to(repo_root))
    ts = _ts(path)
    return [_build_concept(dep, resource, ts) for dep in raw_deps]


def _ts(path: Path) -> str:
    """ISO-8601 timestamp from file mtime."""
    import datetime
    mtime = path.stat().st_mtime
    return datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_concept(dep: dict[str, Any], resource: str, ts: str) -> dict[str, Any]:
    name = dep["name"]
    ecosystem = dep["ecosystem"]
    version = dep.get("version", "")
    dev = dep.get("dev", False)

    cid = f"{ecosystem}:{name}"
    description = f"{'Dev dependency' if dev else 'Dependency'} from {resource}"

    return {
        "type": "Dependency",
        "title": name,
        "description": description,
        "resource": resource,
        "tags": [
            f"ecosystem:{ecosystem}",
            "type:Dependency",
            f"manifest:{Path(resource).name}",
            *([f"version:{version}"] if version else []),
        ],
        "timestamp": ts,
        "concept_id": cid,
        "body_extra": {
            "ecosystem": ecosystem,
            "version_constraint": version,
            "dev_dependency": dev,
            "source_manifest": resource,
        },
    }


_REQ_LINE_RE = re.compile(
    r"^\s*([A-Za-z0-9_.\-]+)\s*(?P<spec>[=<>!~]=?[A-Za-z0-9_.\-,*]*)?\s*(?:#.*)?$"
)


def parse_requirements_txt(path: Path) -> list[dict[str, Any]]:
    deps = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue
        m = _REQ_LINE_RE.match(line)
        if not m:
            continue
        name = m.group(1)
        spec = m.group("spec") or ""
        deps.append({"name": name, "ecosystem": "pip", "version": spec, "dev": False})
    return deps


def parse_pyproject_toml(path: Path) -> list[dict[str, Any]]:
    data = tomllib.loads(path.read_text(encoding="utf-8", errors="ignore"))
    deps = []

    project = data.get("project", {})
    for entry in project.get("dependencies", []):
        name, version = _split_pep508(entry)
        deps.append({"name": name, "ecosystem": "pip", "version": version, "dev": False})

    for group, entries in project.get("optional-dependencies", {}).items():
        for entry in entries:
            name, version = _split_pep508(entry)
            deps.append({"name": name, "ecosystem": "pip", "version": version, "dev": True})

    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for name, spec in poetry_deps.items():
        if name.lower() == "python":
            continue
        version = spec if isinstance(spec, str) else spec.get("version", "")
        deps.append({"name": name, "ecosystem": "pip", "version": version, "dev": False})

    return deps


def _split_pep508(entry: str) -> tuple[str, str]:
    m = re.match(r"^([A-Za-z0-9_.\-]+)\s*(.*)$", entry.strip())
    if not m:
        return entry, ""
    return m.group(1), m.group(2)


def parse_package_json(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    deps = []
    for name, version in data.get("dependencies", {}).items():
        deps.append({"name": name, "ecosystem": "npm", "version": version, "dev": False})
    for name, version in data.get("devDependencies", {}).items():
        deps.append({"name": name, "ecosystem": "npm", "version": version, "dev": True})
    return deps
