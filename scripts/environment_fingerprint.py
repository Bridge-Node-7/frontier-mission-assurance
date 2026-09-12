from __future__ import annotations

import argparse
import importlib.metadata
import json
import platform
from pathlib import Path

PACKAGES = ("PyYAML", "pytest", "ruff", "jsonschema", "setuptools", "wheel", "build")


def package_version(name: str) -> str | None:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return None


def fingerprint() -> dict[str, object]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "system": platform.system(),
        "machine": platform.machine(),
        "packages": {name: package_version(name) for name in PACKAGES},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a public-safe environment fingerprint")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(fingerprint(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"WROTE: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
