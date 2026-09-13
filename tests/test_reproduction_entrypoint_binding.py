from __future__ import annotations

import hashlib
from pathlib import Path

import pytest
import yaml

from frontier_assurance.receipt import reproduce_receipt


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _write_receipt(tmp_path: Path, command: str) -> Path:
    code_bytes = (
        b"from pathlib import Path\n"
        b"import json\n"
        b"Path('outputs').mkdir(exist_ok=True)\n"
        b"Path('outputs/result.json').write_text(json.dumps({'value': 1.0}) + '\\n', encoding='utf-8')\n"
    )
    input_bytes = b"declared input\n"
    output_bytes = b'{"value": 1.0}\n'

    (tmp_path / "analysis.py").write_bytes(code_bytes)
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "input.txt").write_bytes(input_bytes)

    receipt = {
        "receipt_version": "2.0",
        "experiment": {
            "id": "ENTRYPOINT-BINDING",
            "command": command,
            "entrypoint": "analysis.py",
        },
        "code": [{"path": "analysis.py", "sha256": _sha256(code_bytes)}],
        "inputs": [{"path": "data/input.txt", "sha256": _sha256(input_bytes)}],
        "outputs": [{"path": "outputs/result.json", "sha256": _sha256(output_bytes)}],
        "checks": [
            {
                "name": "value",
                "path": "outputs/result.json",
                "json_path": "value",
                "expected": 1.0,
                "atol": 0.0,
                "rtol": 0.0,
            }
        ],
    }
    path = tmp_path / "receipt.yaml"
    path.write_text(yaml.safe_dump(receipt, sort_keys=False), encoding="utf-8")
    return path


def test_python_entrypoint_as_first_script_argument_reproduces(tmp_path: Path):
    result = reproduce_receipt(_write_receipt(tmp_path, "python analysis.py"))
    assert result.ok, result.errors
    assert result.numerical_checks == 1


@pytest.mark.parametrize(
    "command",
    [
        'python -c "print(1)" analysis.py',
        "python -m analysis analysis.py",
        "python - analysis.py",
        "python -I analysis.py",
        'python -c "open(\'BYPASS\', \'w\').write(\'x\')" analysis.py',
    ],
)
def test_interpreter_modes_and_decoy_entrypoint_tokens_fail_closed(
    tmp_path: Path, command: str
):
    result = reproduce_receipt(_write_receipt(tmp_path, command))
    assert not result.ok
    assert any("first Python script argument" in error for error in result.errors)
