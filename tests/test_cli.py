from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _run(*args: str):
    return subprocess.run(
        [sys.executable, "-m", "frontier_assurance.cli", *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_cli_version_matches_package():
    from frontier_assurance import __version__

    completed = _run("--version")
    assert completed.returncode == 0
    assert completed.stdout.strip() == f"fma {__version__}"


def test_cli_no_args_points_to_five_minute_evaluation():
    completed = _run()
    assert completed.returncode == 2
    assert "docs/FIVE_MINUTE_EVALUATION.md" in completed.stderr
    assert "Traceback" not in completed.stderr


def test_cli_subcommand_help_describes_positionals():
    completed = _run("validate", "--help")
    assert completed.returncode == 0
    assert "Path to an assurance-graph YAML/JSON file" in completed.stdout
    assert "Example:" in completed.stdout

    completed = _run("reproduce", "--help")
    assert completed.returncode == 0
    assert "Path to a local code-bound research receipt" in completed.stdout
    assert "Maximum command runtime" in completed.stdout


def test_cli_directory_input_fails_with_exit_2_without_traceback(tmp_path):
    completed = _run("receipt", str(tmp_path))
    assert completed.returncode == 2
    combined = completed.stdout + completed.stderr
    assert "FAIL:" in combined
    assert "Traceback" not in combined


def test_cli_malformed_yaml_fails_with_exit_2_without_traceback(tmp_path):
    malformed = Path(tmp_path) / "malformed.yaml"
    malformed.write_text("root: [unterminated\n", encoding="utf-8")
    completed = _run("receipt", str(malformed))
    assert completed.returncode == 2
    combined = completed.stdout + completed.stderr
    assert "FAIL:" in combined
    assert "Traceback" not in combined
    assert "\n  in " not in combined
