from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import cast

type YamlValue = None | bool | int | str | list["YamlValue"] | dict[str, "YamlValue"]


class ManifestError(ValueError):
    """Raised when the restricted handoff manifest cannot be parsed or validated."""


def _scalar(text: str) -> YamlValue:
    value = text.strip()
    if value == "[]":
        return []
    if value == "null":
        return None
    if value == "true":
        return True
    if value == "false":
        return False
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", value):
        return int(value)
    if value.startswith(("'", '"')):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ManifestError(f"invalid quoted scalar: {value}") from exc
        if not isinstance(parsed, str):
            raise ManifestError(f"quoted scalar must be a string: {value}")
        return parsed
    return value


def _split_mapping(text: str, line_number: int) -> tuple[str, str]:
    if ":" not in text:
        raise ManifestError(f"line {line_number}: expected 'key: value'")
    key, value = text.split(":", 1)
    key = key.strip()
    if not key or not re.fullmatch(r"[A-Za-z0-9_-]+", key):
        raise ManifestError(f"line {line_number}: invalid key {key!r}")
    return key, value.strip()


def _tokens(text: str) -> list[tuple[int, str, int]]:
    tokens: list[tuple[int, str, int]] = []
    for number, raw in enumerate(text.splitlines(), start=1):
        if "\t" in raw:
            raise ManifestError(f"line {number}: tabs are not allowed")
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if indent % 2:
            raise ManifestError(f"line {number}: indentation must use multiples of two spaces")
        tokens.append((indent, raw[indent:], number))
    return tokens


def _parse_block(
    tokens: list[tuple[int, str, int]], index: int, indent: int
) -> tuple[YamlValue, int]:
    if index >= len(tokens):
        raise ManifestError("unexpected end of manifest")
    actual_indent, first, line_number = tokens[index]
    if actual_indent != indent:
        raise ManifestError(
            f"line {line_number}: expected indentation {indent}, got {actual_indent}"
        )
    if first.startswith("- "):
        return _parse_list(tokens, index, indent)
    return _parse_map(tokens, index, indent)


def _parse_map(
    tokens: list[tuple[int, str, int]], index: int, indent: int
) -> tuple[dict[str, YamlValue], int]:
    result: dict[str, YamlValue] = {}
    while index < len(tokens):
        actual_indent, text, line_number = tokens[index]
        if actual_indent < indent:
            break
        if actual_indent > indent:
            raise ManifestError(
                f"line {line_number}: unexpected indentation {actual_indent}; expected {indent}"
            )
        if text.startswith("- "):
            break

        key, value_text = _split_mapping(text, line_number)
        if key in result:
            raise ManifestError(f"line {line_number}: duplicate key {key!r}")
        index += 1

        if value_text:
            result[key] = _scalar(value_text)
            continue

        if index >= len(tokens) or tokens[index][0] <= indent:
            result[key] = {}
            continue
        if tokens[index][0] != indent + 2:
            raise ManifestError(
                f"line {tokens[index][2]}: nested block must indent by exactly two spaces"
            )
        value, index = _parse_block(tokens, index, indent + 2)
        result[key] = value

    return result, index


def _parse_list(
    tokens: list[tuple[int, str, int]], index: int, indent: int
) -> tuple[list[YamlValue], int]:
    result: list[YamlValue] = []
    while index < len(tokens):
        actual_indent, text, line_number = tokens[index]
        if actual_indent < indent:
            break
        if actual_indent != indent or not text.startswith("- "):
            break

        item_text = text[2:].strip()
        index += 1
        if not item_text:
            if index >= len(tokens) or tokens[index][0] != indent + 2:
                raise ManifestError(f"line {line_number}: list item requires a nested value")
            value, index = _parse_block(tokens, index, indent + 2)
            result.append(value)
            continue

        if ":" not in item_text:
            result.append(_scalar(item_text))
            continue

        key, value_text = _split_mapping(item_text, line_number)
        mapping: dict[str, YamlValue] = {}
        if value_text:
            mapping[key] = _scalar(value_text)
        elif index >= len(tokens) or tokens[index][0] != indent + 2:
            mapping[key] = {}
        else:
            nested, index = _parse_block(tokens, index, indent + 2)
            mapping[key] = nested

        while index < len(tokens):
            next_indent, next_text, next_line = tokens[index]
            if next_indent <= indent:
                break
            if next_indent != indent + 2:
                raise ManifestError(
                    f"line {next_line}: list mapping continuation must indent by two spaces"
                )
            if next_text.startswith("- "):
                raise ManifestError(
                    f"line {next_line}: unexpected list item in mapping continuation"
                )

            subkey, subvalue_text = _split_mapping(next_text, next_line)
            if subkey in mapping:
                raise ManifestError(f"line {next_line}: duplicate key {subkey!r}")
            index += 1
            if subvalue_text:
                mapping[subkey] = _scalar(subvalue_text)
            elif index >= len(tokens) or tokens[index][0] <= next_indent:
                mapping[subkey] = {}
            else:
                if tokens[index][0] != next_indent + 2:
                    raise ManifestError(
                        f"line {tokens[index][2]}: nested block must indent by two spaces"
                    )
                nested, index = _parse_block(tokens, index, next_indent + 2)
                mapping[subkey] = nested

        result.append(mapping)

    return result, index


def loads_manifest(text: str) -> dict[str, YamlValue]:
    """Parse the deliberately restricted YAML subset used by handoff.yaml."""
    tokens = _tokens(text)
    if not tokens:
        raise ManifestError("manifest is empty")
    value, index = _parse_block(tokens, 0, 0)
    if index != len(tokens):
        _, _, line_number = tokens[index]
        raise ManifestError(f"line {line_number}: unparsed content remains")
    if not isinstance(value, dict):
        raise ManifestError("manifest root must be a mapping")
    return value


def load_manifest(path: Path) -> dict[str, YamlValue]:
    return loads_manifest(path.read_text(encoding="utf-8"))


def _mapping(parent: dict[str, YamlValue], key: str) -> dict[str, YamlValue]:
    value = parent.get(key)
    if not isinstance(value, dict):
        raise ManifestError(f"missing mapping {key!r}")
    return value


def _string(parent: dict[str, YamlValue], key: str) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"missing non-empty string {key!r}")
    return value


def _integer(parent: dict[str, YamlValue], key: str) -> int:
    value = parent.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ManifestError(f"missing integer {key!r}")
    return value


def _boolean(parent: dict[str, YamlValue], key: str) -> bool:
    value = parent.get(key)
    if not isinstance(value, bool):
        raise ManifestError(f"missing boolean {key!r}")
    return value


def _int_list(parent: dict[str, YamlValue], key: str) -> list[int]:
    value = parent.get(key)
    if not isinstance(value, list) or any(
        isinstance(item, bool) or not isinstance(item, int) for item in value
    ):
        raise ManifestError(f"{key!r} must be a list of integers")
    return cast(list[int], value)


def _str_list(parent: dict[str, YamlValue], key: str) -> list[str]:
    value = parent.get(key)
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ManifestError(f"{key!r} must be a list of non-empty strings")
    return cast(list[str], value)


def validate_manifest(manifest: dict[str, YamlValue]) -> None:
    """Validate the handoff fields needed to reconstruct current project state."""
    if _integer(manifest, "handoff_version") != 1:
        raise ManifestError("unsupported handoff_version; expected 1")

    project = _mapping(manifest, "project")
    _string(project, "name")
    _string(project, "repository")
    _string(project, "default_branch")
    _string(project, "status")
    _boolean(project, "architecture_frozen")

    authority = _mapping(manifest, "authority")
    _string(authority, "canonical_plan")
    _string(authority, "phase_contract")
    _string(authority, "current_state")

    gate = _mapping(manifest, "current_gate")
    _string(gate, "id")
    _string(gate, "name")
    _integer(gate, "issue")
    current_child = gate.get("current_child_issue")
    if current_child is not None and (
        isinstance(current_child, bool) or not isinstance(current_child, int)
    ):
        raise ManifestError("'current_child_issue' must be null or an integer")
    _str_list(gate, "implemented_capabilities")
    _str_list(gate, "authorized_work")
    _str_list(gate, "forbidden_work")

    execution = _mapping(manifest, "g0_execution")
    child_issues = _int_list(execution, "child_issues")
    completed = _int_list(execution, "completed_child_issues")
    active = _int_list(execution, "active_child_issues")
    if len(set(child_issues)) != len(child_issues):
        raise ManifestError("'child_issues' contains duplicates")
    if not set(completed).issubset(child_issues):
        raise ManifestError("completed G0 child issue is absent from 'child_issues'")
    if not set(active).issubset(child_issues):
        raise ManifestError("active G0 child issue is absent from 'child_issues'")
    overlap = sorted(set(completed) & set(active))
    if overlap:
        raise ManifestError(f"G0 child issues cannot be completed and active: {overlap}")
    convergence = _integer(execution, "convergence_issue")
    if convergence not in child_issues:
        raise ManifestError("'convergence_issue' must be a G0 child issue")
    _integer(execution, "conditional_transport_issue")
    _integer(execution, "independent_critic_issue")
    _integer(execution, "exit_issue")

    session = _mapping(manifest, "fresh_session_start")
    _str_list(session, "read_order")
    _string(session, "instruction")


def load_and_validate(path: Path) -> dict[str, YamlValue]:
    manifest = load_manifest(path)
    validate_manifest(manifest)
    return manifest
