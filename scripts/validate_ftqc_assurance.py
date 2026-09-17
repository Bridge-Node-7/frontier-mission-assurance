"""Validate the bounded FTQC Assurance profile."""

from __future__ import annotations

import sys
from pathlib import Path

from evaluate_ftqc_reference import validate_profile


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    problems = validate_profile(root)
    if problems:
        print("FTQC ASSURANCE PROFILE FAIL")
        for problem in problems:
            print(f"FAIL: {problem}")
        return 2

    print("FTQC ASSURANCE PROFILE PASS")
    print("NOTE: PASS is bounded to declared synthetic contracts and checks.")
    print("NOTE: quantum performance and consequential decision authority remain external.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
