"""okf diff — compare two OKF bundles.

Usage:
  okf diff <old_bundle> <new_bundle>
  okf diff <old_bundle> <new_bundle> --compact
  okf diff <old_bundle> <new_bundle> --json

Outputs added, removed, and changed concepts between bundle versions.
Changes are detected via content hash (description + signature + tags + body_extra)
so the same concept_id with different content shows as changed.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path


def _concept_hash(c: dict) -> str:
    """Stable hash of content fields — not concept_id or timestamps."""
    raw = json.dumps(
        {
            "description": c.get("description", ""),
            "signature": c.get("sections", {}).get("signature", ""),
            "tags": sorted(c.get("tags", [])),
            "body_extra": c.get("body_extra", {}),
        },
        sort_keys=True,
        ensure_ascii=False,
    )
    return hashlib.md5(raw.encode()).hexdigest()


def diff_bundles(old_dir: Path, new_dir: Path) -> dict:
    """Compare two bundles and return added/removed/changed concepts."""
    from okf.lookup import load_bundle as _load

    old_list = _load(old_dir)
    new_list = _load(new_dir)

    old_by_id: dict[str, dict] = {c["concept_id"]: c for c in old_list}
    new_by_id: dict[str, dict] = {c["concept_id"]: c for c in new_list}

    old_ids = set(old_by_id.keys())
    new_ids = set(new_by_id.keys())

    old_hashes = {cid: _concept_hash(c) for cid, c in old_by_id.items()}
    new_hashes = {cid: _concept_hash(c) for cid, c in new_by_id.items()}

    added_ids = new_ids - old_ids
    removed_ids = old_ids - new_ids
    common_ids = new_ids & old_ids
    changed_ids = {cid for cid in common_ids if old_hashes[cid] != new_hashes[cid]}

    def _brief(c: dict) -> dict:
        return {
            "concept_id": c["concept_id"],
            "type": c["type"],
            "title": c["title"],
            "resource": c.get("resource", ""),
            "description": c.get("description", ""),
        }

    added = [_brief(new_by_id[cid]) for cid in sorted(added_ids)]
    removed = [_brief(old_by_id[cid]) for cid in sorted(removed_ids)]

    changed = []
    for cid in sorted(changed_ids):
        old_c = old_by_id[cid]
        new_c = new_by_id[cid]
        entry = _brief(new_c)
        entry["changes"] = {}
        if old_c.get("description") != new_c.get("description"):
            entry["changes"]["description"] = (old_c.get("description", ""), new_c.get("description", ""))
        old_sig = old_c.get("sections", {}).get("signature", "")
        new_sig = new_c.get("sections", {}).get("signature", "")
        if old_sig != new_sig:
            entry["changes"]["signature"] = (old_sig, new_sig)
        if old_c.get("tags") != new_c.get("tags"):
            entry["changes"]["tags"] = (old_c.get("tags", []), new_c.get("tags", []))
        changed.append(entry)

    return {
        "old_path": str(old_dir),
        "new_path": str(new_dir),
        "old_count": len(old_list),
        "new_count": len(new_list),
        "added": added,
        "removed": removed,
        "changed": changed,
    }


# ---------------------------------------------------------------------------
# Formatters
# ---------------------------------------------------------------------------

DIVIDER = "─" * 60


def fmt_compact(result: dict) -> str:
    lines = [
        DIVIDER,
        "  okf diff",
        DIVIDER,
        f"  Old: {result['old_path']} ({result['old_count']} concepts)",
        f"  New: {result['new_path']} ({result['new_count']} concepts)",
        DIVIDER,
    ]
    if result["added"]:
        lines.append(f"\n  Added ({len(result['added'])}):")
        for c in result["added"][:10]:
            lines.append(f"    [+] {c['type']}: {c['title']} — {c['resource']}")
        if len(result["added"]) > 10:
            lines.append(f"    ... and {len(result['added']) - 10} more")
    if result["removed"]:
        lines.append(f"\n  Removed ({len(result['removed'])}):")
        for c in result["removed"][:10]:
            lines.append(f"    [-] {c['type']}: {c['title']} — {c['resource']}")
        if len(result["removed"]) > 10:
            lines.append(f"    ... and {len(result['removed']) - 10} more")
    if result["changed"]:
        lines.append(f"\n  Changed ({len(result['changed'])}):")
        for c in result["changed"][:10]:
            lines.append(f"    [~] {c['type']}: {c['title']} — {c['resource']}")
        if len(result["changed"]) > 10:
            lines.append(f"    ... and {len(result['changed']) - 10} more")
    lines.append(DIVIDER)
    return "\n".join(lines)


def fmt_detail(result: dict) -> str:
    lines = [
        DIVIDER,
        "  okf diff",
        DIVIDER,
        f"  Old: {result['old_path']} ({result['old_count']} concepts)",
        f"  New: {result['new_path']} ({result['new_count']} concepts)",
        DIVIDER,
    ]
    if result["added"]:
        lines.append(f"\n  Added ({len(result['added'])}):\n")
        for c in result["added"]:
            lines.append(f"    [+] {c['type']}: {c['title']}")
            lines.append(f"        resource: {c['resource']}")
            if c.get("description"):
                lines.append(f"        description: {c['description'][:80]}")
            lines.append("")
    if result["removed"]:
        lines.append(f"  Removed ({len(result['removed'])}):\n")
        for c in result["removed"]:
            lines.append(f"    [-] {c['type']}: {c['title']}")
            lines.append(f"        resource: {c['resource']}")
            lines.append("")
    if result["changed"]:
        lines.append(f"  Changed ({len(result['changed'])}):\n")
        for c in result["changed"]:
            lines.append(f"    [~] {c['type']}: {c['title']}")
            lines.append(f"        resource: {c['resource']}")
            for field, (old_val, new_val) in c.get("changes", {}).items():
                old_short = str(old_val)[:60]
                new_short = str(new_val)[:60]
                lines.append(f"        {field}:")
                lines.append(f"          - {old_short}")
                lines.append(f"          + {new_short}")
            lines.append("")
    lines.append(DIVIDER)
    return "\n".join(lines)


def fmt_json(result: dict) -> str:
    return json.dumps(result, indent=2, ensure_ascii=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Diff two OKF bundles — see added, removed, and changed concepts.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("old_bundle", help="Path to the older OKF bundle")
    p.add_argument("new_bundle", help="Path to the newer OKF bundle")
    p.add_argument("--compact", action="store_true", help="Compact one-line output per concept")
    p.add_argument("--json", action="store_true", help="JSON output for programmatic use")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    old_dir = Path(args.old_bundle).resolve()
    new_dir = Path(args.new_bundle).resolve()

    if not old_dir.exists():
        print(f"ERROR: Old bundle not found: {old_dir}", file=sys.stderr)
        sys.exit(1)
    if not new_dir.exists():
        print(f"ERROR: New bundle not found: {new_dir}", file=sys.stderr)
        sys.exit(1)

    result = diff_bundles(old_dir, new_dir)

    if args.json:
        print(fmt_json(result))
    elif args.compact:
        print(fmt_compact(result))
    else:
        print(fmt_detail(result))

    total_changes = len(result["added"]) + len(result["removed"]) + len(result["changed"])
    if total_changes == 0:
        print("  No differences — bundles are identical.")
    sys.exit(0 if total_changes == 0 else 0)  # diff exits 0 even with changes


if __name__ == "__main__":
    main()
