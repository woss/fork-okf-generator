"""OKF manifest plugin — parses .env files as dependency concepts.

Install:
    pip install .

Then run ``okf plugin list`` — you should see ``dotenv [.env, .env.example, .env.local]``
under the Manifests section.

Any ``okf generate`` scan that encounters a ``.env`` file will call this plugin's
``parse()`` method and emit one Dependency concept per environment variable.
"""

from pathlib import Path


__all__ = ["ManifestHandler"]


class ManifestHandler:
    """OKF manifest handler for ``.env`` files.

    Required attributes:
        MANIFEST_FILES (list[str]): Filenames this handler recognises.
            OKF's scanner checks these names during ``okf generate``.

    Required method:
        parse(path, repo_root) -> list[dict]:
            Return a list of raw dependency dicts. Each dict must have:
                name (str):       Dependency name (e.g. ``"DB_URL"``)
                ecosystem (str):  Ecosystem label (e.g. ``"dotenv"``)
                version (str):    Version string (e.g. ``"=postgres://..."``)
                dev (bool):       Whether this is a dev dependency
    """

    MANIFEST_FILES: list[str] = [".env", ".env.example", ".env.local", ".env.production", ".env.development"]

    def parse(self, path: Path, repo_root: Path) -> list[dict]:
        """Parse a ``.env`` file and return one dependency per variable.

        Args:
            path: Absolute path to the manifest file.
            repo_root: Absolute path to the repository root (for computing
                       relative paths).

        Returns:
            A list of raw dependency dicts. OKF wraps each into a
            ``Concept(type="Dependency")`` and writes it to the bundle.
        """
        deps: list[dict] = []
        try:
            text = path.read_bytes().decode("utf-8")
        except Exception:
            return deps

        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            val = val.strip().strip("\"'")
            if key and val:
                deps.append({
                    "name": key,
                    "ecosystem": "dotenv",
                    "version": f"={val}",
                    "dev": False,
                })
        return deps
