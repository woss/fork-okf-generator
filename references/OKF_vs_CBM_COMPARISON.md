# OKF Generator vs codebase-memory-mcp — Full Comparison

> Generated: 2026-07-21
> OKF Generator v0.1.51 | codebase-memory-mcp v0.8.1

---

## 1. Overview & Philosophy

| Dimension | OKF Generator | codebase-memory-mcp |
|-----------|--------------|---------------------|
| Version | 0.1.51 | 0.8.1 |
| Language | **Python** (≥3.11) | **C** (static binary) |
| License | MIT | MIT |
| Distribution | `pip install` | npm/PyPI/Homebrew/Scoop/Winget/Chocolatey/AUR/go install |
| Runtime deps | tree-sitter + 15 lang grammars + pyyaml/tqdm/watchdog | **Zero** — everything statically linked |
| Binary size | N/A (Python package) | ~100MB+ (statically linked, 158 TS grammars + SQLite + ONNX + mimalloc + ...) |
| Install size | ~50MB (Python + grammar wheels) | Single binary |
| Target audience | AI coding agents (Claude Code, OpenCode, etc.) | AI coding agents (43 agent surfaces) |
| Tagline | "The knowledge layer for AI coding agents" | "Structural code intelligence for AI coding agents" |
| arXiv paper | None | 2603.27277 |
| Primary output | **Markdown bundle** (flat files) + SQLite on demand | **SQLite graph database** |
| Output schema | OKF v0.2 (YAML frontmatter markdown) | Graph DB: nodes, edges, FTS5, vectors |

**Core philosophical difference:**

- **OKF:** Knowledge is **markdown files** — human-readable, git-friendly, simple. The bundle is a deterministic document. AI agents read individual concept files. Think "wiki for your codebase."
- **codebase-memory-mcp:** Knowledge is a **graph database** — queryable via Cypher, searchable via FTS5 + vectors, traversable for call paths. AI agents query the graph via 15 MCP tools. Think "codebase as a semantic graph."

---

## 2. Implementation & Architecture

### OKF Generator (Python)

```
Source Code
  → walk + gitignore pruning
  → concurrent AST parsing (ProcessPoolExecutor, 17 parsers)
  → manifest scanning (22 formats, same process)
  → cross-reference linker (dep edges + call graph)
  → write OKF markdown files (mirrored source tree)
  → optional: LSP enrichment, LLM enrichment
  → optional: MCP server, SQLite store, dashboard
```

**Key architectural decisions:**
- **File-based knowledge store** — each concept is a .md file; no SQLite needed for basic usage
- **Deterministic by default** — pure AST extraction, no AI in the critical path
- **Bundles are portable** — copy the `okf_bundle/` directory anywhere; it's self-contained markdown
- **Python threading** — ProcessPoolExecutor for CPU-bound parsing, Lock for shared state
- **Plugin system** — entry-point-based parsers + manifest handlers
- **Edge-triggered update** — SHA256 manifest tracks file+edge hashes, re-renders cascading concepts

### codebase-memory-mcp (C)

```
Source Code
  → file discovery (gitignore + cbmignore + 11-layer filter)
  → multi-pass pipeline: definitions → calls → usages → LSP → routes → config → infra → tests → semantic → similarity → cross-repo
  → graph store (SQLite WAL, nodes + edges + FTS5 + vectors)
  → MCP server (15 tools over stdin/stdout JSON-RPC)
  → optional: 3D graph UI, watcher, artifact export
```

**Key architectural decisions:**
- **Graph-based knowledge store** — nodes + labeled edges + properties
- **Multi-pass pipeline** — 19 pass files, each adding a different layer of understanding
- **158 languages via tree-sitter** — all compiled into the single binary
- **Hybrid LSP** — type-aware cross-file resolution in C (9 language families)
- **Embedded semantic search** — nomic-embed-code ONNX model in the binary (no external API)
- **Supervised indexing worker** — child process for crash isolation (prevents memory leak in long-lived server)
- **Thread-safe** — atomic globals, thread-local pipelines, mutex-guarded shared resources

---

## 3. Language Support

| Feature | OKF Generator | codebase-memory-mcp |
|---------|---------------|---------------------|
| **Languages** | 17 | **158** |
| **Parser engine** | tree-sitter (16) + stdlib `ast` (Python) | tree-sitter (158) |
| **Tree-sitter grammars** | 15 Python packages (pip) | 158 vendored C sources |
| **Managed via** | pip install each grammar wheel | Compiled into binary |
| **Parser plugin system** | Yes (entry points) | No (hardcoded) |

Languages in OKF: Python, JS, TS, JSX, TSX, Go, Java, Rust, Ruby, C, C++, C#, Swift, Kotlin, PHP, Dart, Scala, Julia, SQL, YAML

Languages in codebase-memory-mcp: all the above + Ada, Agda, Apex, Assembly, Astro, AWK, Bash, Clojure, CMake, COBOL, Crystal, CSS, CUDA, D, Dockerfile, Elixir, Elm, Erlang, F#, Fortran, GraphQL, Groovy, Haskell, HCL/Terraform, HTML, INI, JSON, Lean, Lua, Makefile, Markdown, MATLAB, Meson, Nix, Objective-C, OCaml, Perl, Protobuf, R, SCSS, SQL, Svelte, Verilog, VHDL, Vue, WGSL, XML, Zig, etc.

**Winner:** codebase-memory-mcp by a **wide margin** (158 vs 17 languages).

---

## 4. Knowledge Representation

### OKF (Markdown Files)
```
okf_bundle/
├── index.md          # bundle root
├── SUMMARY.md        # agent-facing knowledge map
├── .okf-manifest.json
├── _dependencies/pip/requests.md
└── src/connectors/
    ├── index.md
    └── economic_data/
        ├── WorldBankConnector.md    # Class concept
        └── get_indicator.md        # Function concept
```

Each concept is a standalone markdown file with YAML frontmatter (52 fields): type, title, description, signature, params, returns, docstring, methods, inheritance, decorators, relationships, etc.

### codebase-memory-mcp (SQLite Graph)
```
~/.cache/codebase-memory-mcp/<project>.db  (WAL mode)
  Tables: nodes, edges, node_fts5, file_hashes, coverage, adrs, ...
  Node labels: Project, Package, Folder, File, Module, Class, Function, Method, Interface, Route, Resource
  Edge types: CALLS, IMPORTS, DEFINES, INHERITS, TESTS, SIMILAR_TO, SEMANTICALLY_RELATED, CROSS_*, ...
  Query: Cypher (read subset), FTS5, vector cosine similarity, BFS traversal
```

**Key difference:**
- OKF is **document-oriented** — each concept is a human-readable file
- codebase-memory-mcp is **graph-oriented** — nodes + relationships, queryable

**Token efficiency (for AI agents):**
- OKF: reads single concept file (~1.2K tokens per lookup)
- codebase-memory-mcp: TOON format (40-60% of JSON) for structured graph results

Both achieve ~97-99% token reduction vs reading source files, but through different mechanisms.

---

## 5. Manifest/Dependency Scanning

| Feature | OKF Generator | codebase-memory-mcp |
|---------|---------------|---------------------|
| **Manifest formats** | **22 formats** | ~15 (via pass_pkgmap.c) |
| **Supported** | requirements.txt, pyproject.toml, package.json, Cargo.toml, Cargo.lock, yarn.lock, pnpm-lock.yaml, go.mod, go.sum, poetry.lock, composer.json, pom.xml, Gemfile, build.gradle, Package.swift, project.clj, mix.exs, Dockerfile, docker-compose.yml | package.json, go.mod, Cargo.toml, pyproject.toml (and likely more via the pkgmap pass) |
| **Approach** | Pure Python regex + parsers | C regex + tree-sitter |
| **Result** | Creates `Dependency` concepts in bundle | Creates `Package` nodes with `CONTAINS_PACKAGE` edges |
| **Version constraints** | Stored in body_extra | Stored as properties_json on edge |

**Winner:** OKF has more declared formats (22) with richer version constraint extraction.

---

## 6. Incremental/Update Strategy

| Feature | OKF Generator | codebase-memory-mcp |
|---------|---------------|---------------------|
| **Change detection** | SHA256 + mtime | SHA256 + mtime + file size |
| **Tracking file** | `.okf-manifest.json` (project-root) | `file_hashes` table in SQLite |
| **Granularity** | File-level + concept-level + edge-level | File-level |
| **Edge cascade** | **Yes** — edge_hash detects when concept B must be re-rendered because concept A changed | Only re-parses changed files, edges re-resolved |
| **Rename detection** | **Yes** — content-hash index + path similarity | Not explicitly mentioned |
| **Crash safety** | Atomic tmp+rename on manifest write | Supervised worker (child process isolation) |
| **Watch mode** | watchdog.Observer (file system events) | git polling (5-60s adaptive) |
| **Team artifact** | Not yet | `.codebase-memory/graph.db.zst` (zstd-compressed SQLite) |

**Unique features:**
- OKF: edge-triggered cascade re-render, rename detection, atomic manifest commits
- codebase-memory-mcp: supervised child process (100% RSS reclaim on crash), team-shared compressed artifact

---

## 7. MCP Integration

| Dimension | OKF Generator | codebase-memory-mcp |
|-----------|---------------|---------------------|
| **Protocol** | MCP stdio + HTTP/SSE | MCP stdio (JSON-RPC 2.0), supervised worker |
| **Tools** | **11 tools** | **15 tools** |
| **Tool categories** | lookup, get_concept, find_callers, find_callees, list_by_file, list_dependencies, bundle_info, list_by_type, search_by_tag, get_related, get_manifest_source | index_repository, list_projects, delete_project, index_status, search_graph, trace_path, trace_call_path, query_graph, get_graph_schema, get_code_snippet, search_code, get_architecture, detect_changes, manage_adr, ingest_traces, check_index_coverage |
| **Agent install** | `okf install` (OpenCode + Claude Desktop) | Auto-detects **43 agent surfaces**, writes config in their format |
| **Agent profiles** | None | 3 tiers: ALL, ANALYSIS, SCOUT (tool allowlists) |
| **Cancellation** | Basic | Full: `notifications/cancelled` + index supervisor cancellation |
| **Auto-index** | Manual | Auto-index on session start + auto-watch background registration |
| **Console output** | JSON responses | **TOON format** (40-60% token reduction vs JSON) |

**Winner:** codebase-memory-mcp — 15 tools vs 11, 43 agent surfaces vs 2, agent profiles, TOON format, cancellation, auto-index, auto-watch.

OKF's MCP server is functional but much less mature.

---

## 8. Semantic / Enrichment Features

| Feature | OKF Generator | codebase-memory-mcp |
|---------|---------------|---------------------|
| **LSP enrichment** | **Yes** — 4 servers (pyright, gopls, rust-analyzer, typescript-language-server), stdio JSON-RPC client | **Yes** — Hybrid LSP (9 language families, pure C implementation) |
| **LLM enrichment** | **Yes** — 4 modes (base/deep/security/full), 11 providers, multi-provider routing per mode | **No** — all analysis is structural (no LLM calls) |
| **Semantic search** | No (text only) | **Yes** — nomic-embed-code (768d int8) ONNX model compiled in, cosine similarity |
| **Similarity/clone detection** | No | **Yes** — MinHash + LSH → SIMILAR_TO edges (near-clone detection) |
| **Semantic relationships** | LLM-generated (if enabled) | **11 signals**: TF-IDF, RRI, API/Type/Decorator sigs, AST profiles, data flow, Halstead-lite, MinHash, module proximity, graph diffusion |
| **Community detection** | No | **Yes** — Louvain/Leiden algorithms built in |
| **Architecture analysis** | Basic (index.md structure) | **Yes** — languages, packages, entry points, routes, hotspots, cross-pkg boundaries, service links, layers, clusters |
| **ADR management** | No | **Yes** — CRUD for Architecture Decision Records |
| **Trace ingestion** | No | **Yes** — runtime trace → HTTP_CALLS edges |
| **Infrastructure-as-code** | No (YAML parser exists but for resource classification) | **Yes** — Dockerfiles, K8s manifests, Kustomize as first-class graph nodes |

**Winner:** codebase-memory-mcp by a wide margin for analysis depth. OKF has LLM enrichment which codebase-memory-mcp explicitly avoids.

---

## 9. Training Data / Export Features

| Feature | OKF Generator | codebase-memory-mcp |
|---------|---------------|---------------------|
| **Training data generation** | **Yes** — 5 pair types (codegen, qa, doc, summarize, crosslink) → JSONL | No |
| **Diff/Comparison** | **Yes** — content-hash based, per-field diff, impact analysis (3 output modes) | Limited — `detect_changes` tool (git diff → symbol impact) |
| **Visualization** | **Yes** — D3.js/Cytoscape.js force-directed HTML, FastAPI dashboard | **Yes** — 3D graph visualization at localhost:9749 |
| **Bundle portability** | **Excellent** — plain markdown files, copy anywhere | Limited — SQLite file + zstd artifact (needs binary to read) |

**Unique to OKF:** Training data generation (5 pair types) is entirely unique — codebase-memory-mcp has nothing comparable.

---

## 10. Performance & Scale

| Metric | OKF Generator | codebase-memory-mcp |
|--------|---------------|---------------------|
| **Indexing speed** | ~600 files/sec (Python, ProcessPoolExecutor) | Linux kernel (28M LOC, 75K files) in 3 min |
| **Query latency** | ~50ms (file read + frontmatter parse) | **<1ms** (SQLite, Cypher queries) |
| **Max repo size** | ~100K files (practical limit for Python) | Millions of files (28M LOC tested) |
| **Memory usage** | ~200-500MB (Python overhead + tree-sitter) | ~200MB-1GB (C + graph + vectors) |
| **Concurrency** | ProcessPoolExecutor + Lock | Multi-threaded (worker pool, thread-local pipelines) |

**Winner in scale:** codebase-memory-mcp (C is orders of magnitude faster, handles Linux kernel in 3 min)

**Winner in simplicity:** OKF (pip install, human-readable output, no binary)

---

## 11. Unique Features — Not in the Other

### OKF Only
1. **Training data generation** — 5 pair types for fine-tuning coding models
2. **LLM enrichment** — multi-provider, multi-mode (base/deep/security/full)
3. **Plugin system** — extend with pip packages
4. **Domain classification engine** — reclassify YAML resources with rule files
5. **Bundle migration** — formal v0.1 → v0.2 migration script
6. **Interactive REPL** (`okf agent`) — persistent sessions with slash commands
7. **LLM-powered Q&A** (`okf ask`) over the knowledge bundle
8. **Init wizard** (`okf init`) — interactive bundle setup
9. **Serve mode** — local HTTP with git URL support
10. **Deterministic by default** — zero LLM required, same output every run (reproducible)
11. **Edge-triggered cascade updates** — re-render concepts that depend on changed code
12. **Rename detection** — content-hash + path similarity
13. **Markdown-native output** — human readable, diffable, git-friendly

### codebase-memory-mcp Only
1. **158 language grammars** (vs 17) — compiled into single binary
2. **Hybrid LSP type resolution** — semantic, cross-file, no external LSP servers
3. **Embedded ONNX semantic model** — no external API, no Docker, no keys
4. **Cypher query engine** — openCypher read subset parser/planner/executor
5. **Leiden/Louvain community detection** — discover module clusters
6. **Infrastructure-as-code nodes** — Dockerfiles, K8s manifests, Kustomize
7. **Cross-repo intelligence** — CROSS_* edges linking multiple repos
8. **43 agent surfaces** — auto-detection and config for 43+ AI coding agents
9. **Supervised worker isolation** — crash-safe indexing in child process
10. **TOON output format** — proprietary token-optimized notation (40-60% less than JSON)
11. **Single static binary** — zero runtime dependencies, no interpreter required
12. **11-signal semantic scoring** — comprehensive similarity beyond simple embeddings
13. **Architecture Decision Records** — persisted across sessions
14. **Trace ingestion** — validate call edges with runtime traces
15. **3D graph UI** — interactive web visualization at localhost:9749
16. **Dead code detection** — ~150ms for indexed projects
17. **File change impact analysis** — git diff → affected symbols with risk classification

---

## 12. Similarities

Despite the different implementation languages and output formats, both projects share a **common vision** and several design choices:

1. **Same core purpose** — structural code analysis for AI coding agent context injection
2. **Tree-sitter based** — both use tree-sitter for AST parsing (OKF via Python bindings, codebase-memory-mcp via vendored C)
3. **MCP server** — both implement the Model Context Protocol for AI agent integration
4. **Git-aware** — both detect git repo, branch, and origin metadata
5. **Incremental updates** — both track file hashes to avoid full re-scans
6. **Cross-reference resolution** — both resolve call graphs and imports
7. **Manifest scanning** — both parse package manager files alongside source code
8. **Format diversity** — both support multiple languages in a single scan
9. **Deterministic core** — neither requires AI/LLM for the basic indexing pipeline
10. **Open source MIT** — both freely available
11. **CLI-first** — both are primarily command-line tools
12. **AI agent optimization** — both designed to minimize token costs for AI coding agents

---

## 13. Summary Table

| Category | Winner | Why |
|----------|--------|-----|
| **Language coverage** | codebase-memory-mcp | 158 vs 17 languages |
| **Output simplicity** | OKF | Human-readable markdown, git-friendly |
| **Query depth** | codebase-memory-mcp | Cypher, FTS5, vectors, BFS traversal |
| **Install simplicity** | OKF | `pip install` vs binary download |
| **Zero deps** | codebase-memory-mcp | Single static binary, no interpreter |
| **Scale** | codebase-memory-mcp | Handles 28M LOC, sub-ms queries |
| **MCP maturity** | codebase-memory-mcp | 15 tools, 43 agents, profiles, TOON format |
| **Training data** | OKF | 5 pair types, JSONL export (unique feature) |
| **LLM enrichment** | OKF | Multi-provider, multi-mode (unique feature) |
| **Semantic search** | codebase-memory-mcp | Embedded ONNX, no external API |
| **Structural analysis** | codebase-memory-mcp | 11-signal semantic scoring, community detection, architecture analysis |
| **Portability** | OKF | Plain markdown, copy anywhere without tools |
| **Plugin system** | OKF | Entry-point-based extensibility |
| **Agent integration** | codebase-memory-mcp | 43 surfaces vs 2, auto-detection |
| **Code quality** | codebase-memory-mcp | More rigorous C (defensive, thread-safe, memory-safe) |
| **Development speed** | OKF | Python = faster iteration and feature development |

---

## 14. The Bottom Line

These projects are **complementary approaches to the same problem**:

- **OKF Generator** is built for **simplicity, portability, and human readability**. Its output is markdown files that any AI agent or human can read directly. It excels at training data generation, LLM enrichment, and plugin extensibility. It's easier to install, hack on, and integrate.

- **codebase-memory-mcp** is built for **performance, depth, and scale**. Its output is a queryable graph database with semantic understanding. It excels at structural analysis (158 languages, Cypher queries, semantic search, community detection) and has far more mature MCP tooling with broad agent surface support.

**If you want to:** Index your codebase once and have AI agents query it via MCP tools with sub-millisecond response, codebase-memory-mcp is more mature.  
**If you want to:** Have human-readable knowledge bundles you can browse, diff, version-control, and use for training data, OKF is the right tool.  
**If you want both:** OKF's MCP server and SQLite store give you some graph capability, and codebase-memory-mcp can eventually be paired with LLM enrichment from OKF-style bundles.
