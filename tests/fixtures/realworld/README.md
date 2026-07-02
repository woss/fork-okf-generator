# OKF Generator — Real-World Fixture Suite

This directory contains 20 real-world code projects (2 per language, 1 easy + 1 complex) designed to exercise the OKF generator's AST scanner across 11 programming languages.

## Structure

```
realworld/
├── python/          # 2 projects (utility library + web service)
├── javascript/      # 2 projects (math utils + API server)
├── typescript/      # 2 projects (type/helpers + user service)
├── go/              # 2 projects (string/math + HTTP server)
├── java/            # 2 projects (string utils + payment service)
├── rust/            # 2 projects (math utils + data service)
├── ruby/            # 2 projects (formatter + report service)
├── c/               # 2 projects (math + linked list)
├── cpp/             # 2 projects (calculator + vector container)
├── csharp/          # 2 projects (utils + order service)
├── sql/             # 2 projects (basic schema + enterprise schema)
├── manifests/       # Cross-project dependency references
└── README.md        # This file
```

## Per-Project Layout

Each project directory contains:
- **Source files** with compilable/syntactically-valid code
- **Manifest file** (package.json, Cargo.toml, pyproject.toml, go.mod, etc.)
- Real logic with meaningful docstrings/comments

## Feature Coverage

| Feature | Languages |
|---------|-----------|
| Functions with type annotations | Python, TypeScript, Go, Rust, C++ |
| Classes with inheritance | Python, TypeScript, Java, Rust, Ruby, C++ |
| Dataclasses/records | Python, Rust, C# |
| Generic types/params | Python, TypeScript, Go, Java, Rust, C++ |
| Decorators/attributes | Python, TypeScript, Java, C# |
| Interfaces/traits | TypeScript, Go, Java, Rust, C# |
| Cross-file imports | All multi-file projects |
| Async/await | Python, JavaScript, TypeScript, C# |
| Error handling | Python, JavaScript, Go, Java, Rust, C#, C |
| Memory management | C (malloc/free), C++ (new/delete) |
| Enums | Python, TypeScript, Java, Rust, SQL |
| Properties/getters-setters | Python, C#, Ruby, Java |
| Docstrings | All languages with language-appropriate format |

## Usage

```bash
# Scan all fixtures with the OKF generator
okf generate ./realworld ./okf_bundle

# Run existing test suite
pytest tests/ -q
```
