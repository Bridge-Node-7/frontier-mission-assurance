from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "compare_ftqc_cases.py"
PREVIOUS = (
    ROOT
    / "profiles"
    / "ftqc-assurance"
    / "examples"
    / "synthetic-neutral-atom"
    / "baseline"
)
CURRENT = (
    ROOT
    / "profiles"
    / "ftqc-assurance"
    / "examples"
    / "synthetic-neutral-atom"
    / "changed-assumption-case"
)


def _load_tool():
    scripts_dir = str(SCRIPT.parent)
    if scripts_dir not in sys.path:
        sys.path.insert(0, scripts_dir)
    spec = importlib.util.spec_from_file_location("ftqc_compare_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


tool = _load_tool()


def test_complete_changed_case_surfaces_decision_reopen():
    errors, warnings, result = tool.compare_cases(ROOT, PREVIOUS, CURRENT)
    assert errors == []
    assert isinstance(warnings, list)
    assert result["changed_assumptions"] == ["ASSUMPTION-LOSS-001"]
    assert result["context_changes"] == ["architecture_revision"]
    assert result["resource_estimates_stale"] == ["MODEL-RESOURCE-001"]
    assert result["evidence_outside_envelope"] == [
        "EVIDENCE-LOSS-001",
        "EXPERT-REVIEW-001",
        "MODEL-RESOURCE-001",
    ]
    assert result["expert_reviews_reopen"] == ["EXPERT-REVIEW-001"]
    assert "DECISION-001" in result["impacted_nodes"]
    assert result["decision_reopen_required"] is True


def test_compare_cli_writes_human_change_report(tmp_path):
    report = tmp_path / "change-impact.md"
    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            str(PREVIOUS),
            str(CURRENT),
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
    assert "FTQC CHANGE IMPACT PASS" in completed.stdout
    assert "DECISION REOPEN REQUIRED: TRUE" in completed.stdout
    text = report.read_text(encoding="utf-8")
    assert "# FTQC Change Impact" in text
    assert "OUTSIDE DECLARED ENVELOPE" in text
    assert "Reopen: `EXPERT-REVIEW-001`" in text
    assert "Decision reopen required: **TRUE**" in text


def test_compare_is_deterministic_json():
    command = [
        sys.executable,
        str(SCRIPT),
        str(PREVIOUS),
        str(CURRENT),
        "--root",
        str(ROOT),
        "--json",
    ]
    first = subprocess.run(command, capture_output=True, text=True, check=False)
    second = subprocess.run(command, capture_output=True, text=True, check=False)
    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert payload["status"] == "PASS"
    assert payload["result"]["decision_reopen_required"] is True


def test_compare_rejects_different_systems(tmp_path):
    current = tmp_path / "current"
    import shutil

    shutil.copytree(CURRENT, current)
    path = current / "system-concept.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["system_id"] = "DIFFERENT-SYSTEM"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    errors, _, _ = tool.compare_cases(ROOT, PREVIOUS, current)
    assert "previous/current FTQC cases must refer to the same system_id" in errors


def test_no_change_does_not_reopen_decision():
    errors, _, result = tool.compare_cases(ROOT, PREVIOUS, PREVIOUS)
    assert errors == []
    assert result["changed_assumptions"] == []
    assert result["context_changes"] == []
    assert result["resource_estimates_stale"] == []
    assert result["expert_reviews_reopen"] == []
    assert result["decision_reopen_required"] is False
