from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

TEXT_SUFFIXES = {
    "", ".md", ".txt", ".py", ".toml", ".yaml", ".yml", ".json", ".cff",
    ".ini", ".cfg", ".sh", ".ps1", ".csv", ".sha256"
}
LOCAL_SKIP_DIRS = {".git", ".venv", "build", "dist", ".pytest_cache", ".ruff_cache", "__pycache__"}
FORBIDDEN_SUFFIXES = {
    ".pem", ".key", ".p12", ".pfx", ".kdbx",
    ".log", ".db", ".sqlite", ".sqlite3", ".ipynb",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".pdf",
    ".docx", ".xlsx", ".pptx", ".zip", ".7z", ".tar", ".gz",
}
ALLOWED_URL_PREFIXES = (
    "https://bridgenode7.com/",
    "https://www.bridgenode7.com/",
    "https://github.com/Bridge-Node-7/",
    "https://bridge-node-7.github.io/",
    "https://json-schema.org/",
)
PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
    "unix-home-path": re.compile(r"/(?:home|Users)/[^/\s]+/"),
    "windows-user-path": re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
    "private-key": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "github-token": re.compile(r"\b(?:ghp_|github_pat_)[A-Za-z0-9_\-]+\b"),
    "generic-secret-assignment": re.compile(
        r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"]?[^\s'\"]{8,}"
    ),
    "private-ipv4": re.compile(r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"),
}
URL_RE = re.compile(r"https?://[^\s)\]>\"']+")


def _git_tracked_files(root: Path) -> list[Path] | None:
    """Return every Git-tracked file, or None when root is not a Git worktree.

    Release eligibility is based on tracked content, not directory reputation. A file
    remains in scope even when it is force-added under build/, dist/, or a cache path.
    """
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"],
            check=False,
            capture_output=True,
        )
    except OSError:
        return None
    if completed.returncode != 0:
        return None
    paths: list[Path] = []
    for raw in completed.stdout.split(b"\0"):
        if not raw:
            continue
        rel = raw.decode("utf-8", errors="surrogateescape")
        path = root / rel
        if path.is_file():
            paths.append(path)
    return paths


def iter_files(root: Path):
    tracked = _git_tracked_files(root)
    if tracked is not None:
        yield from tracked
        return

    # Non-Git fallback supports bounded fixture/directory scans. Local ephemeral
    # directories may be skipped here because they cannot enter a Git release archive.
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if any(part in LOCAL_SKIP_DIRS for part in rel.parts):
            continue
        yield path


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    findings: list[str] = []
    warnings: list[str] = []

    for path in iter_files(root):
        rel = path.relative_to(root)
        if path.name == ".env" or path.name.startswith(".env.") or path.suffix.lower() in FORBIDDEN_SUFFIXES:
            findings.append(f"forbidden sensitive-looking file: {rel}")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES and path.name not in {"Makefile", "LICENSE", ".gitignore", ".editorconfig", ".python-version"}:
            warnings.append(f"manual review of non-text file: {rel}")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            warnings.append(f"manual review of undecodable file: {rel}")
            continue
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                findings.append(f"{label}: {rel}:{line}")
        for match in URL_RE.finditer(text):
            url = match.group(0)
            if not any(url.startswith(prefix) for prefix in ALLOWED_URL_PREFIXES):
                line = text.count("\n", 0, match.start()) + 1
                host = (urlparse(url).hostname or "").lower()
                findings.append(f"unapproved external URL: {rel}:{line} ({host})")

    if warnings:
        print("PUBLIC BOUNDARY WARNINGS")
        for item in sorted(set(warnings)):
            print(f"WARN: {item}")
    if findings:
        print("PUBLIC BOUNDARY FAIL")
        for item in sorted(set(findings)):
            print(f"FAIL: {item}")
        return 2
    print("PUBLIC BOUNDARY PASS: no automated high-risk disclosure patterns detected")
    print("NOTE: tracked release files are authoritative; manual review is still required for proper nouns, sensitive technical values, binaries, and context.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
