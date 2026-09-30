from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys

import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "evaluate_ftqc_reference.py"


def _load_evaluator():
    spec = importlib.util.spec_from_file_location("ftqc_reference_test", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


evaluator = _load_evaluator()


def test_ftqc_profile_release_surface_is_present():
    required = [
        ROOT / "profiles" / "ftqc-assurance" / "README.md",
        ROOT / "profiles" / "ftqc-assurance" / "PROFILE_CONTRACT.md",
        ROOT / "profiles" / "ftqc-assurance" / "ASSURANCE_SCOPE.md",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "ftqc-system-concept.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "resource-estimate-receipt.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "evidence-validity-envelope.schema.json",
        ROOT / "profiles" / "ftqc-assurance" / "schemas" / "expert-adjudication-record.schema.json",
        ROOT / "scripts" / "validate_ftqc_assurance.py",
        ROOT / "scripts" / "evaluate_ftqc_reference.py",
        ROOT / "scripts" / "validate_ftqc_case.py",
        ROOT / "scripts" / "compare_ftqc_cases.py",
        ROOT / "profiles" / "ftqc-assurance" / "docs" / "GOVERNED_CASE_QUICKSTART.md",
    ]
    assert all(path.is_file() for path in required)


def test_profile_validator_passes():
    completed = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_ftqc_assurance.py"), str(ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert "FTQC ASSURANCE PROFILE PASS" in completed.stdout


def test_changed_assumption_produces_expected_impact():
    result = evaluator.evaluate_case(ROOT)
    expected = json.loads(
        (ROOT / "profiles" / "ftqc-assurance" / "examples" / "synthetic-neutral-atom" / "changed-assumption" / "expected-impact.json").read_text(encoding="utf-8")
    )
    assert result["change"] == expected
    assert result["baseline"]["technical_decision_readiness"] == "HOLD"


def test_evaluator_is_deterministic_and_human_readable():
    command = [sys.executable, str(SCRIPT), str(ROOT)]
    first = subprocess.run(command, capture_output=True, text=True, check=False)
    second = subprocess.run(command, capture_output=True, text=True, check=False)
    assert first.returncode == 0, first.stdout + first.stderr
    assert second.returncode == 0, second.stdout + second.stderr
    assert first.stdout == second.stdout
    assert "SOFTWARE / CONTRACT VALIDATION\nPASS" in first.stdout
    assert "TECHNICAL DECISION READINESS\nHOLD" in first.stdout
    assert "decision reopen required: TRUE" in first.stdout
    assert first.stdout.rstrip().endswith("RESULT - FTQC REFERENCE EVALUATION PASS")


def test_declared_applicability_does_not_become_established_by_structure():
    envelopes = json.loads(
        (ROOT / "profiles" / "ftqc-assurance" / "examples" / "synthetic-neutral-atom" / "baseline" / "evidence-envelopes.json").read_text(encoding="utf-8")
    )
    loss = next(item for item in envelopes["envelopes"] if item["envelope_id"] == "ENV-LOSS-001")
    assert loss["basis"]["type"] == "declared_assumption"
    assert loss["review"]["authority_state"] == "DECLARED"
    assert loss["review"]["decision_gate"] is True


def test_stable_release_reverifies_ftqc_profile_and_reference():
    workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    assert "python scripts/validate_ftqc_assurance.py ." in workflow
    assert "python scripts/evaluate_ftqc_reference.py ." in workflow
    assert workflow.count("scripts/validate_ftqc_assurance.py .") >= 2
    assert workflow.count("scripts/evaluate_ftqc_reference.py .") >= 2
    assert workflow.count("scripts/validate_ftqc_case.py") >= 2
    assert workflow.count("scripts/compare_ftqc_cases.py") >= 2
    assert "PYTHONPATH=src python scripts/validate_ftqc_case.py" in workflow
    assert "PYTHONPATH=src python scripts/compare_ftqc_cases.py" in workflow


def test_external_reported_resource_estimate_boundary_is_explicit():
    schema = json.loads(
        (
            ROOT
            / "profiles"
            / "ftqc-assurance"
            / "schemas"
            / "resource-estimate-receipt.schema.json"
        ).read_text(encoding="utf-8")
    )
    assert schema["properties"]["result"]["properties"]["synthetic_only"]["type"] == "boolean"

    scope = (
        ROOT / "profiles" / "ftqc-assurance" / "ASSURANCE_SCOPE.md"
    ).read_text(encoding="utf-8")
    adoption = (ROOT / "docs" / "EXTERNAL_RESEARCH_ADOPTION.md").read_text(
        encoding="utf-8"
    )

    for text in (scope, adoption):
        assert "external" in text.lower()
        assert "reported" in text.lower()
        assert "freshly reproduced" in text.lower()
        assert "applicab" in text.lower()

VALIDATE_CASE = ROOT / "scripts" / "validate_ftqc_case.py"
COMPARE_CASES = ROOT / "scripts" / "compare_ftqc_cases.py"
BASELINE_CASE = (
    ROOT
    / "profiles"
    / "ftqc-assurance"
    / "examples"
    / "synthetic-neutral-atom"
    / "baseline"
)


def _copy_case(tmp_path: Path, name: str) -> Path:
    target = tmp_path / name
    shutil.copytree(BASELINE_CASE, target)
    return target


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _read_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _write_yaml(path: Path, value: dict) -> None:
    path.write_text(yaml.safe_dump(value, sort_keys=False), encoding="utf-8")


def _validate_case(case_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATE_CASE), str(case_dir)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _compare_cases(previous: Path, current: Path) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            str(COMPARE_CASES),
            str(previous),
            str(current),
            "--json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return json.loads(completed.stdout)["result"]


def test_governed_case_rejects_duplicate_assumption_ids(tmp_path):
    case_dir = _copy_case(tmp_path, "duplicate-assumption")
    path = case_dir / "system-concept.json"
    system = _read_json(path)
    system["assumptions"].append(dict(system["assumptions"][0]))
    _write_json(path, system)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "duplicate system assumption id" in completed.stdout


def test_governed_case_recomputes_applicability(tmp_path):
    case_dir = _copy_case(tmp_path, "applicability-contradiction")
    path = case_dir / "system-concept.json"
    system = _read_json(path)
    loss = next(
        item for item in system["assumptions"] if item["id"] == "ASSUMPTION-LOSS-001"
    )
    loss["value"] = "changed-regime"
    _write_json(path, system)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "computes outside envelope" in completed.stdout


def test_governed_case_blocks_approve_with_stale_resource(tmp_path):
    case_dir = _copy_case(tmp_path, "stale-approve")
    resource_path = case_dir / "resource-estimate-receipt.json"
    resource = _read_json(resource_path)
    resource["review_state"] = "STALE"
    _write_json(resource_path, resource)

    decision_path = case_dir / "decision-receipt.yaml"
    decision = _read_yaml(decision_path)
    decision["decision"]["disposition"] = "APPROVE"
    _write_yaml(decision_path, decision)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "review_state is STALE" in completed.stdout
    assert "decision cannot APPROVE" in completed.stdout


def test_exact_receipt_ref_must_resolve_and_verify(tmp_path):
    case_dir = _copy_case(tmp_path, "missing-exact-receipt")
    path = case_dir / "resource-estimate-receipt.json"
    resource = _read_json(path)
    resource["provenance"] = {
        "status": "EXACT_RECEIPT_REF",
        "research_receipt_ref": "receipts/missing.yaml",
    }
    _write_json(path, resource)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "research_receipt_ref does not resolve" in completed.stdout


def test_governed_case_rejects_duplicate_expert_review_ids(tmp_path):
    case_dir = _copy_case(tmp_path, "duplicate-review")
    path = case_dir / "expert-adjudications.json"
    experts = _read_json(path)
    experts["reviews"].append(dict(experts["reviews"][0]))
    _write_json(path, experts)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "duplicate expert review id" in completed.stdout


def test_supported_independent_review_requires_reviewer_identity(tmp_path):
    case_dir = _copy_case(tmp_path, "independent-review-without-reviewer")
    path = case_dir / "expert-adjudications.json"
    experts = _read_json(path)
    review = experts["reviews"][0]
    review["review_class"] = "INDEPENDENT_VV_REVIEW"
    review["reviewer_ref"] = None
    _write_json(path, experts)

    completed = _validate_case(case_dir)

    assert completed.returncode != 0
    assert "requires reviewer_ref" in completed.stdout


def test_comparison_surfaces_removed_dependency_as_governance_change(tmp_path):
    previous = _copy_case(tmp_path, "previous")
    current = _copy_case(tmp_path, "current")
    graph_path = current / "assurance-graph.yaml"
    graph = _read_yaml(graph_path)
    removed = next(
        edge
        for edge in graph["edges"]
        if edge["from"] == "DECISION-001"
        and edge["to"] == "CLAIM-003"
        and edge["relation"] == "depends_on"
    )
    graph["edges"].remove(removed)
    _write_yaml(graph_path, graph)

    result = _compare_cases(previous, current)

    assert result["governance_review_required"] is True
    assert removed in result["graph_changes"]["removed_relations"]


def test_comparison_surfaces_evidence_envelope_governance_change(tmp_path):
    previous = _copy_case(tmp_path, "previous-envelope")
    current = _copy_case(tmp_path, "current-envelope")
    path = current / "evidence-envelopes.json"
    envelopes = _read_json(path)
    resource_envelope = next(
        item for item in envelopes["envelopes"] if item["envelope_id"] == "ENV-RESOURCE-001"
    )
    scale = next(
        item
        for item in resource_envelope["applicability"]["conditions"]
        if item["subject"] == "assumption:ASSUMPTION-SCALE-001"
    )
    scale["value"] = [100, 2000]
    _write_json(path, envelopes)

    result = _compare_cases(previous, current)

    assert result["governance_review_required"] is True
    changed = {
        item["envelope_id"]: item["changed_fields"]
        for item in result["envelope_changes"]["changed"]
    }
    assert "applicability" in changed["ENV-RESOURCE-001"]


def test_comparison_surfaces_resource_and_decision_mutations(tmp_path):
    previous = _copy_case(tmp_path, "previous-records")
    current = _copy_case(tmp_path, "current-records")

    resource_path = current / "resource-estimate-receipt.json"
    resource = _read_json(resource_path)
    resource["estimator"]["version"] = "v0.2"
    _write_json(resource_path, resource)

    decision_path = current / "decision-receipt.yaml"
    decision = _read_yaml(decision_path)
    decision["decision"]["rationale"] = "Updated governed rationale."
    _write_yaml(decision_path, decision)

    result = _compare_cases(previous, current)

    assert "estimator" in result["resource_estimate_changes"]
    assert "rationale" in result["decision_changes"]
    assert result["governance_review_required"] is True

