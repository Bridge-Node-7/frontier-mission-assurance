from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "scientific-discovery"
SCHEMAS = PROFILE / "schemas"
EXAMPLE = PROFILE / "examples" / "synthetic-discovery"


def _load_schema(name: str) -> dict:
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def _load_example(name: str) -> dict:
    return yaml.safe_load((EXAMPLE / name).read_text(encoding="utf-8"))


def _validator_module():
    path = ROOT / "scripts" / "validate_scientific_discovery.py"
    spec = importlib.util.spec_from_file_location("validate_scientific_discovery", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_scientific_discovery_schemas_are_valid_draft_2020_12():
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        Draft202012Validator.check_schema(json.loads(path.read_text(encoding="utf-8")))


def test_scientific_discovery_examples_conform_to_schemas():
    cases = {
        "discovery-passport.yaml": "discovery-passport.schema.json",
        "research-priority-receipt.yaml": "research-priority-receipt.schema.json",
        "research-boundary-attestation.yaml": "research-boundary-attestation.schema.json",
        "formal-proof-record.yaml": "formal-proof-record.schema.json",
        "replication-receipt.yaml": "replication-receipt.schema.json",
        "agent-provenance-ref.yaml": "agent-provenance-ref.schema.json",
    }
    for doc_name, schema_name in cases.items():
        Draft202012Validator(
            _load_schema(schema_name), format_checker=FormatChecker()
        ).validate(_load_example(doc_name))


def test_scientific_discovery_cross_record_validator_passes():
    module = _validator_module()
    assert module.validate_profile(ROOT) == []


def test_local_time_cannot_be_promoted_to_trusted_priority(tmp_path):
    import shutil

    module = _validator_module()
    profile_root = tmp_path
    target = profile_root / "profiles" / "scientific-discovery"
    target.mkdir(parents=True)
    shutil.copytree(SCHEMAS, target / "schemas")
    shutil.copytree(EXAMPLE, target / "examples" / "synthetic-discovery")
    priority_path = target / "examples" / "synthetic-discovery" / "research-priority-receipt.yaml"
    priority = yaml.safe_load(priority_path.read_text(encoding="utf-8"))
    priority["priority_state"] = "EXTERNALLY_ANCHORED"
    priority_path.write_text(yaml.safe_dump(priority, sort_keys=False), encoding="utf-8")
    errors = module.validate_profile(profile_root)
    assert any(
        "EXTERNALLY_ANCHORED requires verified external anchor evidence" in item
        for item in errors
    )


def test_research_boundary_is_declaration_not_enforcement():
    schema = _load_schema("research-boundary-attestation.schema.json")
    doc = _load_example("research-boundary-attestation.yaml")
    doc["assurance_semantics"] = "ENFORCEMENT_PROVEN"
    errors = list(Draft202012Validator(schema).iter_errors(doc))
    assert errors


def test_formal_checker_pass_does_not_collapse_specification_validation():
    proof = _load_example("formal-proof-record.yaml")
    passport = _load_example("discovery-passport.yaml")
    assert proof["checker"]["state"] == "PASS"
    assert proof["specification_equivalence"]["state"] == "PARTIAL"
    assert passport["verification"]["disposition"] == "REVIEW_REQUIRED"


def test_partial_replication_remains_visible():
    replication = _load_example("replication-receipt.yaml")
    passport = _load_example("discovery-passport.yaml")
    assert replication["result"] == "PARTIAL"
    assert passport["verification"]["disposition"] == "REVIEW_REQUIRED"


def test_synthetic_passport_is_explicitly_marked():
    passport = _load_example("discovery-passport.yaml")
    assert passport["metadata"]["synthetic"] is True
