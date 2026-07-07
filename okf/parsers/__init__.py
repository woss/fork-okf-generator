"""Parser registry — delegates to plugin system.

For backward compatibility, retains imports and a ``get_parser()`` that
forwards to :mod:`okf.plugin`.
"""

# Retained for backward compat — external code may import these directly.
from okf.parsers.python import PythonParser
from okf.parsers.javascript import JSTSParser
from okf.parsers.go import GoParser
from okf.parsers.java import JavaParser
from okf.parsers.rust import RustParser
from okf.parsers.ruby import RubyParser
from okf.parsers.c import CParser
from okf.parsers.cpp import CppParser
from okf.parsers.csharp import CSharpParser
from okf.parsers.sql import SQLParser
from okf.parsers.swift import SwiftParser
from okf.parsers.kotlin import KotlinParser
from okf.parsers.php import PHPParser
from okf.parsers.dart import DartParser
from okf.parsers.scala import ScalaParser
from okf.parsers.julia import JuliaParser

# Deprecated — kept for third-party code that imports EXTENSION_MAP.
# The plugin registry (okf.plugin.discover_parsers) is the canonical source.
EXTENSION_MAP: dict[str, type] = {}


def get_parser(ext: str):
    """Return a parser instance for *ext* via the plugin registry."""
    from okf.plugin import get_parser as _plugin_get
    return _plugin_get(ext)
