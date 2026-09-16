from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_orbital_profile_release_surface_is_present():
    required = [
        ROOT / "profiles" / "orbital-recovery-assurance" / "README.md",
        ROOT / "profiles" / "orbital-recovery-assurance" / "PROFILE_CONTRACT.md",
        ROOT / "profiles" / "orbital-recovery-assurance" / "ASSURANCE_SCOPE.md",
        ROOT / "scripts" / "validate_orbital_recovery_assurance.py",
        ROOT / "scripts" / "validate_orbital_recovery_case.py",
        ROOT / "scripts" / "run_orbital_recovery_synthetic_benchmark.py",
    ]
    assert all(path.is_file() for path in required)

    profile = ROOT / "profiles" / "orbital-recovery-assurance"
    assert len(list((profile / "schemas").glob("*.schema.json"))) == 5
    assert (profile / "examples" / "synthetic-recovery-case").is_dir()
    assert (profile / "benchmark" / "protocol.json").is_file()


def test_orbital_profile_is_source_distributed_not_core_package_data():
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'package-dir = {"" = "src"}' in pyproject
    assert 'where = ["src"]' in pyproject
    assert "profiles/orbital-recovery-assurance" not in pyproject
