from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("aws-access-key-id", re.compile(r"AKIA[0-9A-Z]{16}")),
    ("github-pat", re.compile(r"ghp_[A-Za-z0-9]{36}")),
    ("github-fine-grained-pat", re.compile(r"github_pat_[A-Za-z0-9_]{20,}")),
    ("private-key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
)

ALLOWLIST_PREFIXES = ("tests/ci/fixtures/secrets/",)


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    line: int
    kind: str
    where: str


def _allowed(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(
        normalized == prefix[:-1] or normalized.startswith(prefix) for prefix in ALLOWLIST_PREFIXES
    )


def _scan_text(path: str, text: str, where: str) -> list[Finding]:
    findings: list[Finding] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                findings.append(Finding(path, line_number, kind, where))
    return findings


def scan_tree(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root).as_posix()
        if _allowed(relative):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(_scan_text(relative, text, "workdir"))
    return findings


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _scan_git_paths(root: Path, *ls_files_args: str, where: str) -> list[Finding]:
    result = _git(root, "ls-files", "-z", *ls_files_args)
    if result.returncode != 0:
        return [
            Finding(
                str(root),
                0,
                "git",
                f"git ls-files failed: {result.stderr.strip() or result.stdout.strip()}",
            )
        ]
    findings: list[Finding] = []
    for raw in result.stdout.split("\0"):
        if not raw or _allowed(raw):
            continue
        path = root / raw
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        findings.extend(_scan_text(raw, text, where))
    return findings


def scan_tracked(root: Path) -> list[Finding]:
    tracked = _scan_git_paths(root, where="tracked")
    untracked = _scan_git_paths(root, "--others", "--exclude-standard", where="untracked")
    if any(item.kind == "git" for item in tracked):
        return tracked
    return tracked + untracked


def scan_history(root: Path) -> list[Finding]:
    commits_result = _git(root, "rev-list", "--all")
    if commits_result.returncode != 0:
        return [
            Finding(
                str(root),
                0,
                "git-history",
                f"git rev-list failed: {commits_result.stderr.strip()}",
            )
        ]

    combined = "|".join(f"({pattern.pattern})" for _, pattern in PATTERNS)
    findings: list[Finding] = []
    for commit in commits_result.stdout.splitlines():
        result = _git(
            root,
            "grep",
            "-I",
            "-n",
            "-E",
            combined,
            commit,
            "--",
            ".",
            ":(exclude)tests/ci/fixtures/secrets/**",
        )
        if result.returncode not in {0, 1}:
            findings.append(
                Finding(
                    commit,
                    0,
                    "git-history",
                    f"git grep failed: {result.stderr.strip()}",
                )
            )
            continue
        for match in result.stdout.splitlines():
            path_and_line, _, text = match.partition(":")
            path, _, line_text = text.partition(":")
            if not path or not line_text:
                continue
            for kind, pattern in PATTERNS:
                if pattern.search(line_text):
                    findings.append(
                        Finding(
                            path,
                            int(path_and_line.rsplit(":", 1)[-1]) if ":" in path_and_line else 0,
                            kind,
                            f"commit {commit}",
                        )
                    )
    return findings


def scan(root: Path, include_history: bool) -> list[Finding]:
    findings = scan_tracked(root)
    if include_history:
        findings.extend(scan_history(root))
    return sorted(set(findings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scan the repository tree and git history for credential values."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: inferred from tools/)",
    )
    parser.add_argument(
        "--no-history",
        action="store_true",
        help="Skip git history scan (used by fixture harnesses).",
    )
    parser.add_argument(
        "--tree-only",
        action="store_true",
        help="Scan files under --root without git ls-files (fixture mode).",
    )
    args = parser.parse_args(argv)
    root = args.root.resolve()

    if args.tree_only:
        findings = scan_tree(root)
    else:
        findings = scan(root, include_history=not args.no_history)

    if not findings:
        print("secret/history scan: OK")
        return 0
    for finding in findings:
        location = f"{finding.path}:{finding.line}" if finding.line else finding.path
        print(f"{location}: {finding.kind}: {finding.where}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
