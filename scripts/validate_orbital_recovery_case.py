"""Validate a partner-controlled Orbital Recovery Assurance case locally.

This validator is deliberately structural. It reads local JSON files, applies the
public profile schemas, and checks bounded cross-record references. It performs no
network calls and establishes no real-world truth, safety, authority, ownership,
recoverability, probability calibration, or authorization.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:  # fail closed for real-case structural validation
    jsonschema = None

EXPECTED_PROFILE_VERSION = "0.5"
SCHEMA_FOR = {
    "recovery-evidence-record.json": "recovery-evidence-record.schema.json",
    "post-recovery-evidence-record.json": "recovery-evidence-record.schema.json",
    "recovery-option-assessment.json": "recovery-option-assessment.schema.json",
    "recovery-chain-view.json": "recovery-chain-view.schema.json",
    "requalification-record.json": "requalification-record.schema.json",
    "recovery-timeline.json": "recovery-timeline.schema.json",
}
REQUIRED = {"recovery-evidence-record.json", "recovery-chain-view.json"}
STAGE_REQUIREMENTS = {
    "mapped": set(),
    "assessed": {"recovery-option-assessment.json"},
    "post-intervention": {"recovery-option-assessment.json", "post-recovery-evidence-record.json"},
    "requalification-review": {
        "recovery-option-assessment.json",
        "post-recovery-evidence-record.json",
        "requalification-record.json",
    },
}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def validate_case(case_dir: Path, repo_root: Path, required_stage: str = "mapped") -> list[str]:
    problems: list[str] = []
    if jsonschema is None:
        return ["jsonschema is required for private-case validation"]
    if not case_dir.is_dir():
        return [f"case directory does not exist: {case_dir}"]

    profile = repo_root / "profiles" / "orbital-recovery-assurance"
    schemas_dir = profile / "schemas"
    reference = profile / "reference"
    ev = _load("ora_private_case_evidence_validation", reference / "evidence_validation.py")
    tm = _load("ora_private_case_timeline_metrics", reference / "timeline_metrics.py")

    if required_stage not in STAGE_REQUIREMENTS:
        return [f"unknown required stage: {required_stage}"]

    present = {p.name: p for p in case_dir.glob("*.json") if p.is_file()}
    missing = REQUIRED - set(present)
    if missing:
        problems.append(f"missing required case file(s): {sorted(missing)}")
    stage_missing = STAGE_REQUIREMENTS[required_stage] - set(present)
    if stage_missing:
        problems.append(
            f"required stage '{required_stage}' is incomplete; missing: {sorted(stage_missing)}"
        )

    unknown = set(present) - set(SCHEMA_FOR)
    if unknown:
        problems.append(f"unrecognized case JSON file(s): {sorted(unknown)}")

    records: dict[str, dict] = {}
    classes: set[str] = set()
    for filename, path in sorted(present.items()):
        if filename not in SCHEMA_FOR:
            continue
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
            records[filename] = record
        except Exception as exc:
            problems.append(f"invalid JSON: {filename}: {exc}")
            continue
        if record.get("profile_version") != EXPECTED_PROFILE_VERSION:
            problems.append(
                f"{filename}: profile_version must be {EXPECTED_PROFILE_VERSION!r}"
            )
        record_class = record.get("record_class")
        if record_class:
            classes.add(record_class)
        schema = json.loads((schemas_dir / SCHEMA_FOR[filename]).read_text(encoding="utf-8"))
        try:
            validator_cls = jsonschema.validators.validator_for(schema)
            validator = validator_cls(schema, format_checker=jsonschema.FormatChecker())
            validator.validate(record)
        except Exception as exc:
            problems.append(f"schema validation failed: {filename}: {exc}")

    if len(classes) > 1:
        problems.append(f"case record_class values must be consistent: {sorted(classes)}")
    if classes and classes != {"private"}:
        problems.append(
            "real-case validator expects record_class 'private'; use the public profile "
            "validator for checked-in synthetic examples"
        )

    evidence_records = [
        r for name, r in records.items()
        if name in {"recovery-evidence-record.json", "post-recovery-evidence-record.json"}
    ]
    by_record_id = {r.get("record_id"): r for r in evidence_records if r.get("record_id")}
    evidence_ids = [
        item.get("id")
        for record in evidence_records
        for item in record.get("evidence", [])
        if item.get("id")
    ]
    if len(evidence_ids) != len(set(evidence_ids)):
        problems.append("evidence ids must be globally unique within the case")
    for record in evidence_records:
        problems.extend(ev.validate_evidence_record(record))

    assessment = records.get("recovery-option-assessment.json")
    chain = records.get("recovery-chain-view.json")
    if chain:
        if chain.get("evidence_record_ref") not in by_record_id:
            problems.append("recovery-chain evidence_record_ref does not resolve")
        if assessment and chain.get("asset_id") != assessment.get("asset_id"):
            problems.append("recovery-chain asset_id does not match option assessment")
        stages = ["power", "contact", "telemetry", "command", "capability"]
        chain_keys = set(chain.get("chain", {}))
        if chain_keys != set(stages):
            problems.append("recovery-chain stages must be exactly power/contact/telemetry/command/capability")
        if "trust" in chain.get("chain", {}) or "authority" in chain.get("chain", {}):
            problems.append("trust and authority must remain overlays, not serial chain stages")
        refs: list[str] = []
        for stage in stages:
            refs.extend(chain.get("chain", {}).get(stage, {}).get("evidence_refs", []))
        for row in chain.get("trust_overlay", {}).values():
            refs.extend(row.get("evidence_refs", []))
        for row in chain.get("authority_overlay", {}).values():
            refs.extend(row.get("evidence_refs", []))
        unresolved = ev.resolve_refs(refs, evidence_records)
        if unresolved:
            problems.append(f"recovery-chain evidence refs do not resolve: {sorted(set(unresolved))}")

    if assessment:
        if assessment.get("evidence_record_ref") not in by_record_id:
            problems.append("option-assessment evidence_record_ref does not resolve")
        option_rows = assessment.get("options", [])
        option_names = {row.get("name") for row in option_rows}
        row_robust = {row.get("name") for row in option_rows if row.get("robust")}
        row_eligible = {row.get("name") for row in option_rows if row.get("eligible")}
        if row_robust != set(assessment.get("robust_options", [])):
            problems.append("option-row robust flags do not match robust_options")
        if row_eligible != set(assessment.get("eligible_options", [])):
            problems.append("option-row eligible flags do not match eligible_options")
        for row in option_rows:
            expected_advantage = row.get("expected_utility", 0) - assessment.get("hold_utility", 0)
            if abs(expected_advantage - row.get("utility_advantage_vs_hold", 0)) > 1e-9:
                problems.append(f"option utility advantage drifted: {row.get('name')}")
            if row.get("robust") and row.get("unsafe_hypotheses"):
                problems.append(f"robust option lists unsafe hypotheses: {row.get('name')}")
            if row.get("eligible") and (not row.get("robust") or row.get("gate_failures")):
                problems.append(f"eligible option has unresolved blockers: {row.get('name')}")
        if not set(assessment.get("eligible_options", [])).issubset(
            set(assessment.get("robust_options", []))
        ):
            problems.append("eligible_options must be a subset of robust_options")
        if set(assessment.get("robust_options", [])) - option_names:
            problems.append("robust_options contains an unknown option")
        if set(assessment.get("eligible_options", [])) - option_names:
            problems.append("eligible_options contains an unknown option")
        highest = assessment.get("highest_ranked_eligible_option")
        if highest is not None and highest not in assessment.get("eligible_options", []):
            problems.append("highest_ranked_eligible_option must be eligible")
        expected = (
            "ELIGIBLE_FOR_DECISION_PREPARATION"
            if assessment.get("eligible_options") else "HOLD_FAIL_CLOSED"
        )
        if assessment.get("disposition") != expected:
            problems.append("assessment disposition is inconsistent with eligible_options")

    rq = records.get("requalification-record.json")
    if rq:
        evidence_record = by_record_id.get(rq.get("evidence_record_ref"))
        if evidence_record is None:
            problems.append("requalification evidence_record_ref does not resolve")
        else:
            refs = [ref for req in rq.get("requirements", []) for ref in req.get("evidence_refs", [])]
            unresolved = ev.resolve_refs(refs, [evidence_record])
            if unresolved:
                problems.append(f"requalification evidence refs do not resolve: {sorted(set(unresolved))}")
        states = [row.get("state") for row in rq.get("requirements", [])]
        expected = (
            "READY_FOR_HUMAN_REVIEW"
            if states and all(s in {"verified", "supported"} for s in states)
            else "HOLD_FAIL_CLOSED"
        )
        if rq.get("review_state") != expected:
            problems.append("requalification review_state is inconsistent with requirement states")

    timeline = records.get("recovery-timeline.json")
    if timeline:
        if not assessment:
            problems.append("recovery timeline requires recovery-option-assessment.json")
        elif timeline.get("assessment_ref") != assessment.get("assessment_id"):
            problems.append("timeline assessment_ref does not resolve")
        try:
            tm.compute_timeline_metrics(timeline.get("events", {}))
        except Exception as exc:
            problems.append(f"timeline invalid: {exc}")

    return problems


def lifecycle_coverage(case_dir: Path) -> str:
    names = {p.name for p in case_dir.glob("*.json") if p.is_file()}
    if "requalification-record.json" in names:
        return "requalification-review"
    if "post-recovery-evidence-record.json" in names:
        return "post-intervention"
    if "recovery-option-assessment.json" in names:
        return "assessed"
    return "mapped"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("--quiet", action="store_true", help="suppress local identifiers in failure output")
    parser.add_argument(
        "--require-stage",
        choices=tuple(STAGE_REQUIREMENTS),
        default="mapped",
        help="minimum lifecycle artifact set required for this validation",
    )
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    case_dir = args.case_dir.resolve()
    problems = validate_case(case_dir, repo_root, required_stage=args.require_stage)
    if problems:
        print("ORBITAL RECOVERY PRIVATE CASE FAIL")
        if not args.quiet:
            for problem in problems:
                print(f"FAIL: {problem}")
        return 2
    print("ORBITAL RECOVERY PRIVATE CASE PASS")
    print(f"Lifecycle coverage: {lifecycle_coverage(case_dir)}; required: {args.require_stage}")
    print("NOTE: PASS is structural/cross-reference validation only; no real-world truth or authorization claim is made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
