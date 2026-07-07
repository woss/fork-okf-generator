# okf-dotenv-plugin

Sample OKF manifest plugin — parses `.env` files into Dependency concepts.

## Quick start

```bash
pip install .
okf plugin list
# → dotenv  [.env, .env.example, .env.local, ...]
```

## Test it

```bash
echo 'DB_URL=postgres://localhost:5432/mydb
API_KEY=sk-abc123' > /tmp/test_env/.env
echo 'x = 1' > /tmp/test_env/main.py
okf generate /tmp/test_env /tmp/test_bundle
okf lookup --bundle /tmp/test_bundle --type Dependency
# → DB_URL, API_KEY
```

## How it works

The entry point in `pyproject.toml` registers ``ManifestHandler`` under the
``okf.manifests`` group. OKF discovers it at startup via
``importlib.metadata.entry_points()`` — no manual registration needed.

See [Plugin Development Guide](https://umairbaig8.github.io/okf-generator/docs-site/user-guide/plugins/) for full docs.
