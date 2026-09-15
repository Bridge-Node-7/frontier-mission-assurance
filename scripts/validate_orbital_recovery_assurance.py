"""Validate the bounded Orbital Recovery Assurance profile."""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from pathlib import Path

try:
    import jsonschema
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError:
    jsonschema = None
    SchemaError = ValidationError = ValueError

EXPECTED_PROFILE_VERSION = "0.5"
BENCHMARK_FLOAT_TOLERANCE = 1e-12


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _benchmark_equivalent(actual, expected) -> bool:
    """Compare benchmark records without treating float byte identity as a contract."""
    if isinstance(actual, bool) or isinstance(expected, bool):
        return actual is expected
    if isinstance(actual, (int, float)) and isinstance(expected, (int, float)):
        return math.isclose(
            float(actual),
            float(expected),
            rel_tol=BENCHMARK_FLOAT_TOLERANCE,
            abs_tol=BENCHMARK_FLOAT_TOLERANCE,
        )
    if isinstance(actual, dict) and isinstance(expected, dict):
        return actual.keys() == expected.keys() and all(
            _benchmark_equivalent(actual[key], expected[key]) for key in actual
        )
    if isinstance(actual, list) and isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _benchmark_equivalent(a, e) for a, e in zip(actual, expected)
        )
    return actual == expected


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    profile = root / "profiles" / "orbital-recovery-assurance"
    reference = profile / "reference"
    examples = profile / "examples" / "synthetic-recovery-case"
    schemas = profile / "schemas"

    ev = _load("ora_evidence_validation", reference / "evidence_validation.py")
    tm = _load("ora_timeline_metrics", reference / "timeline_metrics.py")
    sys.path.insert(0, str(reference))
    try:
        sc = _load("ora_synthetic_case", reference / "synthetic_case.py")
    finally:
        sys.path.pop(0)

    problems: list[str] = []
    if not (root / "scripts" / "validate_orbital_recovery_case.py").is_file():
        problems.append("private-case validator is missing")

    required_docs = [
        "EPISTEMIC_ASSURANCE.md",
        "EVIDENCE_QUORUM_PATTERN.md",
        "BLACK_SKY_EXERCISE_PATTERN.md",
        "FUTURE_ARCHITECTURE_BOUNDARIES.md",
        "RECOVERY_CHAIN.md",
        "REAL_CASE_PROTOCOL.md",
    ]
    for doc_name in required_docs:
        if not (profile / "docs" / doc_name).is_file():
            problems.append(f"required profile guidance missing: {doc_name}")

    schema_map = {}
    for path in sorted(schemas.glob("*.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
            schema_map[path.name] = schema
            profile_version = schema.get("properties", {}).get("profile_version", {}).get("const")
            if profile_version != EXPECTED_PROFILE_VERSION:
                problems.append(f"schema profile_version const drifted: {path.name}: {profile_version!r}")
            classes = schema.get("properties", {}).get("record_class", {}).get("enum", [])
            if "private" not in classes:
                problems.append(f"schema does not support partner-private records: {path.name}")
            if jsonschema is not None:
                jsonschema.validators.validator_for(schema).check_schema(schema)
        except (OSError, json.JSONDecodeError, SchemaError) as exc:
            problems.append(f"schema invalid: {path.name}: {exc}")

    records = {
        p.name: json.loads(p.read_text(encoding="utf-8"))
        for p in sorted(examples.glob("*.json"))
    }
    expected_schema = {
        "recovery-evidence-record.json": "recovery-evidence-record.schema.json",
        "post-recovery-evidence-record.json": "recovery-evidence-record.schema.json",
        "recovery-option-assessment.json": "recovery-option-assessment.schema.json",
        "recovery-chain-view.json": "recovery-chain-view.schema.json",
        "requalification-record.json": "requalification-record.schema.json",
        "recovery-timeline.json": "recovery-timeline.schema.json",
    }
    if jsonschema is not None:
        for filename, schema_name in expected_schema.items():
            try:
                validator_cls = jsonschema.validators.validator_for(schema_map[schema_name])
                validator = validator_cls(
                    schema_map[schema_name],
                    format_checker=jsonschema.FormatChecker(),
                )
                validator.validate(records[filename])
            except (SchemaError, ValidationError) as exc:
                problems.append(f"example/schema mismatch: {filename}: {exc}")

    for filename, record in records.items():
        if record.get("profile_version") != EXPECTED_PROFILE_VERSION:
            problems.append(f"example profile_version drifted: {filename}")

    evidence_records = [
        records["recovery-evidence-record.json"],
        records["post-recovery-evidence-record.json"],
    ]
    by_record_id = {r["record_id"]: r for r in evidence_records}
    all_evidence_ids = [
        item["id"]
        for record in evidence_records
        for item in record.get("evidence", [])
    ]
    if len(all_evidence_ids) != len(set(all_evidence_ids)):
        problems.append("evidence ids are not globally unique across the synthetic case")
    for record in evidence_records:
        problems.extend(ev.validate_evidence_record(record))

    components = ev.provenance_correlation_components(records["recovery-evidence-record.json"])
    if not any({"EVIDENCE-002", "EVIDENCE-003"}.issubset(set(group)) for group in components):
        problems.append("shared provenance root was not collapsed into a correlation component")

    expected_assessment = sc.assessment_json()
    if records["recovery-option-assessment.json"] != expected_assessment:
        problems.append("checked-in recovery-option-assessment.json drifted from reference policy")

    assessment = records["recovery-option-assessment.json"]
    chain_view = records["recovery-chain-view.json"]
    if chain_view["evidence_record_ref"] not in by_record_id:
        problems.append("recovery-chain view evidence_record_ref does not resolve")
    if chain_view["asset_id"] != assessment["asset_id"]:
        problems.append("recovery-chain view asset_id does not match option assessment")
    expected_stages = ["power", "contact", "telemetry", "command", "capability"]
    if set(chain_view.get("chain", {})) != set(expected_stages):
        problems.append("recovery-chain view must contain exactly the declared stages")
    chain_refs = []
    for stage in expected_stages:
        chain_refs.extend(chain_view["chain"][stage].get("evidence_refs", []))
    for row in chain_view.get("trust_overlay", {}).values():
        chain_refs.extend(row.get("evidence_refs", []))
    for row in chain_view.get("authority_overlay", {}).values():
        chain_refs.extend(row.get("evidence_refs", []))
    unresolved_chain_refs = ev.resolve_refs(chain_refs, evidence_records)
    if unresolved_chain_refs:
        problems.append(
            f"recovery-chain evidence refs do not resolve: {sorted(set(unresolved_chain_refs))}"
        )
    if "trust" in chain_view.get("chain", {}) or "authority" in chain_view.get("chain", {}):
        problems.append("trust and authority must remain overlays, not serial recovery-chain stages")

    option_names = {row["name"] for row in assessment["options"]}
    row_robust = {row["name"] for row in assessment["options"] if row.get("robust")}
    row_eligible = {row["name"] for row in assessment["options"] if row.get("eligible")}
    if row_robust != set(assessment["robust_options"]):
        problems.append("option-row robust flags do not match robust_options")
    if row_eligible != set(assessment["eligible_options"]):
        problems.append("option-row eligible flags do not match eligible_options")
    for row in assessment["options"]:
        if abs(
            (row["expected_utility"] - assessment["hold_utility"])
            - row["utility_advantage_vs_hold"]
        ) > 1e-9:
            problems.append(f"option utility advantage drifted: {row['name']}")
        if row["robust"] and row["unsafe_hypotheses"]:
            problems.append(f"robust option lists unsafe hypotheses: {row['name']}")
        if row["eligible"] and (not row["robust"] or row["gate_failures"]):
            problems.append(f"eligible option has unresolved blockers: {row['name']}")
    for key in ("robust_options", "eligible_options"):
        unknown = set(assessment[key]) - option_names
        if unknown:
            problems.append(f"{key} references unknown option(s): {sorted(unknown)}")
    if not set(assessment["eligible_options"]).issubset(set(assessment["robust_options"])):
        problems.append("eligible_options must be a subset of robust_options")
    highest = assessment.get("highest_ranked_eligible_option")
    if highest is not None and highest not in set(assessment["eligible_options"]):
        problems.append("highest_ranked_eligible_option must be eligible")
    candidate_names = {row["name"] for row in assessment.get("candidate_observations", [])}
    next_observation = assessment.get("next_best_observation")
    if next_observation is not None and next_observation not in candidate_names:
        problems.append("next_best_observation does not resolve")
    if next_observation is not None:
        row = next(
            row
            for row in assessment["candidate_observations"]
            if row["name"] == next_observation
        )
        if row["nevoi"] <= 0:
            problems.append("next_best_observation must have positive NEVOI")
    expected_disposition = (
        "ELIGIBLE_FOR_DECISION_PREPARATION"
        if assessment["eligible_options"]
        else "HOLD_FAIL_CLOSED"
    )
    if assessment["disposition"] != expected_disposition:
        problems.append("assessment disposition is inconsistent with eligible_options")
    if assessment["evidence_record_ref"] not in by_record_id:
        problems.append("option assessment evidence_record_ref does not resolve")

    rq = records["requalification-record.json"]
    rq_evidence = by_record_id.get(rq["evidence_record_ref"])
    if rq_evidence is None:
        problems.append("requalification evidence_record_ref does not resolve")
    else:
        refs = [ref for req in rq["requirements"] for ref in req["evidence_refs"]]
        unresolved = ev.resolve_refs(refs, [rq_evidence])
        if unresolved:
            problems.append(
                f"requalification evidence refs do not resolve: {sorted(set(unresolved))}"
            )
        states = [item["state"] for item in rq["requirements"]]
        expected_review = (
            "READY_FOR_HUMAN_REVIEW"
            if all(state in {"verified", "supported"} for state in states)
            else "HOLD_FAIL_CLOSED"
        )
        if rq["review_state"] != expected_review:
            problems.append("requalification review_state is inconsistent with requirement states")

    benchmark_dir = profile / "benchmark"
    protocol = json.loads((benchmark_dir / "protocol.json").read_text(encoding="utf-8"))
    checked_result = json.loads((benchmark_dir / "results.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(reference))
    try:
        sb = _load("ora_synthetic_benchmark", reference / "synthetic_benchmark.py")
    finally:
        sys.path.pop(0)
    regenerated = sb.run(protocol)
    if not _benchmark_equivalent(checked_result, regenerated):
        problems.append("checked-in synthetic benchmark results drifted beyond tolerance")
    if regenerated.get("status") != "PASS":
        problems.append("current synthetic benchmark protocol did not pass")
    if regenerated.get("policy", {}).get("unsafe_action_rate") != 0.0:
        problems.append("synthetic benchmark policy violated the declared safety invariant")
    stress_protocol = json.loads(
        (benchmark_dir / "stress-matrix.json").read_text(encoding="utf-8")
    )
    checked_stress = json.loads(
        (benchmark_dir / "stress-results.json").read_text(encoding="utf-8")
    )
    regenerated_stress = sb.run_stress_matrix(protocol, stress_protocol)
    if not _benchmark_equivalent(checked_stress, regenerated_stress):
        problems.append("checked-in stress benchmark results drifted beyond tolerance")
    if regenerated_stress.get("status") != "PASS":
        problems.append("synthetic stress benchmark did not pass")

    timeline = records["recovery-timeline.json"]
    if timeline["assessment_ref"] != assessment["assessment_id"]:
        problems.append("timeline assessment_ref does not resolve")
    metrics = tm.compute_timeline_metrics(timeline["events"])
    if metrics.get("TTT") != 1680.0 or metrics.get("TTV") != 2100.0:
        problems.append("timeline metric regression")

    for record in records.values():
        if record.get("record_class") != "synthetic":
            problems.append("public example is not synthetic")

    url_re = re.compile(r"https?://", re.IGNORECASE)
    email_re = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
    for path in sorted(profile.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".md", ".py", ".json", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        if url_re.search(text):
            problems.append(f"external URL not allowed in profile: {path.relative_to(root)}")
        if email_re.search(text):
            problems.append(f"email address not allowed in profile: {path.relative_to(root)}")

    if problems:
        print("ORBITAL RECOVERY ASSURANCE PROFILE FAIL")
        for problem in problems:
            print(f"FAIL: {problem}")
        return 2

    print("ORBITAL RECOVERY ASSURANCE PROFILE PASS")
    print(f"Provenance correlation components: {components}")
    print(f"Timeline metrics (seconds): {metrics}")
    if jsonschema is None:
        print("WARN: jsonschema unavailable; structural schema validation deferred to full repo dev gate")
    print(
        "NOTE: benchmark case generation and discrete results are deterministic; "
        f"aggregate float snapshots use {BENCHMARK_FLOAT_TOLERANCE:g} comparison tolerance."
    )
    print("NOTE: PASS is bounded to declared synthetic contracts and checks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
