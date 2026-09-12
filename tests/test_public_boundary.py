from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "public_boundary_scan.py"


def _scan(path: Path):
    return subprocess.run(
        [sys.executable, str(SCANNER), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_public_boundary_scanner_rejects_unapproved_external_url(tmp_path):
    (tmp_path / "README.md").write_text("https://" + "example.invalid/private", encoding="utf-8")
    result = _scan(tmp_path)
    assert result.returncode == 2
    assert "unapproved external URL" in result.stdout


def test_public_boundary_scanner_rejects_risky_binary_extension(tmp_path):
    (tmp_path / "screenshot.png").write_bytes(b"not-a-real-image")
    result = _scan(tmp_path)
    assert result.returncode == 2
    assert "forbidden sensitive-looking file" in result.stdout
