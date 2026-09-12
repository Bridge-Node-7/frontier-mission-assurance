from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

PROFILE = Path("profiles/scientific-discovery")
SCHEMAS = PROFILE / "schemas"
EXAMPLE = PROFILE / "examples" / "synthetic-discovery"

DOCUMENTS = {
    "passport": ("discovery-passport.schema.json", "discovery-passport.yaml"),
    "priority": ("research-priority-receipt.schema.json", "research-priority-receipt.yaml"),
    "boundary": ("research-boundary-attestation.schema.json", "research-boundary-attestation.yaml"),
    "proof": ("formal-proof-record.schema.json", "formal-proof-record.yaml"),
    "replication": ("replication-receipt.schema.json", "replication-receipt.yaml"),
    "agent": ("agent-provenance-ref.schema.json", "agent-provenance-ref.yaml"),
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: document must be a mapping")
    return data


def validate_profile(root: Path) -> list[str]:
    errors: list[str] = []
    docs: dict[str, dict] = {}

    for key, (schema_name, doc_name) in DOCUMENTS.items():
        schema_path = root / SCHEMAS / schema_name
        doc_path = root / EXAMPLE / doc_name
        try:
            schema = _load_json(schema_path)
            Draft202012Validator.check_schema(schema)
            doc = _load_yaml(doc_path)
            docs[key] = doc
            schema_errors = sorted(
                Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(doc),
                key=lambda e: list(e.path),
            )
            for error in schema_errors:
                location = ".".join(str(item) for item in error.path) or "<root>"
                errors.append(f"{doc_name}:{location}: {error.message}")
        except Exception as exc:  # noqa: BLE001 - report all bounded validation failures
            errors.append(f"{doc_name}: {exc}")

    if errors or len(docs) != len(DOCUMENTS):
        return errors

    discovery_id = docs["passport"]["discovery_id"]
    for key in ("priority", "boundary", "proof", "replication", "agent"):
        if docs[key]["discovery_id"] != discovery_id:
            errors.append(f"{key}: discovery_id does not match passport")

    passport = docs["passport"]
    if passport.get("metadata", {}).get("synthetic") is not True:
        errors.append("passport: public worked example must declare metadata.synthetic=true")

    if passport["attribution"]["priority_receipt_ref"] != docs["priority"]["receipt_id"]:
        errors.append("passport: priority_receipt_ref does not resolve")
    if (
        passport["provenance"]["research_boundary_attestation_ref"]
        != docs["boundary"]["attestation_id"]
    ):
        errors.append("passport: research_boundary_attestation_ref does not resolve")
    if passport["verification"]["formal_proof_ref"] != docs["proof"]["record_id"]:
        errors.append("passport: formal_proof_ref does not resolve")

    replication_ids = {docs["replication"]["receipt_id"]}
    missing_replications = set(passport["verification"]["replication_refs"]) - replication_ids
    if missing_replications:
        errors.append(f"passport: unresolved replication refs: {sorted(missing_replications)}")

    agent_ids = {docs["agent"]["run_id"]}
    missing_agents = set(passport["provenance"]["agent_provenance_refs"]) - agent_ids
    if missing_agents:
        errors.append(f"passport: unresolved agent provenance refs: {sorted(missing_agents)}")

    priority = docs["priority"]
    anchor = priority["time_evidence"]["external_anchor"]
    signature = priority["signature_evidence"]
    state = priority["priority_state"]
    if state == "EXTERNALLY_ANCHORED" and not (
        isinstance(anchor, dict) and anchor.get("verified") is True
    ):
        errors.append("priority: EXTERNALLY_ANCHORED requires verified external anchor evidence")
    if state == "SIGNATURE_VERIFIED" and not (
        isinstance(signature, dict) and signature.get("verified") is True
    ):
        errors.append("priority: SIGNATURE_VERIFIED requires verified signature evidence")
    if state != "UNANCHORED" and anchor is None and signature is None:
        errors.append("priority: local time alone cannot establish trusted priority")

    boundary = docs["boundary"]
    if boundary["assurance_semantics"] != "DECLARATION_ONLY":
        errors.append("boundary: attestation must remain declaration-only")

    proof = docs["proof"]
    proof_checker_passed = proof["checker"]["state"] == "PASS"
    spec_state = proof["specification_equivalence"]["state"]
    if (
        proof_checker_passed
        and spec_state != "CONFIRMED"
        and passport["verification"]["disposition"] == "PASS"
    ):
        errors.append(
            "passport: proof-checker PASS cannot become overall PASS while "
            "specification equivalence is unresolved"
        )

    replication = docs["replication"]
    if replication["result"] != "REPRODUCED" and passport["verification"]["disposition"] == "PASS":
        errors.append("passport: overall PASS requires completed independent reproduction")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_profile(root)
    if errors:
        print("SCIENTIFIC DISCOVERY PROFILE FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 2
    print("SCIENTIFIC DISCOVERY PROFILE PASS")
    print("NOTE: PASS establishes only the declared contract and synthetic-case invariants.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
