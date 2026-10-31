#!/usr/bin/env python3
"""Align VERSION/__init__, strip pre-tag CHANGELOG compare URLs."""
from __future__ import annotations
import json, re, sys
from pathlib import Path
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
COMPARE_HEADING_RE = re.compile(
    r"(^## \[\d+\.\d+\.\d+\])\(https://github\.com/[^\s)]+/compare/[^\s)]+\)( \(\d{4}-\d{2}-\d{2}\))",
    re.MULTILINE,
)
INIT_RE = re.compile(r'__version__\s*=\s*["\'][^"\']+["\']')
def main() -> int:
    root = Path(".").resolve()
    version = str(json.loads((root / ".release-please-manifest.json").read_text(encoding="utf-8")).get(".", "")).strip()
    if not VERSION_RE.fullmatch(version):
        print(f"FAIL: invalid manifest version {version!r}", file=sys.stderr); return 1
    vp = root / "VERSION"
    if vp.read_text(encoding="utf-8").strip() != version:
        vp.write_text(version + "\n", encoding="utf-8", newline="\n")
        print(f"PASS: aligned VERSION to {version}")
    else:
        print(f"PASS: VERSION already {version}")
    ip = root / "src/frontier_assurance/__init__.py"
    text = ip.read_text(encoding="utf-8")
    nt, n = INIT_RE.subn(f'__version__ = "{version}"', text, count=1)
    if n and nt != text:
        ip.write_text(nt, encoding="utf-8", newline="\n")
        print("PASS: aligned __init__.__version__")
    else:
        print("PASS: __init__ already aligned or pattern absent")
    cl = root / "CHANGELOG.md"
    text = cl.read_text(encoding="utf-8")
    rewritten, n = COMPARE_HEADING_RE.subn(r"\1\2", text, count=1)
    if n:
        cl.write_text(rewritten, encoding="utf-8", newline="\n")
        print("PASS: stripped pre-tag CHANGELOG compare URL")
    else:
        print("PASS: CHANGELOG compare heading already plain or absent")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
