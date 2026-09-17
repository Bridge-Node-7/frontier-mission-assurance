import json
from copy import deepcopy
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def _schema(name: str):
    return json.loads((ROOT / "schemas" / name).read_text(encoding="utf-8"))


def test_schemas_are_valid_draft_2020_12():
    for name in (
        "assurance-graph.schema.json",
        "assurance-context.schema.json",
        "research-receipt.schema.json",
        "decision-receipt.schema.json",
    ):
        Draft202012Validator.check_schema(_schema(name))


def test_examples_conform_to_published_schemas():
    cases = [
        (
            "assurance-context.schema.json",
            ROOT / "examples" / "assurance_context" / "synthetic-changed-assumption.json",
        ),
        (
            "assurance-graph.schema.json",
            ROOT / "examples" / "frontier_program" / "graph.yaml",
        ),
        (
            "research-receipt.schema.json",
            ROOT / "examples" / "research_receipt" / "receipt.yaml",
        ),
        (
            "decision-receipt.schema.json",
            ROOT / "examples" / "frontier_program" / "decision-receipt.yaml",
        ),
    ]
    for schema_name, doc_path in cases:
        doc = yaml.safe_load(doc_path.read_text(encoding="utf-8"))
        Draft202012Validator(_schema(schema_name)).validate(doc)


def test_graph_schema_rejects_runtime_invalid_status_and_version():
    schema = _schema("assurance-graph.schema.json")
    doc = yaml.safe_load(
        (ROOT / "examples" / "frontier_program" / "graph.yaml").read_text(encoding="utf-8")
    )
    doc["graph_version"] = "2.0"
    assert list(Draft202012Validator(schema).iter_errors(doc))

    doc = yaml.safe_load(
        (ROOT / "examples" / "frontier_program" / "graph.yaml").read_text(encoding="utf-8")
    )
    doc["nodes"][0]["status"] = "mystery"
    assert list(Draft202012Validator(schema).iter_errors(doc))


def test_research_receipt_v2_rejects_empty_assurance_sections_and_missing_entrypoint():
    schema = _schema("research-receipt.schema.json")
    validator = Draft202012Validator(schema)
    original = yaml.safe_load(
        (ROOT / "examples" / "research_receipt" / "receipt.yaml").read_text(encoding="utf-8")
    )

    for section in ("code", "inputs", "outputs", "checks"):
        doc = deepcopy(original)
        doc[section] = []
        assert list(validator.iter_errors(doc)), section

    doc = deepcopy(original)
    doc["experiment"].pop("entrypoint")
    assert list(validator.iter_errors(doc))

    doc = deepcopy(original)
    doc["receipt_version"] = "1.0"
    assert list(validator.iter_errors(doc))
