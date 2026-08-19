from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent
FIXTURE = REPO / "tests" / "ci" / "fixtures" / "secrets"


def main() -> int:
    result = subprocess.run(
        [
            sys.executable,
            str(TOOLS / "check_secrets.py"),
            "--root",
            str(FIXTURE),
            "--tree-only",
            "--no-history",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    combined = result.stdout + result.stderr
    expected = ("aws-access-key-id", "github-pat")
    missing = [needle for needle in expected if needle not in combined]
    if result.returncode == 0 or missing:
        print(
            f"seeded fake credential was not detected: missing={missing!r} output={combined!r}",
            file=sys.stderr,
        )
        return 1
    print("secret negative fixtures: OK (1 expected failure)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
