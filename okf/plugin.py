"""Plugin system — discovers parser plugins via Python entry points.

A plugin is any package that registers an entry point in the ``okf.parsers``
group and exports a class matching ParserPlugin.

Example plugin ``pyproject.toml``::

    [project.entry-points."okf.parsers"]
    cobol = "okf_parser_cobol:Parser"

The plugin class must implement:

.. code-block:: python

    class Parser:
        LANGUAGE: str           # "cobol"
        EXTENSIONS: set[str]    # {".cbl", ".cob"}

        def parse_file(self, path: Path, repo_root: Path) -> list[Concept]: ...
"""

import logging
from pathlib import Path
from typing import Any

from okf.parsers.base import Concept

log = logging.getLogger("okf_gen")

# ---------------------------------------------------------------------------
# ParserPlugin interface (documented — structural subtyping, no ABC)
# ---------------------------------------------------------------------------

class ParserPlugin:
    """Minimal interface a parser plugin must satisfy.

    Subclass and override ``parse_file``. Set ``LANGUAGE`` and ``EXTENSIONS``
    as class attributes.
    """
    LANGUAGE: str = "unknown"
    EXTENSIONS: set[str] = set()

    def parse_file(self, path: Path, repo_root: Path) -> list[Concept]:
        raise NotImplementedError

    def collect_imports(self, root_node: Any, source_bytes: bytes) -> list[str]:
        return []

    def collect_calls(self, root_node: Any, source_bytes: bytes) -> list[str]:
        return []


# ---------------------------------------------------------------------------
# Built-in parser entry points (same format as external plugins)
# ---------------------------------------------------------------------------

_BUILTIN_PARSERS: dict[str, str] = {
    "python":     "okf.parsers.python:PythonParser",
    "javascript": "okf.parsers.javascript:JSTSParser",
    "go":         "okf.parsers.go:GoParser",
    "java":       "okf.parsers.java:JavaParser",
    "rust":       "okf.parsers.rust:RustParser",
    "ruby":       "okf.parsers.ruby:RubyParser",
    "c":          "okf.parsers.c:CParser",
    "cpp":        "okf.parsers.cpp:CppParser",
    "csharp":     "okf.parsers.csharp:CSharpParser",
    "sql":        "okf.parsers.sql:SQLParser",
    "swift":      "okf.parsers.swift:SwiftParser",
    "kotlin":     "okf.parsers.kotlin:KotlinParser",
    "php":        "okf.parsers.php:PHPParser",
    "dart":       "okf.parsers.dart:DartParser",
    "scala":      "okf.parsers.scala:ScalaParser",
    "julia":      "okf.parsers.julia:JuliaParser",
}

# JS/TS needs special runtime config (_path_ext for grammar selection).
# Mark it so get_parser can special-case instantiation.
_JS_TS_KEY = "javascript"


# ---------------------------------------------------------------------------
# Registry (cached singleton)
# ---------------------------------------------------------------------------

_registry: dict[str, type[ParserPlugin]] | None = None
_errors: list[str] = []


def discover_parsers() -> dict[str, type[ParserPlugin]]:
    """Discover all parsers (built-in + external plugins) and return
    ``{extension: parser_class}`` mapping.

    External plugins are discovered via ``importlib.metadata.entry_points``
    (group ``okf.parsers``).  Built-in parsers are registered internally.

    The result is cached after first call.
    """
    global _registry, _errors
    if _registry is not None:
        return _registry

    _errors = []
    ext_map: dict[str, type[ParserPlugin]] = {}

    def _load_all(namespace: str, source: str):
        for name, dotted_path in source.items():
            try:
                mod_path, cls_name = dotted_path.rsplit(":", 1)
                import importlib
                mod = importlib.import_module(mod_path)
                cls: type[ParserPlugin] = getattr(mod, cls_name)
                for ext in cls.EXTENSIONS:
                    ext_map[ext] = cls
            except Exception as e:
                _errors.append(f"{namespace}/{name}: {e}")
                log.debug(f"Failed to load parser {namespace}/{name}: {e}")

    # 1. Load built-in parsers
    _load_all("builtin", _BUILTIN_PARSERS)

    # 2. Load external plugins via entry points
    try:
        from importlib.metadata import entry_points
        for ep in entry_points(group="okf.parsers"):
            try:
                cls = ep.load()
                for ext in cls.EXTENSIONS:
                    ext_map[ext] = cls
            except Exception as e:
                _errors.append(f"plugin/{ep.name}: {e}")
                log.warning(f"Failed to load plugin {ep.name}: {e}")
    except Exception as e:
        log.debug(f"Entry point discovery failed: {e}")

    _registry = ext_map
    return _registry


def get_parser(ext: str) -> ParserPlugin | None:
    """Return a parser instance for *ext* (e.g. ``.py``), or ``None``."""
    import okf.parsers.javascript as jsts
    registry = discover_parsers()
    cls = registry.get(ext)
    if cls is None:
        return None
    from okf.parsers.javascript import JSTSParser
    if cls is JSTSParser and ext in {".ts", ".tsx"}:
        p = cls()
        p._path_ext = ext
        return p
    return cls()


def plugin_errors() -> list[str]:
    """Return list of load errors from last discovery."""
    return list(_errors)


def list_plugins() -> list[dict]:
    """Return a human-readable list of discovered plugins."""
    registry = discover_parsers()
    seen: dict[str, dict] = {}
    for ext, cls in registry.items():
        lang = getattr(cls, "LANGUAGE", "unknown")
        if lang not in seen:
            seen[lang] = {
                "language": lang,
                "extensions": set(),
                "class": f"{cls.__module__}.{cls.__qualname__}",
            }
        seen[lang]["extensions"].add(ext)
    result = sorted(seen.values(), key=lambda x: x["language"])
    for r in result:
        r["extensions"] = sorted(r["extensions"])
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cli():
    """``okf plugin`` subcommand entry point."""
    import sys
    args = sys.argv[1:]  # ["okf plugin", "list", ...] → take from index 1

    if not args or args[0] in {"-h", "--help"}:
        print(__doc__)
        return

    cmd = args[0]

    if cmd == "list":
        plugins = list_plugins()
        errors = plugin_errors()
        print(f"\n  Discovered parsers ({len(plugins)} languages, {len(discover_parsers())} extensions):\n")
        for p in plugins:
            exts = ", ".join(p["extensions"])
            print(f"    {p['language']:15s} [{exts}]")
        if errors:
            print(f"\n  Errors ({len(errors)}):")
            for e in errors:
                print(f"    ! {e}")
        print()

    elif cmd == "install":
        if len(args) < 2:
            print("Usage: okf plugin install <package_name>")
            return
        pkg = args[1]
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "install", pkg],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Install failed:\n{result.stderr}")
            return
        print(f"Installed {pkg}")
        # Verify the plugin loads
        _reset_registry()
        try:
            discover_parsers()
            errors = plugin_errors()
            if errors:
                print(f"Plugin loaded with {len(errors)} error(s):")
                for e in errors:
                    print(f"  ! {e}")
            else:
                print("Plugin registered successfully.")
        except Exception as e:
            print(f"Plugin load failed: {e}")

    elif cmd == "uninstall":
        if len(args) < 2:
            print("Usage: okf plugin uninstall <package_name>")
            return
        pkg = args[1]
        import subprocess
        result = subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", pkg],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Uninstall failed:\n{result.stderr}")
            return
        print(f"Uninstalled {pkg}")
        _reset_registry()

    else:
        print(f"Unknown plugin command: {cmd!r}")
        print("Available: list, install, uninstall")


def _reset_registry():
    """Force re-discovery on next call (used after install/uninstall)."""
    global _registry, _errors
    _registry = None
    _errors = []
