from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_ftqc_case.py"
BASELINE = (
    ROOT
    / "profiles"
    / "ftqc-assurance"
    / "examples"
    / "synthetic-neutral-atom"
    / "baseline"
)


def _load_tool():
    spec = importlib.util.spec_from_file_location("ftqc_case_tool_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


tool = _load_tool()


def _private_case(tmp_path: Path) -> Path:
    case = tmp_path / "private-case"
    shutil.copytree(BASELINE, case)

    for name in (
        "system-concept.json",
        "resource-estimate-receipt.json",
        "evidence-envelopes.json",
        "expert-adjudications.json",
    ):
        path = case / name
        data = json.loads(path.read_text(encoding="utf-8"))
        data["record_class"] = "private"
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    resource_path = case / "resource-estimate-receipt.json"
    resource = json.loads(resource_path.read_text(encoding="utf-8"))
    resource["result"]["synthetic_only"] = False
    resource_path.write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")

    graph_path = case / "assurance-graph.yaml"
    graph = yaml.safe_load(graph_path.read_text(encoding="utf-8"))
    graph["metadata"]["record_class"] = "private"
    graph_path.write_text(yaml.safe_dump(graph, sort_keys=False), encoding="utf-8")
    return case


def test_private_real_resource_estimate_case_validates(tmp_path):
    case = _private_case(tmp_path)
    errors, warnings, docs = tool.validate_case(ROOT, case)
    assert errors == []
    assert docs["resource"]["result"]["synthetic_only"] is False
    assert docs["system"]["record_class"] == "private"
    assert isinstance(warnings, list)


def test_private_case_cli_writes_decision_basis_report(tmp_path):
    case = _private_case(tmp_path)
    report = tmp_path / "decision-basis.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(case),
            "--root",
            str(ROOT),
            "--report",
            str(report),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "FTQC CASE PASS" in completed.stdout
    assert "RECORD CLASS: private" in completed.stdout
    text = report.read_text(encoding="utf-8")
    assert "# FTQC Decision Basis" in text
    assert "Disposition: **HOLD**" in text
    assert "Synthetic only: **FALSE**" in text
    assert "quantum performance" in text


def test_synthetic_case_cannot_claim_non_synthetic_result(tmp_path):
    case = tmp_path / "synthetic-case"
    shutil.copytree(BASELINE, case)
    resource_path = case / "resource-estimate-receipt.json"
    resource = json.loads(resource_path.read_text(encoding="utf-8"))
    resource["result"]["synthetic_only"] = False
    resource_path.write_text(json.dumps(resource, indent=2) + "\n", encoding="utf-8")

    errors, _, _ = tool.validate_case(ROOT, case)
    assert "synthetic FTQC cases must declare result.synthetic_only=true" in errors


def test_case_rejects_mixed_record_classes(tmp_path):
    case = _private_case(tmp_path)
    path = case / "expert-adjudications.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["record_class"] = "synthetic"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    errors, _, _ = tool.validate_case(ROOT, case)
    assert "FTQC case records must use one consistent record_class" in errors


def test_case_cannot_approve_with_declared_applicability_gate(tmp_path):
    case = _private_case(tmp_path)
    path = case / "decision-receipt.yaml"
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    data["decision"]["disposition"] = "APPROVE"
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    errors, _, _ = tool.validate_case(ROOT, case)
    assert any("cannot APPROVE" in item for item in errors)


def test_case_requires_resource_applicability_envelope(tmp_path):
    case = _private_case(tmp_path)
    path = case / "resource-estimate-receipt.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["applicability_envelope_ref"] = "ENV-MISSING"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    errors, _, _ = tool.validate_case(ROOT, case)
    assert "resource-estimate applicability_envelope_ref does not resolve" in errors
