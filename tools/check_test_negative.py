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
    expected: tuple[str, ...]


CASES = (
    Case(
        "deterministic-failure",
        (
            "uv",
            "run",
            "--frozen",
            "pytest",
            "-q",
            "tests/test_harness_fixtures/deterministic_failure",
        ),
        ("seeded deterministic failure",),
    ),
    Case(
        "hypothesis-failure",
        (
            "uv",
            "run",
            "--frozen",
            "pytest",
            "-q",
            "--hypothesis-seed=1",
            "tests/test_harness_fixtures/property_failure",
        ),
        ("Failing test case", "value=0"),
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
            continue
        missing = [needle for needle in case.expected if needle not in combined]
        if missing:
            failures.append(
                f"{case.name}: expected diagnostics {missing!r} not found; output={combined!r}"
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print(f"test negative fixtures: OK ({len(CASES)} expected failures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
