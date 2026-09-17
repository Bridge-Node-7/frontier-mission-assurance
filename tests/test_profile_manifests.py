from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_profile_manifests_validate_current_tree():
    result = subprocess.run(
        [sys.executable, "scripts/validate_profile_manifests.py", "."],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "PROFILE MANIFESTS PASS" in result.stdout


def test_profile_manifest_ids_are_unique_and_match_directories():
    manifests = []
    for path in sorted((ROOT / "profiles").glob("*/profile.yaml")):
        manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
        manifests.append((path.parent.name, manifest["profile_id"]))

    assert manifests
    assert all(directory == profile_id for directory, profile_id in manifests)
    assert len({profile_id for _, profile_id in manifests}) == len(manifests)


def test_profile_manifest_schema_has_stable_identifier():
    schema = json.loads(
        (ROOT / "schemas" / "profile-manifest.schema.json").read_text(encoding="utf-8")
    )
    assert schema["$id"] == (
        "https://bridge-node-7.github.io/frontier-mission-assurance/profile-manifest.schema.json"
    )
    assert schema["properties"]["manifest_version"]["const"] == "1.0"
