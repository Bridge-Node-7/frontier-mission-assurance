from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_structured_public_files_parse():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in {".git", ".venv", "build", "dist"} for part in path.parts):
            continue
        if path.suffix.lower() == ".json":
            json.loads(path.read_text(encoding="utf-8"))
        elif path.suffix.lower() in {".yaml", ".yml", ".cff"}:
            yaml.safe_load(path.read_text(encoding="utf-8"))


def test_local_markdown_links_resolve():
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    missing: list[str] = []
    for path in ROOT.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw_target in pattern.findall(text):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>\"")
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            candidate = (path.parent / file_part).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                missing.append(f"{path.relative_to(ROOT)} -> {target} (escapes root)")
                continue
            if not candidate.exists():
                missing.append(f"{path.relative_to(ROOT)} -> {target}")
    assert not missing, "\n".join(missing)


def test_github_actions_are_immutably_pinned():
    workflows = list((ROOT / ".github" / "workflows").glob("*.yml")) + list(
        (ROOT / ".github" / "workflows").glob("*.yaml")
    )
    assert workflows
    floating: list[str] = []
    uses_seen = 0
    for path in workflows:
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "uses:" not in line:
                continue
            uses_seen += 1
            value = line.split("uses:", 1)[1].strip().split()[0]
            ref = value.rsplit("@", 1)[-1] if "@" in value else ""
            if not re.fullmatch(r"[0-9a-f]{40}", ref):
                floating.append(f"{path.relative_to(ROOT)}:{lineno}: {value}")
    assert uses_seen > 0
    assert not floating, "\n".join(floating)


def test_release_identity_is_consistent():
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    assert version == "0.2.0-rc8"

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.2.0rc8"' in pyproject
    assert 'license = "LicenseRef-Proprietary"' in pyproject
    assert 'license-files = ["LICENSE"]' in pyproject
    assert 'Private :: Do Not Upload' in pyproject

    init_text = (ROOT / "src" / "frontier_assurance" / "__init__.py").read_text(encoding="utf-8")
    assert '__version__ = "0.2.0rc8"' in init_text

    facts = json.loads((ROOT / "PROJECT_FACTS.json").read_text(encoding="utf-8"))
    assert facts["version"] == version

    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    assert citation["version"] == version


def test_proprietary_candidate_does_not_claim_open_source():
    disclaimer = (ROOT / "DISCLAIMER.md").read_text(encoding="utf-8").lower()
    assert "open-source" not in disclaimer
    assert "open source" not in disclaimer
