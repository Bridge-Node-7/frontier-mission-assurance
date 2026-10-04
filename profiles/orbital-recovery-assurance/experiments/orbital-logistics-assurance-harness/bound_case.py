"""Bind cross-system service assurance to a governed Orbital Recovery case.

This local-only helper validates the existing private Orbital Recovery case first,
then projects the minimum governed records into the experimental service-assurance
harness. It performs no network calls and creates no operational authority.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case_dir", type=Path)
    parser.add_argument("service_case", type=Path)
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="suppress governed-case details in structural-validation failures",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[4]
    validator = _load_module(
        "ora_bound_case_validator",
        repo_root / "scripts" / "validate_orbital_recovery_case.py",
    )
    harness = _load_module(
        "ora_service_assurance_harness",
        Path(__file__).resolve().with_name("assurance_harness.py"),
    )

    try:
        service_case = _read_json(args.service_case.resolve())
    except (OSError, json.JSONDecodeError):
        print("invalid service-assurance case input", file=sys.stderr)
        return 2

    phase = service_case.get("phase")
    required_stage = {
        "pre_service": "assessed",
        "post_service": "post-intervention",
        "requalification_review": "requalification-review",
    }.get(phase, "mapped")

    case_dir = args.case_dir.resolve()
    problems = validator.validate_case(
        case_dir,
        repo_root,
        required_stage=required_stage,
    )
    if problems:
        print("CROSS-SYSTEM SERVICE CASE FAIL")
        if not args.quiet:
            for problem in problems:
                print(f"FAIL: {problem}")
        return 2

    if service_case.get("record_class") != "private":
        print("governed binding requires record_class 'private'", file=sys.stderr)
        return 2

    try:
        evidence_record = _read_json(case_dir / "recovery-evidence-record.json")
        option_assessment = _read_json(case_dir / "recovery-option-assessment.json")
        post_evidence_record = (
            _read_json(case_dir / "post-recovery-evidence-record.json")
            if (case_dir / "post-recovery-evidence-record.json").is_file()
            else None
        )
        requalification_record = (
            _read_json(case_dir / "requalification-record.json")
            if (case_dir / "requalification-record.json").is_file()
            else None
        )
    except (OSError, json.JSONDecodeError):
        print("invalid governed Orbital Recovery case input", file=sys.stderr)
        return 2

    result = harness.evaluate_bound_case(
        service_case,
        evidence_record,
        option_assessment,
        post_evidence_record=post_evidence_record,
        requalification_record=requalification_record,
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["disposition"] != harness.HOLD else 3


if __name__ == "__main__":
    raise SystemExit(main())
