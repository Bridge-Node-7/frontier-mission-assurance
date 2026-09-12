from __future__ import annotations

import subprocess
import sys


def test_cli_version_matches_package():
    from frontier_assurance import __version__

    completed = subprocess.run(
        [sys.executable, "-m", "frontier_assurance.cli", "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == f"fma {__version__}"
