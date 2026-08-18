from __future__ import annotations

import argparse
import sys
from pathlib import Path

from handoff_manifest import ManifestError, load_and_validate
from render_handoff import check_or_write


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Cortex Ascend documentation gates.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: inferred from tools/)",
    )
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()

    try:
        load_and_validate(root / "handoff.yaml")
        result = check_or_write(root, write=False)
    except (ManifestError, OSError) as exc:
        print(f"documentation gate failed: {exc}", file=sys.stderr)
        return 1

    if result:
        return result
    print("documentation gate: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
