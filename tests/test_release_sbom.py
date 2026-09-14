from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_release_sbom.py"


def test_release_sbom_is_deterministic_and_binds_wheel(tmp_path: Path):
    wheel = tmp_path / "frontier_mission_assurance-9.9.9-py3-none-any.whl"
    metadata = (
        "Metadata-Version: 2.4\n"
        "Name: frontier-mission-assurance\n"
        "Version: 9.9.9\n"
        "Requires-Dist: PyYAML>=6.0\n"
        "\n"
    )
    with zipfile.ZipFile(wheel, "w") as archive:
        archive.writestr(
            "frontier_mission_assurance-9.9.9.dist-info/METADATA",
            metadata,
        )
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    for output in (first, second):
        subprocess.run(
            [sys.executable, str(SCRIPT), str(wheel), str(output)],
            check=True,
        )
    assert first.read_bytes() == second.read_bytes()
    document = json.loads(first.read_text(encoding="utf-8"))
    component = document["metadata"]["component"]
    expected = hashlib.sha256(wheel.read_bytes()).hexdigest()
    assert component["hashes"] == [{"alg": "SHA-256", "content": expected}]
    assert component["version"] == "9.9.9"
    assert document["components"][0]["name"] == "PyYAML"
    assert document["components"][0]["properties"][0]["value"] == "PyYAML>=6.0"
