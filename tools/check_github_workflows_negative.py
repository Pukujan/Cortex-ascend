from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent


@dataclass(frozen=True)
class Case:
    name: str
    expected: str


CASES = (
    Case("movable_action_tag", "movable Action tag or non-SHA pin"),
    Case("excessive_permissions", "excessive permissions"),
    Case("unfrozen_uv", "unfrozen uv run"),
    Case("long_lived_aws_keys", "long-lived AWS credential path"),
)


def main() -> int:
    checker = TOOLS / "check_github_workflows.py"
    fixtures = REPO / "tests" / "ci" / "fixtures" / "workflows"
    failures: list[str] = []

    for case in CASES:
        result = subprocess.run(
            [sys.executable, str(checker), "--root", str(fixtures / f"{case.name}.yml")],
            check=False,
            capture_output=True,
            text=True,
        )
        combined = result.stdout + result.stderr
        if result.returncode == 0:
            failures.append(f"{case.name}: fixture unexpectedly passed")
        elif case.expected not in combined:
            failures.append(
                f"{case.name}: expected diagnostic {case.expected!r} not found; output={combined!r}"
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print(f"github workflow negative fixtures: OK ({len(CASES)} expected failures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
