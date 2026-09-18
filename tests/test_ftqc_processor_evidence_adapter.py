from __future__ import annotations

import hashlib
import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ftqc_processor_evidence_adapter.py"
SPEC = importlib.util.spec_from_file_location("ftqc_processor_evidence_adapter", MODULE_PATH)
assert SPEC and SPEC.loader
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)

ENVELOPE_SCHEMA = json.loads(
    (
        ROOT
        / "profiles"
        / "ftqc-assurance"
        / "schemas"
        / "evidence-validity-envelope.schema.json"
    ).read_text(encoding="utf-8")
)


def canonical_sha(value):
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


def experiment(*, reproduction_state="GENERATED"):
    doc = {
        "producer": {"application": "naftk", "release": "0.5.0"},
        "contract": {
            "id": adapter.EXPERIMENT_CONTRACT_ID,
            "version": adapter.EXPERIMENT_CONTRACT_VERSION,
            "schema_digest": adapter.EXPERIMENT_SCHEMA_SHA256,
        },
        "experiment": {
            "id": "SYNTHETIC-DECODER-BACKLOG-001",
            "kind": "decoder_backlog",
            "configuration_ref": "synthetic:decoder-backlog:v1",
        },
        "inputs": {"rounds": 1000, "seed": 7},
        "result": {
            "utilisation": 0.60,
            "mean_service_us": 720.0,
            "stability_boundary_us": 774.0,
            "final_backlog_rounds": 0.0,
            "max_backlog_rounds": 2.0,
            "p_backlog_exceeds": 0.0,
            "diverged": False,
        },
        "provenance": {"python": "3.12", "numpy": "2.0", "platform": "synthetic"},
        "reproduction_state": reproduction_state,
        "limitations": ["Synthetic model evidence only."],
        "not_claimed": ["Hardware validation."],
    }
    payload = deepcopy(doc)
    doc["integrity"] = {
        "inputs_sha256": canonical_sha(doc["inputs"]),
        "scientific_payload_sha256": canonical_sha(doc["result"]),
        "evidence_run_sha256": canonical_sha(
            {"inputs": doc["inputs"], "result": doc["result"]}
        ),
        "artifact_payload_sha256": canonical_sha(payload),
    }
    return doc


def receipt(exp, exp_sha, *, status="WITHIN_TARGET_ENVELOPE", state="SAME_DECLARED_CONFIGURATION"):
    identical = {
        "SAME_DECLARED_CONFIGURATION": True,
        "CROSS_ARCHITECTURE": False,
        "NOT_APPLICABLE": None,
    }[state]
    doc = {
        "producer": {
            "application": "neutral-atom-ftqc-processor-contract",
            "release": "0.4.0",
        },
        "contract": {
            "id": adapter.PROCESSOR_CONTRACT_ID,
            "version": adapter.PROCESSOR_CONTRACT_VERSION,
            "schema_digest": adapter.PROCESSOR_SCHEMA_SHA256,
        },
        "input_evidence": [
            {
                "artifact_sha256": exp_sha,
                "contract_id": exp["contract"]["id"],
                "contract_version": exp["contract"]["version"],
                "schema_digest": exp["contract"]["schema_digest"],
                "producer_application": exp["producer"]["application"],
                "producer_release": exp["producer"]["release"],
                "experiment_id": exp["experiment"]["id"],
                "experiment_kind": exp["experiment"]["kind"],
            }
        ],
        "evaluation_type": "decoder_backlog_envelope",
        "technical_scope": "Synthetic bounded processor criterion.",
        "architecture_comparison": {
            "state": state,
            "architectures_identical": identical,
        },
        "status": status,
        "metrics": {"utilisation": 0.60, "diverged": False},
        "target_envelope": {"max_utilisation": 0.70},
        "gap": {"utilisation_minus_target": -0.10},
        "reopen_when": ["Trusted technical evidence changes."],
        "not_claimed": ["Mission approval."],
    }
    payload = deepcopy(doc)
    doc["integrity"] = {
        "input_artifact_sha256": exp_sha,
        "artifact_payload_sha256": canonical_sha(payload),
    }
    return doc


def adapt(*, status="WITHIN_TARGET_ENVELOPE", state="SAME_DECLARED_CONFIGURATION", reproduction="GENERATED"):
    exp = experiment(reproduction_state=reproduction)
    exp_sha = "a" * 64
    rec = receipt(exp, exp_sha, status=status, state=state)
    result = adapter.adapt_verified_documents(
        exp,
        experiment_sha256=exp_sha,
        receipt=rec,
        receipt_sha256="b" * 64,
        evidence_ref="TECH-EVIDENCE-001",
    )
    return exp, rec, result


def test_generated_simulation_maps_to_declared_not_assessed_state():
    _, _, result = adapt()
    fma = result["fma_evidence"]
    assert fma["evidence_class"] == "SIMULATED"
    assert fma["authority_state"] == "DECLARED"
    assert fma["reproduction_state"] == "NOT_ASSESSED"
    assert fma["applicability"] == "IN_SCOPE"
    assert fma["assurance_effect"] == "RE-EVALUATION_OPPORTUNITY"
    assert fma["expert_review_required"] is True
    assert fma["automatic_decision_authorized"] is False
    assert not list(
        Draft202012Validator(ENVELOPE_SCHEMA).iter_errors(
            result["evidence_validity_envelope"]
        )
    )


def test_reproduced_state_is_preserved_but_does_not_establish_authority():
    _, _, result = adapt(reproduction="REPRODUCED")
    assert result["fma_evidence"]["reproduction_state"] == "REPRODUCED"
    assert result["fma_evidence"]["authority_state"] == "DECLARED"
    assert result["fma_evidence"]["automatic_decision_authorized"] is False


def test_cross_architecture_remains_review_required():
    _, _, result = adapt(state="CROSS_ARCHITECTURE")
    assert result["fma_evidence"]["applicability"] == "REVIEW_REQUIRED"
    envelope = result["evidence_validity_envelope"]["envelopes"][0]
    assert envelope["review"]["status"] == "REVIEW_REQUIRED"
    assert envelope["review"]["decision_gate"] is True


def test_unfavorable_technical_status_remains_bounded_review_not_decision():
    _, _, result = adapt(status="NOT_YET_WITHIN_TARGET_ENVELOPE")
    assert result["fma_evidence"]["processor_technical_status"] == "NOT_YET_WITHIN_TARGET_ENVELOPE"
    assert result["fma_evidence"]["assurance_effect"] == "REVIEW_REQUIRED"
    assert result["fma_evidence"]["automatic_decision_authorized"] is False


def test_exact_single_input_linkage_is_required():
    exp = experiment()
    rec = receipt(exp, "a" * 64)
    rec["input_evidence"].append(deepcopy(rec["input_evidence"][0]))
    payload = {key: value for key, value in rec.items() if key != "integrity"}
    rec["integrity"]["artifact_payload_sha256"] = canonical_sha(payload)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="exactly one"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_receipt_cannot_substitute_different_experiment_artifact():
    exp = experiment()
    rec = receipt(exp, "c" * 64)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="linkage mismatch"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_experiment_internal_tamper_fails():
    exp = experiment()
    exp["result"]["utilisation"] = 0.99
    rec = receipt(exp, "a" * 64)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="internal integrity"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_processor_internal_tamper_fails():
    exp = experiment()
    rec = receipt(exp, "a" * 64)
    rec["metrics"]["utilisation"] = 0.99
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="payload integrity"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_contradictory_architecture_state_fails_even_if_upstream_schema_were_bypassed():
    exp = experiment()
    rec = receipt(exp, "a" * 64)
    rec["architecture_comparison"]["architectures_identical"] = False
    payload = {key: value for key, value in rec.items() if key != "integrity"}
    rec["integrity"]["artifact_payload_sha256"] = canonical_sha(payload)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="contradictory"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_unreviewed_future_producer_rejected():
    exp = experiment()
    exp["producer"]["release"] = "0.6.0"
    payload = {key: value for key, value in exp.items() if key != "integrity"}
    exp["integrity"]["artifact_payload_sha256"] = canonical_sha(payload)
    rec = receipt(exp, "a" * 64)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="not explicitly reviewed"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_unknown_experiment_kind_requires_explicit_mapping():
    exp = experiment()
    exp["experiment"]["kind"] = "future_hardware_measurement"
    payload = {key: value for key, value in exp.items() if key != "integrity"}
    exp["integrity"]["artifact_payload_sha256"] = canonical_sha(payload)
    rec = receipt(exp, "a" * 64)
    with pytest.raises(adapter.FTQCEvidenceAdapterError, match="no reviewed"):
        adapter.adapt_verified_documents(
            exp,
            experiment_sha256="a" * 64,
            receipt=rec,
            receipt_sha256="b" * 64,
            evidence_ref="TECH-EVIDENCE-001",
        )


def test_schema_digest_constants_are_exact_reviewed_contract_identities():
    assert adapter.EXPERIMENT_SCHEMA_SHA256 == (
        "923f28bd45729008f54eea09281caacf359311f9a7e0486344d41a336a4c3c33"
    )
    assert adapter.PROCESSOR_SCHEMA_SHA256 == (
        "1e8c164ddabbf1f6a1f0274e3b3225ec2ba81a1a566a33d69d00b91e1788ccdb"
    )
