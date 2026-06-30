# Release Process

## Prerequisites

- All unit tests pass: `pytest tests/ -q` (70+ green)
- Full integration spec passes: `TEST.md` (generate, lookup, pairs, summarize, edge cases)
- CHANGELOG.md has an up-to-date `[Unreleased]` section

For a quick confidence check before starting, run `TEST.md` — it exercises every CLI command against AgentBox (TS/JS monorepo) and edge cases.

## Steps

### 1. Bump version

```bash
# Edit both files to match
vim pyproject.toml          # version = "x.y.z"
vim okf/__init__.py         # __version__ = "x.y.z"
```

### 2. Update CHANGELOG

- Promote `[Unreleased]` → `[x.y.z] — YYYY-MM-DD`
- Review for accuracy: every commit should have a line
- Update comparison URL at the bottom:
  ```
  [Unreleased]: https://github.com/UmairBaig8/okf-generator/compare/vx.y.z...HEAD
  [x.y.z]: https://github.com/UmairBaig8/okf-generator/releases/tag/vx.y.z
  ```

### 3. Update README (if new features)

- New CLI flags? Add to CLI Reference section.
- New manifest/language support? Update Supported Languages table + Features list.

### 4. Commit and tag

```bash
git add -A
git commit -m "chore: bump vx.y.z"
git tag vx.y.z
git push && git push --tags
```

### 5. CI handles the rest

The `publish.yml` workflow automatically:

| Step | What it does |
|------|-------------|
| Build | `python -m build` → wheel + sdist |
| Publish to PyPI | `pypa/gh-action-pypi-publish` |
| Smoke test | Installs published wheel in fresh venv, runs `generate` + `lookup` + `pairs` + `summarize` |
| GitHub Release | Creates release from CHANGELOG section |

### 6. Verify

```bash
# Wait for CI, then:
pip install okf-generator==x.y.z
okf --version
```

## Rollback

If a release is broken:
- **PyPI**: `pip install okf-generator==<previous-version>` (no yank unless security)
- **Git tag**: Delete remote tag: `git push --delete origin vx.y.z`
- **GitHub Release**: Delete via `gh release delete vx.y.z`
