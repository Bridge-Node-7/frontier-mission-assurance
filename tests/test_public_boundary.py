from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "public_boundary_scan.py"


def _scan(path: Path):
    return subprocess.run(
        [sys.executable, str(SCANNER), str(path)],
        capture_output=True,
        text=True,
        check=False,
    )


def _git_init(path: Path) -> None:
    subprocess.run(["git", "init", "-q", str(path)], check=True)


def _synthetic_secret_assignment() -> str:
    # Construct the adversarial fixture at runtime so the tracked test source itself
    # does not contain a secret-assignment pattern that the repository boundary scan
    # is intentionally required to reject.
    return "tok" + "en=synthetic_secret_value_for_boundary_test"


def test_public_boundary_scanner_rejects_unapproved_external_url(tmp_path):
    (tmp_path / "README.md").write_text("https://" + "example.invalid/private", encoding="utf-8")
    result = _scan(tmp_path)
    assert result.returncode == 2
    assert "unapproved external URL" in result.stdout


def test_public_boundary_scanner_rejects_risky_binary_extension(tmp_path):
    (tmp_path / "screenshot.png").write_bytes(b"not-a-real-image")
    result = _scan(tmp_path)
    assert result.returncode == 2
    assert "forbidden sensitive-looking file" in result.stdout


def test_public_boundary_scans_force_tracked_file_inside_ephemeral_directory(tmp_path):
    _git_init(tmp_path)
    hidden = tmp_path / "build" / "private-note.txt"
    hidden.parent.mkdir()
    hidden.write_text(_synthetic_secret_assignment(), encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "-f", "build/private-note.txt"], check=True)

    result = _scan(tmp_path)
    assert result.returncode == 2
    assert "generic-secret-assignment" in result.stdout
    assert "build/private-note.txt" in result.stdout.replace("\\", "/")


def test_public_boundary_ignores_untracked_ephemeral_cache_in_git_worktree(tmp_path):
    _git_init(tmp_path)
    readme = tmp_path / "README.md"
    readme.write_text("public fixture\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(tmp_path), "add", "README.md"], check=True)
    cache = tmp_path / ".pytest_cache" / "private-note.txt"
    cache.parent.mkdir()
    cache.write_text(_synthetic_secret_assignment(), encoding="utf-8")

    result = _scan(tmp_path)
    assert result.returncode == 0
    assert "PUBLIC BOUNDARY PASS" in result.stdout
