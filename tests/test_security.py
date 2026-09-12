from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_runtime_package_has_no_network_client_imports():
    forbidden = {"requests", "httpx", "aiohttp", "socket", "urllib.request"}
    seen = set()
    for path in (ROOT / "src" / "frontier_assurance").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                seen.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                seen.add(node.module)
    assert not (forbidden & seen), sorted(forbidden & seen)
