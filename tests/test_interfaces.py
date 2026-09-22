from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ftqc_processor_evidence_adapter.py"
SPEC = importlib.util.spec_from_file_location("ftqc_processor_evidence_adapter_contract_test", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)



def test_interface_manifest_is_low_churn_and_exact() -> None:
    manifest = json.loads((ROOT / "INTERFACES.json").read_text(encoding="utf-8"))
    assert manifest["format"] == "bn7.interfaces/0.1"
    assert manifest["system"] == "frontier-mission-assurance"
    assert "application_version" not in manifest

    for entry in manifest["provides"]:
        path = ROOT / entry["schema_path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]

    accepted = {item["contract_id"]: item for item in manifest["accepts"]}
    assert accepted["na-ftqc.experiment-result"]["contract_version"] == "2.0.0"
    assert accepted["na-ftqc.experiment-result"]["sha256"] == adapter.EXPERIMENT_SCHEMA_SHA256
    assert accepted["na-ftqc.processor-evidence-receipt"]["contract_version"] == "2.0.0"
    assert accepted["na-ftqc.processor-evidence-receipt"]["sha256"] == adapter.PROCESSOR_SCHEMA_SHA256


def test_reviewed_producer_registry_preserves_explicit_human_review_boundary(tmp_path: Path) -> None:
    registry_path = ROOT / "profiles" / "ftqc-assurance" / "compatibility" / "reviewed-producers.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    assert registry["format"] == "bn7.fma.ftqc-reviewed-producers/0.1"
    assert registry["authority"] == "HUMAN_REVIEW_REQUIRED_FOR_CHANGES"

    experiment, processor = adapter._load_reviewed_producers(registry_path)
    assert experiment == {"naftk": {"0.5.0"}}
    assert processor == {"neutral-atom-ftqc-processor-contract": {"0.4.0"}}

    widened = copy.deepcopy(registry)
    widened["reviewed"][0]["releases"].append("0.6.0")
    candidate = tmp_path / "reviewed-producers.json"
    candidate.write_text(json.dumps(widened), encoding="utf-8")
    future_experiment, _ = adapter._load_reviewed_producers(candidate)
    assert "0.6.0" in future_experiment["naftk"]


def test_registry_fails_closed_on_contract_or_authority_drift(tmp_path: Path) -> None:
    registry_path = ROOT / "profiles" / "ftqc-assurance" / "compatibility" / "reviewed-producers.json"
    base = json.loads(registry_path.read_text(encoding="utf-8"))

    for mutation in ("authority", "schema"):
        candidate = copy.deepcopy(base)
        if mutation == "authority":
            candidate["authority"] = "AUTO_TRUST_LATEST"
        else:
            candidate["reviewed"][0]["schema_sha256"] = "0" * 64
        path = tmp_path / f"{mutation}.json"
        path.write_text(json.dumps(candidate), encoding="utf-8")
        with pytest.raises(RuntimeError):
            adapter._load_reviewed_producers(path)
