from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

SCHEMA_PATH = Path("schemas/profile-manifest.schema.json")
PROFILES_PATH = Path("profiles")
SEMVER = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def _load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError(f"{path}: document must be a mapping")
    return data


def _safe_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    candidate.relative_to(root.resolve())
    return candidate


def _semver_tuple(value: str) -> tuple[int, int, int]:
    match = SEMVER.fullmatch(value)
    if match is None:
        raise ValueError(f"invalid semantic version: {value}")
    return tuple(int(part) for part in match.groups())


def validate_profile_manifests(root: Path) -> list[str]:
    errors: list[str] = []
    schema_path = root / SCHEMA_PATH
    profiles_root = root / PROFILES_PATH

    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(schema)
    except Exception as exc:  # noqa: BLE001 - bounded validation surface
        return [f"schema: {exc}"]

    try:
        fma_version = (root / "VERSION").read_text(encoding="utf-8").strip()
        current_version = _semver_tuple(fma_version)
    except Exception as exc:  # noqa: BLE001 - bounded validation surface
        return [f"VERSION: {exc}"]

    profile_dirs = sorted(path for path in profiles_root.iterdir() if path.is_dir())
    if not profile_dirs:
        return ["profiles: no profile directories found"]

    ids_seen: set[str] = set()
    validator = Draft202012Validator(schema)

    for profile_dir in profile_dirs:
        manifest_path = profile_dir / "profile.yaml"
        if not manifest_path.is_file():
            errors.append(f"{profile_dir.name}: missing profile.yaml")
            continue

        try:
            manifest = _load_yaml(manifest_path)
        except Exception as exc:  # noqa: BLE001 - report bounded failures
            errors.append(f"{profile_dir.name}: {exc}")
            continue

        for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "<root>"
            errors.append(f"{profile_dir.name}:{location}: {error.message}")

        if errors and any(item.startswith(f"{profile_dir.name}:") for item in errors):
            continue

        profile_id = manifest["profile_id"]
        if profile_id != profile_dir.name:
            errors.append(
                f"{profile_dir.name}: profile_id must match directory name, got {profile_id!r}"
            )
        if profile_id in ids_seen:
            errors.append(f"{profile_dir.name}: duplicate profile_id {profile_id!r}")
        ids_seen.add(profile_id)

        try:
            introduced = _semver_tuple(manifest["introduced_in_fma_release"])
            if introduced > current_version:
                errors.append(
                    f"{profile_dir.name}: introduced_in_fma_release is newer than VERSION"
                )
        except ValueError as exc:
            errors.append(f"{profile_dir.name}: {exc}")

        try:
            contract_path = _safe_path(root, manifest["profile_contract"])
            contract_path.relative_to(profile_dir.resolve())
            if not contract_path.is_file():
                errors.append(f"{profile_dir.name}: profile_contract does not exist")
        except (ValueError, TypeError) as exc:
            errors.append(f"{profile_dir.name}: invalid profile_contract path: {exc}")

        try:
            validator_path = _safe_path(root, manifest["validator"])
            if not validator_path.is_file():
                errors.append(f"{profile_dir.name}: validator does not exist")
            elif validator_path.suffix != ".py":
                errors.append(f"{profile_dir.name}: validator must reference a Python file")
        except (ValueError, TypeError) as exc:
            errors.append(f"{profile_dir.name}: invalid validator path: {exc}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate_profile_manifests(root)
    if errors:
        print("PROFILE MANIFESTS FAIL")
        for error in errors:
            print(f"FAIL: {error}")
        return 2
    print("PROFILE MANIFESTS PASS")
    print("NOTE: PASS establishes manifest structure and referenced public files only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
