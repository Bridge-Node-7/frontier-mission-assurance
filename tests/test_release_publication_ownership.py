"""t91u: release-please must not create GitHub Releases; Stable Release is sole publisher."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RP = ROOT / ".github" / "workflows" / "release-please.yml"
STABLE = ROOT / ".github" / "workflows" / "release.yml"


class ReleasePublicationOwnershipTests(unittest.TestCase):
    def test_release_please_skips_github_release(self) -> None:
        text = RP.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"(?m)^\s*skip-github-release:\s*true\s*$",
            "release-please must set skip-github-release: true so it cannot "
            "preempt the Stable Release publisher with a lightweight assetless Release",
        )

    def test_stable_release_is_sole_github_release_creator(self) -> None:
        rp = RP.read_text(encoding="utf-8")
        stable = STABLE.read_text(encoding="utf-8")
        self.assertNotRegex(rp, r"gh\s+release\s+create")
        self.assertNotRegex(rp, r"/releases['\"]?\s*")
        self.assertTrue(
            ("gh api --method POST" in stable and "/releases" in stable)
            or "gh release create" in stable,
            "Stable Release workflow must create the GitHub Release",
        )
        self.assertIn("git/tags", stable)
        self.assertIn("dry_run", stable)

    def test_release_please_uses_default_token_only(self) -> None:
        """No PAT required for this ownership split; flag if a token input appears."""
        text = RP.read_text(encoding="utf-8")
        # Action may omit token (defaults to GITHUB_TOKEN). Disallow secret PATs.
        self.assertNotRegex(text, r"secrets\.[A-Z0-9_]*(TOKEN|PAT|APP)")


if __name__ == "__main__":
    unittest.main()
