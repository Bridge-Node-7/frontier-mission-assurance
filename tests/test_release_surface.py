from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_structured_public_files_parse():
    for path in ROOT.rglob("*"):
        ignored = {".git", ".venv", "build", "dist"}
        if not path.is_file() or any(part in ignored for part in path.parts):
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
            target = raw_target.strip().split(maxsplit=1)[0].strip('<>"')
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
    assert version == "0.3.0"
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "0.3.0"' in pyproject
    assert 'license = "LicenseRef-Proprietary"' in pyproject
    assert 'license-files = ["LICENSE"]' in pyproject
    assert 'Private :: Do Not Upload' in pyproject
    init_text = (ROOT / "src" / "frontier_assurance" / "__init__.py").read_text(encoding="utf-8")
    assert '__version__ = "0.3.0"' in init_text
    assert json.loads((ROOT / "PROJECT_FACTS.json").read_text())["version"] == version
    assert yaml.safe_load((ROOT / "CITATION.cff").read_text())["version"] == version


def test_proprietary_candidate_does_not_claim_open_source():
    disclaimer = (ROOT / "DISCLAIMER.md").read_text(encoding="utf-8").lower()
    assert "open-source" not in disclaimer
    assert "open source" not in disclaimer


def test_release_evidence_lifecycle_is_non_recursive():
    receipt = (ROOT / "RELEASE_RECEIPT.md").read_text(encoding="utf-8")
    validation = (ROOT / "VALIDATION_REPORT.md").read_text(encoding="utf-8")
    checklist = (ROOT / "docs" / "RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
    lifecycle = (ROOT / "docs" / "RELEASE_EVIDENCE_LIFECYCLE.md").read_text(encoding="utf-8")
    assert "Commit-specific hosted evidence belongs in GitHub Actions" in receipt
    assert "not a live status board" in checklist
    assert "recursive" in lifecycle.lower()
    assert not re.search(r"\b[0-9a-f]{40}\b", receipt)
    assert not re.search(r"\b[0-9a-f]{40}\b", validation)


def test_scientific_discovery_profile_surface_is_present():
    required = [
        ROOT / "profiles" / "scientific-discovery" / "README.md",
        ROOT / "profiles" / "scientific-discovery" / "SPECIFICATION_EQUIVALENCE.md",
        ROOT / "profiles" / "scientific-discovery" / "ATTRIBUTION.md",
        ROOT / "profiles" / "scientific-discovery" / "LIMITATIONS.md",
        ROOT / "scripts" / "validate_scientific_discovery.py",
        ROOT / "tests" / "test_scientific_discovery.py",
    ]
    assert all(path.is_file() for path in required)
    assert len(list((ROOT / "profiles" / "scientific-discovery" / "schemas").glob("*.schema.json"))) == 6


def test_uat_identifiers_are_unique_and_sequential():
    text = (ROOT / "docs" / "UAT.md").read_text(encoding="utf-8")
    numbers = [int(value) for value in re.findall(r"^## UAT-(\d{2})\b", text, flags=re.MULTILINE)]
    assert numbers == list(range(1, len(numbers) + 1))


def test_issue_forms_do_not_depend_on_custom_labels():
    issue_dir = ROOT / ".github" / "ISSUE_TEMPLATE"
    forms = [issue_dir / "assumption-challenge.yml", issue_dir / "evidence-gap.yml", issue_dir / "experiment-result.yml", issue_dir / "bug-report.yml"]
    for path in forms:
        assert "labels" not in yaml.safe_load(path.read_text(encoding="utf-8"))
