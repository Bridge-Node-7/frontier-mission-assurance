import shutil
from pathlib import Path

from frontier_assurance.receipt import verify_receipt

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "examples" / "research_receipt" / "receipt.yaml"


def test_reference_receipt_passes():
    result = verify_receipt(RECEIPT)
    assert result.ok, result.errors


def test_tampered_output_fails(tmp_path):
    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    output = dst / "outputs" / "result.json"
    output.write_text('{"estimate_z": 0.0, "n": 10}\n', encoding="utf-8")
    result = verify_receipt(dst / "receipt.yaml")
    assert not result.ok
    assert any("sha256 mismatch" in error for error in result.errors)



def test_path_escape_fails(tmp_path):
    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    receipt = (dst / "receipt.yaml").read_text(encoding="utf-8")
    receipt = receipt.replace("data/measurements.csv", "../outside.csv")
    (tmp_path / "outside.csv").write_text("secret\n", encoding="utf-8")
    (dst / "receipt.yaml").write_text(receipt, encoding="utf-8")
    result = verify_receipt(dst / "receipt.yaml")
    assert not result.ok
    assert any("path escapes receipt directory" in error for error in result.errors)


def test_numeric_regression_fails_even_with_updated_hash(tmp_path):
    from frontier_assurance.receipt import sha256_file

    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    output = dst / "outputs" / "result.json"
    output.write_text('{"estimate_z": 0.0, "n": 10}\n', encoding="utf-8")
    receipt_path = dst / "receipt.yaml"
    receipt = receipt_path.read_text(encoding="utf-8")
    old_hash = sha256_file(src / "outputs" / "result.json")
    receipt = receipt.replace(old_hash, sha256_file(output))
    receipt_path.write_text(receipt, encoding="utf-8")
    result = verify_receipt(receipt_path)
    assert not result.ok
    assert any("observed 0.0" in error for error in result.errors)


def test_check_path_escape_fails(tmp_path):
    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    receipt_path = dst / "receipt.yaml"
    receipt = receipt_path.read_text(encoding="utf-8")
    receipt = receipt.replace("path: outputs/result.json", "path: ../outside.json")
    (tmp_path / "outside.json").write_text('{"estimate_z": 0.6}\n', encoding="utf-8")
    receipt_path.write_text(receipt, encoding="utf-8")
    result = verify_receipt(receipt_path)
    assert not result.ok
    assert any("path escapes receipt directory" in error for error in result.errors)


def test_reproduce_regenerates_expected_output(tmp_path):
    from frontier_assurance.receipt import reproduce_receipt

    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    output = dst / "outputs" / "result.json"
    output.write_text('{"estimate_z": 0.0, "n": 10}\n', encoding="utf-8")
    result = reproduce_receipt(dst / "receipt.yaml", timeout=30)
    assert result.ok, result.errors
    assert "command exit OK" in "\n".join(result.checks)


def test_malformed_artifact_entry_fails_cleanly(tmp_path):
    src = RECEIPT.parent
    dst = tmp_path / "receipt-demo"
    shutil.copytree(src, dst)
    receipt_path = dst / "receipt.yaml"
    text = receipt_path.read_text(encoding="utf-8")
    text = text.replace(
        "inputs:\n  - path: data/measurements.csv\n    sha256: afac4acef548f23e1787a9bb70b3455284ddbd961e985e48b9f17a828f8a3f56",
        "inputs:\n  - not-a-mapping",
    )
    receipt_path.write_text(text, encoding="utf-8")
    result = verify_receipt(receipt_path)
    assert not result.ok
    assert any("artifact entry must be a mapping" in error for error in result.errors)
