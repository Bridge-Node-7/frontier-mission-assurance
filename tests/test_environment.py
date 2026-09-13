from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import yaml

import frontier_assurance.receipt as receipt_module
from frontier_assurance.io import load_structured
from frontier_assurance.receipt import reproduce_receipt, verify_receipt_inputs

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "environment_fingerprint.py"
RECEIPT = ROOT / "examples" / "research_receipt" / "receipt.yaml"


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


def test_receipt_v2_binds_declared_code_hash(tmp_path):
    dst = tmp_path / "receipt-demo"
    shutil.copytree(RECEIPT.parent, dst)
    receipt_path = dst / "receipt.yaml"
    doc = load_structured(receipt_path)
    doc["code"][0]["sha256"] = "0" * 64
    receipt_path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    result = verify_receipt_inputs(receipt_path)
    assert not result.ok
    assert any("code[0]: sha256 mismatch" in error for error in result.errors)


def test_receipt_v2_command_must_reference_entrypoint(tmp_path):
    dst = tmp_path / "receipt-demo"
    shutil.copytree(RECEIPT.parent, dst)
    receipt_path = dst / "receipt.yaml"
    doc = load_structured(receipt_path)
    doc["experiment"]["command"] = "python alternate.py"
    receipt_path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")

    result = reproduce_receipt(receipt_path, timeout=30)
    assert not result.ok
    assert any("declared experiment.entrypoint" in error for error in result.errors)


def test_fresh_reproduction_does_not_reuse_preexisting_output(tmp_path, monkeypatch):
    dst = tmp_path / "receipt-demo"
    shutil.copytree(RECEIPT.parent, dst)

    def no_output_run(*args, **kwargs):
        workspace = Path(kwargs["cwd"])
        assert not (workspace / "outputs" / "result.json").exists()
        return SimpleNamespace(returncode=0, stdout="", stderr="")

    monkeypatch.setattr(receipt_module.subprocess, "run", no_output_run)
    result = reproduce_receipt(dst / "receipt.yaml", timeout=30)
    assert not result.ok
    assert any("missing artifact" in error for error in result.errors)
