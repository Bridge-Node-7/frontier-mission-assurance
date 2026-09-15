from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    profile = root / "profiles" / "orbital-recovery-assurance"
    reference = profile / "reference"
    sys.path.insert(0, str(reference))
    try:
        benchmark = load("ora_synthetic_benchmark", reference / "synthetic_benchmark.py")
    finally:
        sys.path.pop(0)
    protocol_path = profile / "benchmark" / "protocol.json"
    result = benchmark.run_from_paths(protocol_path)
    stress_path = profile / "benchmark" / "stress-matrix.json"
    stress = json.loads(stress_path.read_text(encoding="utf-8"))
    stress_result = benchmark.run_stress_matrix(
        json.loads(protocol_path.read_text(encoding="utf-8")), stress
    )
    payload = {"primary": result, "stress": stress_result}
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" and stress_result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
