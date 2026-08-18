from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path
from typing import cast

from handoff_manifest import ManifestError, YamlValue, load_and_validate

BEGIN = "<!-- BEGIN GENERATED HANDOFF FACTS -->"
END = "<!-- END GENERATED HANDOFF FACTS -->"
DOC_PATHS = (Path("docs/HANDOFF.md"), Path("docs/CURRENT_STATE.md"))


def _mapping(parent: dict[str, YamlValue], key: str) -> dict[str, YamlValue]:
    value = parent[key]
    assert isinstance(value, dict)
    return cast(dict[str, YamlValue], value)


def _strings(parent: dict[str, YamlValue], key: str) -> list[str]:
    value = parent[key]
    assert isinstance(value, list)
    return cast(list[str], value)


def _ints(parent: dict[str, YamlValue], key: str) -> list[int]:
    value = parent[key]
    assert isinstance(value, list)
    return cast(list[int], value)


def _issue_list(values: list[int]) -> str:
    return ", ".join(f"#{value}" for value in values) if values else "none"


def render_facts(manifest: dict[str, YamlValue]) -> str:
    project = _mapping(manifest, "project")
    gate = _mapping(manifest, "current_gate")
    execution = _mapping(manifest, "g0_execution")
    capabilities = _strings(gate, "implemented_capabilities")
    completed = _ints(execution, "completed_child_issues")
    active = _ints(execution, "active_child_issues")

    current_child = gate["current_child_issue"]
    current_child_text = f"#{current_child}" if isinstance(current_child, int) else "none"
    frozen = "yes" if project["architecture_frozen"] is True else "no"

    lines = [
        BEGIN,
        "> Generated from `handoff.yaml` by `tools/render_handoff.py`. "
        "Do not edit this block directly.",
        "",
        f"- Repository: `{project['repository']}` (default branch `{project['default_branch']}`)",
        f"- Project status: `{project['status']}`",
        f"- Architecture frozen: `{frozen}`",
        f"- Current gate: `{gate['id']} — {gate['name']}` (issue #{gate['issue']})",
        f"- Current child issue: {current_child_text}",
        "- Implemented capabilities: "
        + (", ".join(f"`{item}`" for item in capabilities) if capabilities else "none"),
        f"- Completed G0 child issues: {_issue_list(completed)}",
        f"- Active G0 child issues: {_issue_list(active)}",
        f"- G0 convergence issue: #{execution['convergence_issue']}",
        END,
    ]
    return "\n".join(lines)


def replace_generated_block(text: str, block: str, path: Path) -> str:
    if text.count(BEGIN) != 1 or text.count(END) != 1:
        raise ManifestError(
            f"{path}: expected exactly one generated handoff facts marker pair"
        )
    start = text.index(BEGIN)
    finish = text.index(END, start) + len(END)
    return text[:start] + block + text[finish:]


def check_or_write(repo_root: Path, write: bool) -> int:
    manifest = load_and_validate(repo_root / "handoff.yaml")
    block = render_facts(manifest)
    stale = False

    for relative in DOC_PATHS:
        path = repo_root / relative
        current = path.read_text(encoding="utf-8")
        expected = replace_generated_block(current, block, relative)
        if current == expected:
            continue
        if write:
            path.write_text(expected, encoding="utf-8")
            print(f"updated generated handoff facts: {relative}")
            continue

        stale = True
        print(f"{relative}: generated handoff facts are stale", file=sys.stderr)
        diff = difflib.unified_diff(
            current.splitlines(),
            expected.splitlines(),
            fromfile=str(relative),
            tofile=f"{relative} (expected)",
            lineterm="",
        )
        for line in diff:
            print(line, file=sys.stderr)

    if stale:
        return 1
    print("handoff/docs consistency: OK")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate handoff.yaml and check/write bounded generated fact blocks."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: inferred from tools/)",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Rewrite only the generated fact blocks; architectural prose is untouched.",
    )
    args = parser.parse_args(argv)

    try:
        return check_or_write(args.repo_root.resolve(), args.write)
    except (ManifestError, OSError) as exc:
        print(f"handoff/docs validation failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
