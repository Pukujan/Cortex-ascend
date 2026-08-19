from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

SHA = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^(?:-\s*)?uses:\s*(.+)$")
PERMISSIONS_SCALAR = re.compile(r"^permissions:\s*(\S+)\s*$")
PERMISSIONS_KEY = re.compile(r"^([A-Za-z0-9_-]+):\s*(\S+)\s*$")
AWS_KEY_ENV = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
)
UNFROZEN_UV = re.compile(r"\buv\s+run\b(?![^\n]*--frozen)")
PIP_INSTALL = re.compile(r"\b(?:uv\s+pip\s+install|pip(?:3)?\s+install)\b")
LOCAL_ACTION = re.compile(r"^\./")
DOCKER_ACTION = re.compile(r"^docker://")


@dataclass(frozen=True, order=True)
class Violation:
    path: str
    line: int
    message: str


def _strip_comment(line: str) -> str:
    in_single = False
    in_double = False
    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif (
            char == "#"
            and not in_single
            and not in_double
            and (index == 0 or line[index - 1].isspace())
        ):
            return line[:index].rstrip()
    return line.rstrip()


def _indent(line: str) -> int:
    return len(line) - len(line.lstrip(" "))


def _action_ref(raw: str) -> str:
    return raw.strip().strip("'\"").split()[0]


def _check_action(path: Path, line_number: int, ref: str) -> list[Violation]:
    if LOCAL_ACTION.match(ref):
        return []
    if DOCKER_ACTION.match(ref):
        return [
            Violation(
                str(path),
                line_number,
                f"docker Action references are not permitted: {ref}",
            )
        ]
    if "@" not in ref:
        return [Violation(str(path), line_number, f"Action is not SHA-pinned: {ref}")]
    name, pin = ref.rsplit("@", 1)
    if "/" not in name:
        return [Violation(str(path), line_number, f"malformed Action ref: {ref}")]
    if not SHA.fullmatch(pin):
        return [
            Violation(
                str(path),
                line_number,
                f"movable Action tag or non-SHA pin: {ref}",
            )
        ]
    return []


def _permission_violations(
    path: Path, start_line: int, mapping: dict[str, tuple[int, str]]
) -> list[Violation]:
    violations: list[Violation] = []
    if not mapping:
        violations.append(Violation(str(path), start_line, "permissions mapping is empty"))
        return violations
    allowed = {"contents": {"read"}, "id-token": {"write"}}
    for key, (line_number, value) in mapping.items():
        if key not in allowed or value not in allowed[key]:
            violations.append(
                Violation(
                    str(path),
                    line_number,
                    f"excessive or forbidden permission: {key}: {value}",
                )
            )
    if "contents" not in mapping:
        violations.append(
            Violation(str(path), start_line, "permissions must include contents: read")
        )
    return violations


def check_workflow(path: Path, text: str) -> list[Violation]:
    violations: list[Violation] = []
    lines = text.splitlines()
    saw_permissions = False
    saw_make_check = False
    saw_python_312 = False
    has_role_to_assume = False
    has_id_token_write = False

    index = 0
    while index < len(lines):
        line_number = index + 1
        raw = lines[index]
        stripped = _strip_comment(raw).strip()
        if not stripped:
            index += 1
            continue

        uses = USES.match(stripped)
        if uses:
            violations.extend(_check_action(path, line_number, _action_ref(uses.group(1))))
            index += 1
            continue

        if stripped == "make check" or stripped.endswith(" make check"):
            saw_make_check = True

        if 'python-version: "3.12"' in stripped or "python-version: '3.12'" in stripped:
            saw_python_312 = True
        if "role-to-assume" in stripped:
            has_role_to_assume = True

        for env_name in AWS_KEY_ENV:
            if env_name in stripped:
                violations.append(
                    Violation(
                        str(path),
                        line_number,
                        f"long-lived AWS credential path: {env_name}",
                    )
                )

        if UNFROZEN_UV.search(stripped):
            violations.append(
                Violation(str(path), line_number, "unfrozen uv run (missing --frozen)")
            )
        if PIP_INSTALL.search(stripped):
            violations.append(
                Violation(str(path), line_number, "unlocked pip/uv pip install is forbidden")
            )

        scalar = PERMISSIONS_SCALAR.match(stripped)
        if scalar and scalar.group(1) not in {"", "|", ">"}:
            saw_permissions = True
            violations.append(
                Violation(
                    str(path),
                    line_number,
                    f"excessive permissions: {scalar.group(1)}",
                )
            )
            index += 1
            continue

        if stripped == "permissions:":
            saw_permissions = True
            mapping: dict[str, tuple[int, str]] = {}
            base = _indent(raw)
            index += 1
            while index < len(lines):
                nested_raw = lines[index]
                nested = _strip_comment(nested_raw)
                if not nested.strip():
                    index += 1
                    continue
                if _indent(nested_raw) <= base:
                    break
                match = PERMISSIONS_KEY.match(nested.strip())
                if not match:
                    violations.append(
                        Violation(
                            str(path),
                            index + 1,
                            f"unparseable permission entry: {nested.strip()}",
                        )
                    )
                    index += 1
                    continue
                key, value = match.group(1), match.group(2)
                mapping[key] = (index + 1, value)
                if key == "id-token" and value == "write":
                    has_id_token_write = True
                index += 1
            violations.extend(_permission_violations(path, line_number, mapping))
            continue

        index += 1

    if not saw_permissions:
        violations.append(Violation(str(path), 1, "missing explicit permissions block"))
    if path.name == "check.yml" and not saw_make_check:
        violations.append(
            Violation(str(path), 1, "check.yml must invoke make check, not a divergent graph")
        )
    if ("make check" in text or "check_secrets.py" in text) and "fetch-depth: 0" not in text:
        violations.append(
            Violation(
                str(path),
                1,
                "history-sensitive qualification requires fetch-depth: 0",
            )
        )
    if not saw_python_312:
        violations.append(
            Violation(str(path), 1, "workflow must pin CPython 3.12 as the qualification runtime")
        )
    if has_id_token_write and not has_role_to_assume:
        violations.append(
            Violation(
                str(path),
                1,
                "id-token: write is only allowed with an OIDC role-to-assume",
            )
        )
    return violations


def check(root: Path) -> list[Violation]:
    workflow_root = root / ".github" / "workflows"
    if not workflow_root.is_dir():
        return [Violation(str(workflow_root), 0, "workflow directory does not exist")]

    files = sorted(workflow_root.glob("*.yml")) + sorted(workflow_root.glob("*.yaml"))
    if not files:
        return [Violation(str(workflow_root), 0, "no workflow files found")]

    names = {path.name for path in files}
    required = {"check.yml", "security-provenance.yml"}
    missing = sorted(required - names)
    violations: list[Violation] = [
        Violation(str(workflow_root / name), 0, "required workflow is missing") for name in missing
    ]
    for path in files:
        violations.extend(check_workflow(path, path.read_text(encoding="utf-8")))
    return sorted(set(violations))


def _check_paths(root: Path) -> list[Violation]:
    if root.is_file():
        return sorted(set(check_workflow(root, root.read_text(encoding="utf-8"))))
    if (root / ".github" / "workflows").is_dir():
        return check(root)
    files = sorted(root.glob("*.yml")) + sorted(root.glob("*.yaml"))
    if not files:
        return [Violation(str(root), 0, "no workflow files found")]
    violations: list[Violation] = []
    for path in files:
        violations.extend(check_workflow(path, path.read_text(encoding="utf-8")))
    return sorted(set(violations))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check GitHub Actions provenance policy.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root, a workflow directory, or a single workflow file",
    )
    args = parser.parse_args(argv)
    violations = _check_paths(args.root.resolve())

    if not violations:
        print("github workflow policy: OK")
        return 0
    for violation in violations:
        location = f"{violation.path}:{violation.line}" if violation.line else violation.path
        print(f"{location}: {violation.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
