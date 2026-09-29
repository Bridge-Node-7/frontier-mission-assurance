"""Native adversarial corpus for receipt_version 3.x surfaces.

Two deliberately separate suites:

* ``NEGATIVE_CORPUS`` — mutations that are invalid under the v3 contract.
  Expected behaviour is rejection.
* ``VISIBILITY_CORPUS`` — inputs that are *valid but weak*. A finite wide
  tolerance is a permitted declaration under the acceptance doctrine; it must
  pass, and the declared strength must be visible in the successful result.

Keeping these apart matters. Folding a weak-but-valid declaration into the
rejection corpus would make "everything rejects" the target metric, which
contradicts the doctrine that a receipt declares its own acceptance criterion.

Repository-relative throughout: no absolute paths, no virtualenv assumptions,
no subprocess invocation of an installed console script.
"""

from __future__ import annotations

import copy
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
import yaml

from frontier_assurance.receipt import verify_receipt

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_EXAMPLE_DIR = ROOT / "examples" / "research_receipt_v3_external"

Mutator = Callable[[dict], None]


def _staged(tmp_path: Path) -> Path:
    """Copy the shipped external example into a writable working directory."""
    work = tmp_path / "case"
    shutil.copytree(EXTERNAL_EXAMPLE_DIR, work)
    return work


def _apply(work: Path, mutate: Mutator) -> Path:
    receipt = work / "receipt.yaml"
    document = yaml.safe_load(receipt.read_text(encoding="utf-8"))
    mutate(document)
    receipt.write_text(yaml.safe_dump(document, sort_keys=False), encoding="utf-8")
    return receipt


def _instrument(document: dict) -> dict:
    return document["calibration"]["instruments"][0]


def _collection(document: dict) -> dict:
    return document["execution"]["collection_receipt"]


# --------------------------------------------------------------------------
# Negative corpus — every entry must be rejected
# --------------------------------------------------------------------------

NEGATIVE_CORPUS: list[tuple[str, Mutator]] = [
    # AC-20 output acceptance
    ("acceptance_block_removed", lambda d: d.pop("output_acceptance")),
    ("acceptance_mode_unknown", lambda d: d["output_acceptance"].update(mode="TRUST_ME")),
    ("exact_mode_without_reference_hash",
     lambda d: d["output_acceptance"].update(mode="EXACT_SHA256")),
    ("hybrid_mode_without_reference_hash",
     lambda d: d["output_acceptance"].update(mode="HYBRID")),
    ("checks_emptied", lambda d: d.update(checks=[])),
    ("semantic_check_id_dangling",
     lambda d: d["outputs"][0].update(semantic_check_ids=["CHK-GHOST"])),
    ("semantic_output_without_check_ids",
     lambda d: d["outputs"][0].pop("semantic_check_ids", None)),
    ("receipt_version_unsupported", lambda d: d.update(receipt_version="4.0")),
    # FMA-NUM-01 non-finite acceptance
    ("atol_infinite", lambda d: d["checks"][0].update(atol=float("inf"))),
    ("rtol_infinite", lambda d: d["checks"][0].update(rtol=float("inf"))),
    ("atol_nan", lambda d: d["checks"][0].update(atol=float("nan"))),
    ("rtol_nan", lambda d: d["checks"][0].update(rtol=float("nan"))),
    ("expected_infinite", lambda d: d["checks"][0].update(expected=float("inf"))),
    ("atol_negative", lambda d: d["checks"][0].update(atol=-1.0)),
    # AC-21 calibration and instrument state
    ("calibration_removed", lambda d: d.pop("calibration")),
    ("calibration_not_a_mapping", lambda d: d.update(calibration=["x"])),
    ("calibration_policy_unknown", lambda d: d["calibration"].update(policy="WHATEVER")),
    ("required_policy_without_instruments",
     lambda d: d["calibration"].update(instruments=[])),
    ("instruments_not_a_list", lambda d: d["calibration"].update(instruments={})),
    ("as_of_missing", lambda d: d["calibration"].pop("as_of")),
    ("as_of_not_rfc3339", lambda d: d["calibration"].update(as_of="last tuesday")),
    ("as_of_before_validity_window",
     lambda d: d["calibration"].update(as_of="2026-08-01T00:00:00Z")),
    ("as_of_after_validity_window",
     lambda d: d["calibration"].update(as_of="2027-06-01T00:00:00Z")),
    ("validity_window_inverted",
     lambda d: _instrument(d).update(valid_from="2026-12-01T00:00:00Z",
                                     valid_until="2026-01-01T00:00:00Z")),
    ("instrument_id_missing", lambda d: _instrument(d).pop("instrument_id")),
    ("instrument_id_duplicated",
     lambda d: d["calibration"]["instruments"].append(copy.deepcopy(_instrument(d)))),
    ("configuration_hash_malformed",
     lambda d: _instrument(d).update(configuration_sha256="not-a-hash")),
    ("lineage_ref_missing", lambda d: _instrument(d).pop("lineage_ref")),
    ("state_id_missing", lambda d: _instrument(d).pop("state_id")),
    ("observed_at_not_rfc3339", lambda d: _instrument(d).update(observed_at="yesterday")),
    # AC-22 external execution evidence
    ("collection_receipt_removed", lambda d: d["execution"].pop("collection_receipt")),
    ("submission_receipt_removed", lambda d: d["execution"].pop("submission_receipt")),
    ("job_ref_mismatch", lambda d: _collection(d).update(job_ref="OTHER-JOB")),
    ("terminal_state_cancelled", lambda d: _collection(d).update(terminal_state="CANCELLED")),
    ("terminal_state_unknown",
     lambda d: _collection(d).update(terminal_state="PROBABLY_FINE")),
    ("completed_at_moved_outside_calibration_window",
     lambda d: _collection(d).update(completed_at="2025-01-01T00:00:00Z")),
    ("collected_output_hash_forged",
     lambda d: _collection(d)["outputs"][0].update(sha256="0" * 64)),
    ("code_manifest_forged",
     lambda d: d["execution"]["submission_receipt"].update(code_manifest_sha256="f" * 64)),
    ("environment_hash_removed",
     lambda d: d["execution"]["submission_receipt"]["environment"].pop("environment_sha256")),
    ("external_evidence_retained_under_local_mode",
     lambda d: d["execution"].update(mode="LOCAL")),
    # Artifact integrity carried forward from v2
    ("code_path_traversal_orphans_entrypoint", lambda d: d["code"][0].update(path="../../../etc/passwd")),
    ("code_path_absolute_orphans_entrypoint", lambda d: d["code"][0].update(path="/etc/hostname")),
]



# Each mutation is bound to the diagnostic class it is meant to exercise.
# Without this, a case stays green when its intended control regresses, because
# some other overlapping control happens to reject the receipt. Deriving these
# from observed behaviour also caught three mutations whose names claimed a
# control they did not actually prove.
EXPECTED_DIAGNOSTIC: dict[str, str] = {
    "acceptance_block_removed": "output_acceptance must be a mapping",
    "acceptance_mode_unknown": "output_acceptance.mode must be one of",
    "exact_mode_without_reference_hash": "incompatible with output_acceptance.mode=EXACT",
    "hybrid_mode_without_reference_hash": "HYBRID requires at least one EXACT",
    "checks_emptied": "references unknown check CHK-VALUE",
    "semantic_check_id_dangling": "references unknown check CHK-GHOST",
    "semantic_output_without_check_ids": "semantic_check_ids must be a non-empty list",
    "receipt_version_unsupported": "receipt_version must be",
    "atol_infinite": "atol must be finite",
    "rtol_infinite": "rtol must be finite",
    "atol_nan": "atol must be finite",
    "rtol_nan": "rtol must be finite",
    "expected_infinite": "expected must be finite",
    "atol_negative": "atol/rtol must be non-negative",
    "calibration_removed": "calibration must be a mapping",
    "calibration_not_a_mapping": "calibration must be a mapping",
    "calibration_policy_unknown": "calibration.policy must be one of",
    "required_policy_without_instruments": "calibration evidence is missing",
    "instruments_not_a_list": "calibration.instruments must be a list",
    "as_of_missing": "calibration.as_of must be an RFC3339 timestamp",
    "as_of_not_rfc3339": "calibration.as_of must be an RFC3339 timestamp",
    "as_of_before_validity_window": "calibration outside declared validity window",
    "as_of_after_validity_window": "calibration outside declared validity window",
    "validity_window_inverted": "valid_from is after valid_until",
    "instrument_id_missing": "instrument_id is required",
    "instrument_id_duplicated": "instrument_id is duplicated",
    "configuration_hash_malformed": "configuration_sha256 must be sha256",
    "lineage_ref_missing": "lineage_ref is required",
    "state_id_missing": "state_id is required",
    "observed_at_not_rfc3339": "observed_at must be RFC3339",
    "collection_receipt_removed": "collection_receipt is required for EXTERNAL mode",
    "submission_receipt_removed": "submission_receipt is required for EXTERNAL mode",
    "job_ref_mismatch": "job_ref values must match",
    "terminal_state_cancelled": "external job did not succeed",
    "terminal_state_unknown": "terminal_state must be one of",
    "completed_at_moved_outside_calibration_window":
        "calibration does not cover declared execution interval",
    "collected_output_hash_forged": "external collection sha256 mismatch",
    "code_manifest_forged": "code_manifest_sha256 does not match declared code",
    "environment_hash_removed": "environment_sha256 must be sha256",
    "external_evidence_retained_under_local_mode": "LOCAL execution has unsupported fields",
    "code_path_traversal_orphans_entrypoint":
        "experiment.entrypoint must reference a declared code artifact",
    "code_path_absolute_orphans_entrypoint":
        "experiment.entrypoint must reference a declared code artifact",
}

@pytest.mark.parametrize("name,mutate", NEGATIVE_CORPUS, ids=[c[0] for c in NEGATIVE_CORPUS])
def test_invalid_v3_mutation_is_rejected(tmp_path: Path, name: str, mutate: Mutator):
    receipt = _apply(_staged(tmp_path), mutate)
    result = verify_receipt(receipt)
    assert not result.ok, f"{name} must be rejected"
    assert result.errors, f"{name} rejected without a diagnostic"

    expected = EXPECTED_DIAGNOSTIC[name]
    assert any(expected in error for error in result.errors), (
        f"{name} rejected, but not by its intended control. "
        f"Expected a diagnostic containing {expected!r}; got {result.errors}"
    )


def test_every_negative_case_is_bound_to_a_diagnostic():
    """A case added without a binding would silently become a smoke test."""
    unbound = [name for name, _ in NEGATIVE_CORPUS if name not in EXPECTED_DIAGNOSTIC]
    assert not unbound, f"negative corpus entries missing a diagnostic binding: {unbound}"


def test_shipped_external_example_is_accepted(tmp_path: Path):
    """Guards the corpus itself: if the baseline failed, every case above
    would 'reject' for the wrong reason and prove nothing."""
    work = _staged(tmp_path)
    result = verify_receipt(work / "receipt.yaml")
    assert result.ok, result.errors
    assert result.numerical_checks == 1


def test_tampering_with_declared_artifacts_is_rejected(tmp_path: Path):
    for artifact, payload in (("analysis.py", b"print('x')\n"),
                              ("data/input.txt", b"tampered\n")):
        work = _staged(tmp_path / artifact.replace("/", "_"))
        (work / artifact).write_bytes(payload)
        result = verify_receipt(work / "receipt.yaml")
        assert not result.ok, f"tampered {artifact} must be rejected"


# --------------------------------------------------------------------------
# Assurance-strength visibility corpus — valid, weak, and must be conspicuous
# --------------------------------------------------------------------------


def test_wide_finite_tolerance_is_accepted_but_visible(tmp_path: Path):
    """A finite wide tolerance is a permitted declaration, not a defect.

    The contract is that it passes and that its strength is legible in the
    successful result, so a reader can tell a 1e-12 criterion from a 1e9 one.
    """
    work = _staged(tmp_path)
    receipt = _apply(work, lambda d: d["checks"][0].update(atol=1e9))
    result = verify_receipt(receipt)

    assert result.ok, result.errors
    line = next(check for check in result.checks if check.startswith("numeric OK"))
    assert "atol=1000000000.0" in line
    assert "observed=" in line and "expected=" in line


def test_tight_and_wide_tolerances_are_distinguishable(tmp_path: Path):
    """The regression that would have caught the original opacity defect."""
    tight = verify_receipt(_staged(tmp_path / "tight") / "receipt.yaml")
    wide_dir = _staged(tmp_path / "wide")
    wide = verify_receipt(_apply(wide_dir, lambda d: d["checks"][0].update(atol=1e9)))

    assert tight.ok and wide.ok
    tight_line = next(c for c in tight.checks if c.startswith("numeric OK"))
    wide_line = next(c for c in wide.checks if c.startswith("numeric OK"))
    assert tight_line != wide_line, "weak and strong acceptance must not render identically"


def test_finite_tolerance_does_not_accept_an_out_of_bounds_result(tmp_path: Path):
    """A bounded tolerance must still reject a result outside it.

    Carried over from the external harness: the complement of the wide-tolerance
    visibility case. Together they prove tolerance is enforced, not decorative.
    """
    work = _staged(tmp_path)
    (work / "outputs" / "result.json").write_text('{"value": 99.0}\n', encoding="utf-8")
    result = verify_receipt(work / "receipt.yaml")
    assert not result.ok
    assert any("sha256 mismatch" in e or "!= expected" in e for e in result.errors)


def test_semantic_acceptance_does_not_waive_output_existence(tmp_path: Path):
    """SEMANTICALLY_CHECKED relaxes byte identity, not the artifact itself."""
    work = _staged(tmp_path)
    (work / "outputs" / "result.json").unlink()
    result = verify_receipt(work / "receipt.yaml")
    assert not result.ok
    assert any("missing artifact" in e or "missing result file" in e for e in result.errors)
