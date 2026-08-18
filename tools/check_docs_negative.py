from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
REPO = TOOLS.parent


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _copy_minimal_repo(destination: Path) -> None:
    (destination / "docs").mkdir(parents=True)
    for relative in (
        Path("handoff.yaml"),
        Path("docs/HANDOFF.md"),
        Path("docs/CURRENT_STATE.md"),
    ):
        target = destination / relative
        target.write_text((REPO / relative).read_text(encoding="utf-8"), encoding="utf-8")


def main() -> int:
    failures: list[str] = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _copy_minimal_repo(root)

        baseline = _run(str(TOOLS / "render_handoff.py"), "--repo-root", str(root))
        if baseline.returncode != 0:
            failures.append(f"baseline generated-doc check failed: {baseline.stderr!r}")
        else:
            handoff = root / "handoff.yaml"
            text = handoff.read_text(encoding="utf-8")
            handoff.write_text(
                text.replace(
                    "status: REVISE -> START G0 ONLY",
                    "status: REVISE -> START G0 ONLY STALE-PROBE",
                    1,
                ),
                encoding="utf-8",
            )
            stale = _run(str(TOOLS / "render_handoff.py"), "--repo-root", str(root))
            combined = stale.stdout + stale.stderr
            if stale.returncode == 0 or "generated handoff facts are stale" not in combined:
                failures.append("stale-doc fixture was not rejected for generated handoff drift")

    malformed = _run(
        str(TOOLS / "render_handoff.py"),
        "--repo-root",
        str(REPO / "tests" / "docs" / "fixtures" / "missing_current_gate"),
    )
    malformed_output = malformed.stdout + malformed.stderr
    if malformed.returncode == 0 or "missing mapping 'current_gate'" not in malformed_output:
        failures.append("incomplete handoff fixture was not rejected for missing current_gate")

    pr_result = _run(
        str(TOOLS / "check_pr_contract.py"),
        str(REPO / "tests" / "docs" / "fixtures" / "pr_missing_requirements.md"),
    )
    pr_output = pr_result.stdout + pr_result.stderr
    if pr_result.returncode == 0 or "missing required PR section: Requirement IDs" not in pr_output:
        failures.append("incomplete PR contract fixture was not rejected")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("documentation negative fixtures: OK (3 expected failures)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
