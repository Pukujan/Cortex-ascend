from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = (
    "Phase",
    "Requirement IDs",
    "Affected invariants",
    "Acceptance evidence",
    "Documentation / handoff impact",
    "Trust / architecture boundary",
)
HEADING = re.compile(r"^##[ \t]+(.+?)[ \t]*$")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)


def sections(body: str) -> dict[str, str]:
    found: dict[str, list[str]] = {}
    current: str | None = None
    for line in body.splitlines():
        match = HEADING.match(line)
        if match:
            current = match.group(1).strip()
            found.setdefault(current, [])
            continue
        if current is not None:
            found[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in found.items()}


def _meaningful(text: str) -> bool:
    without_comments = HTML_COMMENT.sub("", text)
    value = without_comments.strip()
    if not value:
        return False
    normalized = value.lower().strip("`*_ -.\n\t")
    return normalized not in {"todo", "tbd", "required", "replace me"}


def validate(body: str) -> list[str]:
    found = sections(body)
    errors: list[str] = []
    for name in REQUIRED_SECTIONS:
        if name not in found:
            errors.append(f"missing required PR section: {name}")
        elif not _meaningful(found[name]):
            errors.append(f"required PR section has no disposition: {name}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the Cortex Ascend PR contract.")
    parser.add_argument("body_file", type=Path, help="File containing the pull request body.")
    args = parser.parse_args(argv)

    try:
        body = args.body_file.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"PR contract validation failed: {exc}", file=sys.stderr)
        return 1

    errors = validate(body)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("PR contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
