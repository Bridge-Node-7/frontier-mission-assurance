from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "assurance-context.schema.json").read_text(encoding="utf-8"))
EXAMPLE = json.loads((ROOT / "examples" / "assurance_context" / "synthetic-changed-assumption.json").read_text(encoding="utf-8"))


def _errors(document: dict) -> list:
    return list(Draft202012Validator(SCHEMA).iter_errors(document))


def test_assurance_context_schema_and_source_neutral_example():
    Draft202012Validator.check_schema(SCHEMA)
    assert not _errors(EXAMPLE)
    assert EXAMPLE["handling"] == {"classification": "PUBLIC_REFERENCE", "contains_raw_evidence": False}


def test_assurance_context_fails_closed_on_identity_and_raw_evidence():
    unsupported = deepcopy(EXAMPLE)
    unsupported["contract_version"] = "0.2.0"
    assert _errors(unsupported)

    missing_identity = deepcopy(EXAMPLE)
    missing_identity["source_release"].pop("commit")
    assert _errors(missing_identity)

    raw_evidence = deepcopy(EXAMPLE)
    raw_evidence["raw_evidence"] = {"measurements": [1, 2, 3]}
    assert _errors(raw_evidence)


def test_assurance_context_preserves_bounded_epistemic_states():
    claim = EXAMPLE["affected_claims"][0]
    evidence = EXAMPLE["evidence_applicability_changes"][0]
    review = EXAMPLE["expert_reviews"][0]
    opportunity = EXAMPLE["reevaluation_opportunities"][0]

    assert EXAMPLE["decision"]["current_disposition"] == "HOLD"
    assert claim["authority_state"] == "DECLARED"
    assert claim["assurance_state"] == "REVIEW_REQUIRED"
    assert evidence["reproduction_state"] == "EXTERNAL_REPORTED"
    assert review["state"] == "REVIEW_REQUIRED" and review["reopened"] is True
    assert opportunity["state"] == "RE-EVALUATION_OPPORTUNITY"
