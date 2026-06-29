---
name: okf-generator
description: >
  Generate OKF (Open Knowledge Format) v0.1 knowledge bundles from codebases,
  and look up exact concepts for AI agent context injection. Use this skill
  whenever the user wants to: index a codebase, generate OKF bundles, extract
  code knowledge into structured markdown, convert codebases into training data,
  look up functions/classes/modules by name, prime an AI agent with codebase
  context, integrate codebase knowledge with OpenCode or other AI coding agents,
  or run okf_generator.py / okf_lookup.py / okf_to_pairs.py. Also trigger for
  phrases like "index my code", "generate knowledge bundle", "extract codebase
  concepts", "what does X class do", or "look up X in OKF".
---

# OKF Generator & Lookup Skill

Generates structured OKF v0.1 knowledge bundles from codebases (Python, JS/TS,
Go, Java, Rust, Ruby via tree-sitter AST), and provides fast concept lookup for
AI agents like OpenCode.

## Pipeline Overview

```
codebase
   |
   v
okf_generator.py  -->  okf_bundle/          (domain/resource-path layout)
                              |
                       okf_lookup.py         (zero-LLM concept search)
                              |
                       okf_to_pairs.py  -->  okf_pairs.jsonl  (training data)
```

## Scripts

All scripts live in `scripts/`. Read their docstrings for full options.

| Script | Purpose |
|--------|---------|
| `okf_generator.py` | Scan codebase and write OKF bundle |
| `okf_lookup.py` | Search bundle and return exact concept |
| `okf_to_pairs.py` | Convert bundle to JSONL training pairs |

## Dependencies

```bash
pip install pyyaml tree-sitter \
  tree-sitter-python tree-sitter-javascript tree-sitter-typescript \
  tree-sitter-go tree-sitter-java tree-sitter-rust tree-sitter-ruby \
  tqdm openai
```

---

## Task: Generate OKF Bundle

**When**: user says "index my codebase", "generate OKF bundle", "extract knowledge from code"

### Static extraction (no LLM — always run this first)
```bash
python scripts/okf_generator.py <source_dir> <output_dir>
```

### With LLM enrichment (fills missing docstrings and descriptions)
```bash
OKF_ENRICH=1 \
OKF_BASE_URL="http://localhost:8080/v1" \
OKF_API_KEY="llamabarn" \
OKF_MODEL="ggml-org/gemma-3-4b-it-qat-GGUF:Q4_0" \
OKF_MAX_WORKERS=2 \
python scripts/okf_generator.py <source_dir> <output_dir>
```

Enrichment is **resumable** — rerun safely if interrupted. Already-enriched
concepts are skipped automatically (checks disk on every run).

### Key env vars (enrichment only)

| Var | Default | Purpose |
|-----|---------|---------|
| `OKF_ENRICH` | `0` | Set `1` to enable LLM enrichment |
| `OKF_BASE_URL` | `https://api.anthropic.com/v1` | OpenAI-compat endpoint |
| `OKF_API_KEY` | `` | API key |
| `OKF_MODEL` | `claude-sonnet-4-6` | Enrichment model |
| `OKF_MAX_WORKERS` | `2` | Parallel workers (keep low for local LLMs) |

### Output layout (mirrors source tree)
```
okf_bundle/
├── SUMMARY.md              <- bird's-eye view for AI agents
├── index.md                <- root index
├── log.md                  <- generation history
└── <domain>/
    └── <module>/
        ├── index.md        <- lists all concepts in folder
        ├── <module>.md     <- Module concept
        └── <ClassName>.md  <- Class / Function concepts
```

---

## Task: Look Up a Concept

**When**: user asks "what does X do", "find class X", "look up X", or needs to
prime OpenCode with exact concept context before editing code.

```bash
# Full detail — signature, docstring, params, returns, related
python scripts/okf_lookup.py WorldBankConnector

# All concepts from one source file
python scripts/okf_lookup.py --file StockAI/RnD/python/connectors/economic_data.py

# Filter by type
python scripts/okf_lookup.py --type Class connector

# Filter by tag
python scripts/okf_lookup.py --tag lang:python --tag type:Function fetch

# Compact list (many results)
python scripts/okf_lookup.py --compact connector

# JSON output (programmatic / agent use)
python scripts/okf_lookup.py --json WorldBankConnector

# Custom bundle path
python scripts/okf_lookup.py --bundle ./Knowlege/okf_bundle WorldBankConnector
```

Default bundle path: `./okf_bundle`. Also auto-tries `./Knowlege/okf_bundle`
and `./knowledge/okf_bundle`.

---

## Task: Generate Training Pairs

**When**: user wants JSONL training data from the OKF bundle.

```bash
# Static only (instant, no LLM)
SKIP_SYNTH=1 python scripts/okf_to_pairs.py <bundle_dir> output.jsonl

# With LLM (QA, doc, summarize pairs)
SYNTH_BASE_URL="http://localhost:8080/v1" \
SYNTH_API_KEY="llamabarn" \
SYNTH_MODEL="ggml-org/gemma-3-4b-it-qat-GGUF:Q4_0" \
MAX_WORKERS=2 \
QA_PER_CONCEPT=3 \
python scripts/okf_to_pairs.py <bundle_dir> output.jsonl

# Specific pair types only
PAIR_TYPES="codegen,qa" python scripts/okf_to_pairs.py <bundle_dir> output.jsonl
```

### Pair types

| Type | Static | LLM | Covers |
|------|--------|-----|--------|
| `codegen` | yes | yes | Functions, Classes |
| `qa` | no | yes | All (purpose/params/return/edge) |
| `doc` | no | yes | Functions, Classes |
| `summarize` | yes | yes | Modules, Classes |
| `crosslink` | yes | no | All with related concepts |

---

## Task: Regenerate SUMMARY.md Only

```bash
python scripts/okf_generator.py --summarize <bundle_dir>
```

Use after enrichment finishes to refresh the summary without re-scanning.

---

## OpenCode Integration

See `references/opencode-integration.md` for full setup.

Quick setup:
```bash
# 1. Add to AGENTS.md (auto-loaded by OpenCode)
echo "OKF bundle at ./okf_bundle — use: python scripts/okf_lookup.py <Name>" >> AGENTS.md

# 2. Add lookup command
mkdir -p .opencode/commands
echo "RUN python scripts/okf_lookup.py --bundle ./okf_bundle \$NAME" \
  > .opencode/commands/lookup.md
```

---

## Supported Languages

| Language | Parser | Extracts |
|----------|--------|---------|
| Python | stdlib ast | functions, classes, params, return types, docstrings |
| JS / TS | tree-sitter | functions, arrow fns, classes, JSDoc |
| Go | tree-sitter | funcs, methods, structs, interfaces, GoDoc |
| Java | tree-sitter | classes, methods, constructors, Javadoc |
| Rust | tree-sitter | fns, structs, enums, traits, impl blocks, doc comments |
| Ruby | tree-sitter | defs, classes, modules, hash comments |

---

## Troubleshooting

**No concepts found**: Check that source dir is not inside a SKIP_DIRS name
(node_modules, .venv, dist, etc).

**Enrichment slow**: Use `OKF_MAX_WORKERS=1`. Local models process ~1 request
at a time. At 32 tok/sec expect ~3-5s per concept.

**Enrichment interrupted**: Rerun same command. Enriched files are skipped.

**JS/TS concepts missing**: Ensure tree-sitter-typescript is installed.
TypeScript uses a separate grammar from JavaScript.

**Lookup wrong result**: Add --type or --file to narrow the search scope.
