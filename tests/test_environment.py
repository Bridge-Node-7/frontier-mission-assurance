from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "environment_fingerprint.py"


def test_environment_fingerprint_excludes_identity_and_paths(tmp_path):
    out = tmp_path / "environment.json"
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    data = json.loads(out.read_text(encoding="utf-8"))
    assert set(data) == {"python", "implementation", "system", "machine", "packages"}
    rendered = json.dumps(data).lower()
    assert "hostname" not in rendered
    assert "username" not in rendered
    assert "/home/" not in rendered
    assert "\\users\\" not in rendered
