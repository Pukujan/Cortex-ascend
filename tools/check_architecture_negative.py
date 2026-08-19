from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Case:
    name: str
    expected: tuple[str, ...]


CASES = (
    Case("prohibited_kernel_import", ("prohibited kernel third-party import: boto3",)),
    Case("reverse_layer_import", ("forbidden layer import: kernel -> application",)),
    Case("architecture_cycle", ("architecture cycle:", "application", "ports")),
    Case("package_root_third_party", ("prohibited package-root third-party import: boto3",)),
)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    checker = repo / "tools" / "check_architecture.py"
    fixtures = repo / "tests" / "architecture" / "fixtures"
    failures: list[str] = []

    for case in CASES:
        result = subprocess.run(
            [sys.executable, str(checker), "--root", str(fixtures / case.name / "src")],
            check=False,
            capture_output=True,
            text=True,
        )
        combined = result.stdout + result.stderr
        if result.returncode == 0:
            failures.append(f"{case.name}: fixture unexpectedly passed")
            continue
        missing = [needle for needle in case.expected if needle not in combined]
        if missing:
            failures.append(
                f"{case.name}: missing expected diagnostics {missing!r}; output={combined!r}"
            )

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print(f"architecture negative fixtures: OK ({len(CASES)} expected failures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
