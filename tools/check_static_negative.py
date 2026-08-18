from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Case:
    name: str
    command: tuple[str, ...]
    expected: str


CASES = (
    Case(
        "ruff-unused-import",
        (
            "uv",
            "run",
            "--frozen",
            "ruff",
            "check",
            "tests/static/fixtures/ruff_unused_import.py",
        ),
        "F401",
    ),
    Case(
        "mypy-return-type",
        (
            "uv",
            "run",
            "--frozen",
            "mypy",
            "--strict",
            "tests/static/fixtures/mypy_return_type.py",
        ),
        "Incompatible return value type",
    ),
)


def main() -> int:
    failures: list[str] = []
    for case in CASES:
        result = subprocess.run(
            case.command,
            cwd=REPO,
            check=False,
            capture_output=True,
            text=True,
        )
        combined = result.stdout + result.stderr
        if result.returncode == 0:
            failures.append(f"{case.name}: invalid fixture unexpectedly passed")
        elif case.expected not in combined:
            failures.append(
                f"{case.name}: expected diagnostic {case.expected!r} not found; "
                f"output={combined!r}"
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print(f"static negative fixtures: OK ({len(CASES)} expected failures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
