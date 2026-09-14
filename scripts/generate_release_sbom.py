from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from email.parser import Parser
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def wheel_metadata(path: Path) -> tuple[str, str, list[str]]:
    with zipfile.ZipFile(path) as archive:
        metadata_names = [name for name in archive.namelist() if name.endswith(".dist-info/METADATA")]
        if len(metadata_names) != 1:
            raise ValueError("wheel must contain exactly one dist-info/METADATA file")
        text = archive.read(metadata_names[0]).decode("utf-8")
    parsed = Parser().parsestr(text)
    name = parsed.get("Name")
    version = parsed.get("Version")
    if not name or not version:
        raise ValueError("wheel metadata is missing Name or Version")
    requirements = parsed.get_all("Requires-Dist", [])
    return name, version, list(requirements)


def requirement_name(requirement: str) -> str:
    requirement_token = requirement.split(";", 1)[0].strip()
    for separator in (" ", "(", "<", ">", "=", "!", "~", "["):
        if separator in requirement_token:
            requirement_token = requirement_token.split(separator, 1)[0]
    return requirement_token.strip()


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: generate_release_sbom.py WHEEL OUT.json", file=sys.stderr)
        return 2
    wheel = Path(sys.argv[1])
    output = Path(sys.argv[2])
    name, version, requirements = wheel_metadata(wheel)
    root_ref = f"pkg:pypi/{name}@{version}"
    components = []
    dependency_refs = []
    for requirement in sorted(requirements):
        dep_name = requirement_name(requirement)
        if not dep_name:
            continue
        ref = f"pkg:pypi/{dep_name.lower().replace('_', '-')}"
        dependency_refs.append(ref)
        components.append(
            {
                "type": "library",
                "name": dep_name,
                "bom-ref": ref,
                "properties": [
                    {"name": "bn7:declared-requirement", "value": requirement}
                ],
            }
        )

    document = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.6",
        "version": 1,
        "metadata": {
            "component": {
                "type": "application",
                "name": name,
                "version": version,
                "bom-ref": root_ref,
                "purl": root_ref,
                "hashes": [
                    {"alg": "SHA-256", "content": sha256_file(wheel)}
                ],
                "properties": [
                    {
                        "name": "bn7:sbom-scope",
                        "value": "release artifact plus declared runtime dependencies",
                    }
                ],
            }
        },
        "components": components,
        "dependencies": [{"ref": root_ref, "dependsOn": dependency_refs}],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
