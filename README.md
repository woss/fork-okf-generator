<div align="center">

<img src="https://raw.githubusercontent.com/UmairBaig8/okf-generator/main/docs/banner.svg" alt="okf-generator banner" width="100%"/>

<br/>

[![PyPI version](https://img.shields.io/pypi/v/okf-generator?style=flat-square&label=PyPI)](https://pypi.org/project/okf-generator/)
[![Python](https://img.shields.io/pypi/pyversions/okf-generator?style=flat-square)](https://pypi.org/project/okf-generator/)
[![Tests](https://img.shields.io/github/actions/workflow/status/UmairBaig8/okf-generator/ci.yml?style=flat-square&label=tests)](https://github.com/UmairBaig8/okf-generator/actions)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![OKF v0.1](https://img.shields.io/badge/OKF-v0.1-7c3aed?style=flat-square)](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-orange?style=flat-square&logo=anthropic)](SKILL.md)
[![OpenCode](https://img.shields.io/badge/OpenCode-ready-7c3aed?style=flat-square)](https://github.com/anthropics/opencode)
[![Cursor](https://img.shields.io/badge/Cursor-ready-6c47ff?style=flat-square)](https://cursor.sh)
[![Windsurf](https://img.shields.io/badge/Windsurf-ready-2563eb?style=flat-square)](https://codeium.com/windsurf)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](CONTRIBUTING.md)

**Index any codebase into a structured OKF v0.1 knowledge bundle — then look up exact concepts for any AI coding agent.**

[Installation](#installation) · [Quick Start](#quick-start) · [CLI Reference](#cli-reference) · [AI Agent Integration](#ai-agent-integration) · [Contributing](#contributing)

</div>

---

## What is this?

`okf-generator` converts your source code into an [Open Knowledge Format](https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing) (OKF) v0.1 knowledge bundle — structured markdown files that AI agents can read, search, and reason over.

Instead of giving an AI your entire codebase, you give it exactly the concept it needs:

```bash
# Before touching WorldBankConnector, look it up
okf lookup WorldBankConnector

# CLASS: WorldBankConnector
# Source      : StockAI/RnD/python/connectors/economic_data.py  line 51
# Description : Fetches World Bank development indicators via wbdata API.
# Methods     : get_indicator, search
# Signature   : class WorldBankConnector
```

## Features

- **7 languages** — Python (stdlib AST), JS/TS/Go/Java/Rust/Ruby (tree-sitter), SQL (dialect-tolerant regex)
- **12 manifest formats** — `requirements.txt`, `pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`, `composer.json`, `pom.xml`, `Gemfile`, `build.gradle`, `Package.swift`, `project.clj`, `mix.exs` — each dependency becomes a `Dependency` concept with ecosystem, version, and dev-flag metadata
- **Zero LLM required** for extraction — deterministic, fast, offline-capable
- **OKF v0.1 conformant** — type, description, resource, tags, timestamp
- **Domain/resource-path layout** — bundle mirrors your source tree exactly; dependencies organized in `_dependencies/{ecosystem}/` folders
- **Resumable LLM enrichment** — enrich descriptions with any OpenAI-compat endpoint; safe to interrupt and rerun
- **Lookup cache** — auto-caches parsed concepts; subsequent lookups skip re-parsing (~2x faster)
- **Any AI agent** — OpenCode, Claude Code, Cursor, Windsurf, Cline, GitHub Copilot, and more
- **Training data pipeline** — convert bundle to JSONL pairs (codegen, QA, doc, summarize, crosslink)
- **Claude Skill included** — install `SKILL.md` to trigger the full pipeline from natural language

## Installation

**One-liner — paste into any terminal:**

```bash
curl -fsSL https://raw.githubusercontent.com/UmairBaig8/okf-generator/main/scripts/install.sh | bash
```

This installs `okf-generator[llm]` + the Claude Code skill in one shot.  
*Requirements: Python 3.11+ with pip.*

Or manually:

```bash
# Core (extraction only — no LLM required)
pip install okf-generator

# With LLM enrichment + training pair generation
pip install "okf-generator[llm]"
```

## Quick Start

```bash
# 1. Generate a knowledge bundle from your codebase
okf generate ./my_project ./okf_bundle

# 2. Look up a concept (works instantly, zero LLM)
okf lookup WorldBankConnector

# 3. Find all concepts from one file
okf lookup --file src/connectors/economic_data.py

# 4. Generate training pairs from the bundle
okf pairs ./okf_bundle ./train.jsonl

# 5. Regenerate SUMMARY.md after enrichment
okf summarize ./okf_bundle
```

## Bundle Layout

The output mirrors your source tree — dependencies get their own organized namespace:

```
okf_bundle/
├── SUMMARY.md                        ← bird's-eye view for AI agents
├── index.md                          ← root navigation
├── log.md                            ← generation history
├── _dependencies/                    ← all dependency concepts
│   ├── index.md                      ← lists ecosystems: pip, npm, cargo, ...
│   ├── pip/
│   │   ├── index.md
│   │   ├── requests.md               ← Dependency concept
│   │   └── flask.md
│   └── npm/
│       ├── index.md
│       ├── express.md
│       └── react.md
└── StockAI/
    └── RnD/
        └── python/
            └── connectors/
                ├── index.md          ← lists all concepts in this folder
                ├── economic_data.md  ← Module concept
                └── economic_data/
                    ├── WorldBankConnector.md   ← Class
                    ├── get_indicator.md        ← Function
                    └── search.md               ← Function
```

Each file is OKF v0.1 conformant:

```yaml
---
type: Class
title: WorldBankConnector
description: Fetches World Bank development indicators via wbdata API.
resource: StockAI/RnD/python/connectors/economic_data.py
tags:
  - lang:python
  - type:Class
  - module:StockAI
  - domain:RnD
  - git:branch:main
  - git:repo:TrainLLMs
timestamp: '2026-05-23T09:01:21Z'
---

# WorldBankConnector

...signature, docstring, params, returns, methods, related concepts...
```

## CLI Reference

### `okf generate`

```
okf generate <source_dir> [output_dir]

Options:
  --summarize <bundle_dir>   Regenerate SUMMARY.md only (no re-scan)

Environment variables (LLM enrichment):
  OKF_ENRICH=1               Enable LLM enrichment
  OKF_BASE_URL               OpenAI-compat base URL (default: https://api.anthropic.com/v1)
  OKF_API_KEY                API key
  OKF_MODEL                  Model name (default: claude-sonnet-4-6)
  OKF_MAX_WORKERS            Parallel workers (default: 2)
```

### `okf lookup`

```
okf lookup [query] [options]

Options:
  --bundle PATH     Bundle directory (default: ./okf_bundle)
  --file PATH       Filter by source file
  --type TYPE       Filter by concept type: Function | Class | Module | Dependency
  --tag TAG         Filter by tag, repeatable: --tag lang:python or --tag ecosystem:npm
  --limit N         Max results (default: 10)
  --compact         One-line output per result
  --json            JSON output for programmatic use
  --full            Raw .md file content
  --min-score N     Minimum relevance score 0-1 (default: 0.1)
  --no-cache        Bypass and skip writing the lookup cache
```

### `okf pairs`

```
okf pairs <bundle_dir> [output_file]

Environment variables:
  SKIP_SYNTH=1          Static pairs only (no LLM)
  SYNTH_BASE_URL        API endpoint
  SYNTH_API_KEY         API key
  SYNTH_MODEL           Model name
  MAX_WORKERS           Parallel workers (default: 3)
  QA_PER_CONCEPT        Q&A pairs per concept (default: 3)
  PAIR_TYPES            Comma-separated: codegen,qa,doc,summarize,crosslink
```

## Supported Languages & Manifests

### Code Languages

| Language | Parser | Extracts |
|----------|--------|---------|
| Python | stdlib `ast` | Functions, classes, params, return types, docstrings |
| JavaScript / TypeScript | tree-sitter | Functions, arrow fns, classes, JSDoc |
| Go | tree-sitter | Funcs, methods, structs, interfaces, GoDoc |
| Java | tree-sitter | Classes, methods, constructors, Javadoc |
| Rust | tree-sitter | Fns, structs, enums, traits, impl blocks, `///` |
| Ruby | tree-sitter | Defs, classes, modules, `#` comments |
| SQL | regex (dialect-tolerant) | `CREATE TABLE`/`VIEW`/`FUNCTION`/`PROCEDURE`/`INDEX`, preceding `--`/`/* */` comments |

### Manifest / Build Files

| Format | Parser | Extracts |
|--------|--------|---------|
| `requirements.txt` | regex | pip package names + version constraints |
| `pyproject.toml` | `tomllib` | PEP 621 deps + optional-dependencies + Poetry legacy |
| `package.json` | `json` | npm/Node dependencies + devDependencies |
| `Cargo.toml` | `tomllib` | Rust crate deps + dev/build-dependencies |
| `go.mod` | regex | Go module deps + `// indirect` flag |
| `composer.json` | `json` | PHP packages (skips `php`/`ext-*` platform entries) |
| `pom.xml` | `xml.etree.ElementTree` | Maven dependencies + `test`/`provided` scope → dev |
| `Gemfile` | regex | Ruby gems + `group :test/:development` → dev |
| `build.gradle` / `.kts` | regex | Gradle deps (Groovy + Kotlin DSL) + `testImplementation` → dev |
| `Package.swift` | regex | SwiftPM packages from `.package(url:from:)` |
| `project.clj` | regex | Clojars deps + `:dev` profile |
| `mix.exs` | regex | Hex packages + `only: :dev/:test` → dev |

## LLM Enrichment

Works with any OpenAI-compatible endpoint — Claude, Ollama, llama.cpp, etc:

```bash
# Using a local llama.cpp server
OKF_ENRICH=1 \
OKF_BASE_URL="http://localhost:8080/v1" \
OKF_API_KEY="llamabarn" \
OKF_MODEL="ggml-org/gemma-3-4b-it-qat-GGUF:Q4_0" \
OKF_MAX_WORKERS=2 \
okf generate ./my_project ./okf_bundle
```

Enrichment is **resumable** — interrupt and rerun freely. Already-enriched concepts are skipped.

## AI Agent Integration

okf-generator works with **any AI coding agent** — the output is plain markdown files that every agent can read.

### OpenCode / Claude Code

```bash
# Tell your agent about the bundle
cat >> AGENTS.md << 'EOF'
## OKF Knowledge Bundle
Before working on any class or function, look it up:
  okf lookup --bundle ./okf_bundle <ConceptName>
EOF

# Add a custom command (OpenCode)
mkdir -p .opencode/commands
echo "RUN okf lookup --bundle ./okf_bundle \$NAME" > .opencode/commands/lookup.md
```

Then: `/lookup NAME=WorldBankConnector`

### Cursor / Windsurf / Cline

Add to `.cursorrules` or agent instructions:

```
Before editing a function or class, run:
  okf lookup --bundle ./okf_bundle <Name>
To see dependencies:
  okf lookup --bundle ./okf_bundle --type Dependency
```

### GitHub Copilot

Reference OKF bundle files in your `/.github/copilot-instructions.md`:

```markdown
Project knowledge is indexed in ./okf_bundle/
  - okf lookup <Name> returns full concept context
  - okf lookup --type Dependency returns dependency info
```

### Any agent with RUN capability

```bash
# Prime full context
cat ./okf_bundle/SUMMARY.md

# Look up a specific concept
okf lookup --bundle ./okf_bundle WorldBankConnector

# List dependencies
okf lookup --bundle ./okf_bundle --type Dependency

# JSON for programmatic agent use
okf lookup --bundle ./okf_bundle --json WorldBankConnector
```

See [docs/opencode-integration.md](references/opencode-integration.md) for full OpenCode setup.

## Python API

```python
from okf.generator import scan_codebase, write_bundle, write_summary
from okf.lookup import load_bundle, search

# Generate bundle
concepts = scan_codebase("./my_project")
write_bundle(concepts, "./okf_bundle", "my_project", ["initial generation"])
write_summary("my_project", concepts, "./okf_bundle", {})

# Search concepts
bundle = load_bundle("./okf_bundle")
results = search(bundle, tokens=["WorldBankConnector"])
print(results[0]["description"])
```

## Training Data

Convert your OKF bundle into JSONL training pairs for fine-tuning:

```bash
# 5 pair types: codegen, qa, doc, summarize, crosslink
okf pairs ./okf_bundle ./train.jsonl
```

Each pair is in chat format compatible with most fine-tuning pipelines.

## Claude Skill

Install the skill in one step:

```bash
curl -fsSL https://raw.githubusercontent.com/UmairBaig8/okf-generator/main/scripts/install.sh | bash
```

Or via pip:

```bash
pip install okf-generator && okf install-skill
```

Once installed, Claude Code automatically triggers the skill on phrases like:
> *"Index my codebase"* → generates OKF bundle  
> *"Look up WorldBankConnector"* → returns exact concept  
> *"Generate training pairs from my bundle"* → outputs JSONL

The same `.md` output works with **any** agent — no vendor lock-in. Point Cursor, Windsurf, Cline, or Copilot at your bundle and they get the same structured knowledge.  

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
git clone https://github.com/UmairBaig8/okf-generator
cd okf-generator
pip install -e ".[dev]"
pytest tests/
```

**Good first issues:** adding a new language parser, improving fuzzy search scoring, adding a CHANGELOG.

## License

[MIT](LICENSE) — Copyright © 2026 Umair Baig
