# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- C# / Swift / Kotlin parsers
- `okf --version` flag
- GitHub Actions CI/CD with automated PyPI release
- mkdocs documentation site

---

## [0.1.0] — 2026-06-29

### Added
- `okf generate` — scan a codebase and produce an OKF v0.1 bundle
- `okf lookup` — zero-LLM concept search (exact, fuzzy, by file, type, tag)
- `okf pairs` — convert bundle to JSONL training pairs (codegen, qa, doc, summarize, crosslink)
- `okf summarize` — regenerate SUMMARY.md from an existing bundle
- Python parser via stdlib `ast` — functions, classes, params, return types, docstrings
- JS/TypeScript parser via tree-sitter — functions, arrow fns, classes, JSDoc
- Go parser via tree-sitter — funcs, methods, structs, interfaces, GoDoc
- Java parser via tree-sitter — classes, methods, constructors, Javadoc
- Rust parser via tree-sitter — fns, structs, enums, traits, impl blocks, doc comments
- Ruby parser via tree-sitter — defs, classes, modules, hash comments
- Domain/resource-path bundle layout mirroring the source tree
- Resumable LLM enrichment (skips already-enriched concepts on rerun)
- Standardised OKF tags: `lang:`, `type:`, `module:`, `domain:`, `git:branch:`, `git:repo:`
- SUMMARY.md with stats table, domain map, key concepts, OpenCode usage snippet
- `SKILL.md` for use as a Claude skill
- OpenCode integration guide
- 32 passing tests

[Unreleased]: https://github.com/umairbaig/okf-generator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/umairbaig/okf-generator/releases/tag/v0.1.0
