from __future__ import annotations

import argparse
import ast
import sys
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

PACKAGE = "cortex_ascend"
LAYERS = ("kernel", "ports", "application", "adapters", "cli")
ALLOWED_LAYER_IMPORTS: dict[str, frozenset[str]] = {
    "kernel": frozenset({"kernel"}),
    "ports": frozenset({"kernel", "ports"}),
    "application": frozenset({"kernel", "ports", "application"}),
    "adapters": frozenset({"kernel", "ports", "application", "adapters"}),
    "cli": frozenset({"kernel", "ports", "application", "adapters", "cli"}),
}


@dataclass(frozen=True, order=True)
class Violation:
    path: str
    line: int
    message: str


def _module_for_file(path: Path, package_root: Path) -> tuple[str, ...]:
    relative = path.relative_to(package_root)
    parts = list(relative.with_suffix("").parts)
    if parts[-1] == "__init__":
        parts.pop()
    return (PACKAGE, *parts)


def _current_package(module: tuple[str, ...], path: Path) -> tuple[str, ...]:
    if path.name == "__init__.py":
        return module
    return module[:-1]


def _resolve_import_from(
    node: ast.ImportFrom,
    current_package: tuple[str, ...],
) -> str | None:
    if node.level == 0:
        return node.module

    if node.level > len(current_package):
        return None
    anchor = current_package[: len(current_package) - node.level + 1]
    suffix = tuple(node.module.split(".")) if node.module else ()
    return ".".join((*anchor, *suffix))


def _literal_dynamic_imports(tree: ast.AST) -> Iterable[tuple[str, int]]:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not node.args:
            continue
        first = node.args[0]
        if not isinstance(first, ast.Constant) or not isinstance(first.value, str):
            continue

        if isinstance(node.func, ast.Name) and node.func.id == "__import__":
            yield first.value, node.lineno
            continue

        if (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "import_module"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "importlib"
        ):
            yield first.value, node.lineno


def _imports_for_file(path: Path, package_root: Path) -> list[tuple[str, int]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    module = _module_for_file(path, package_root)
    current_package = _current_package(module, path)
    imports: list[tuple[str, int]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((alias.name, node.lineno) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            resolved = _resolve_import_from(node, current_package)
            if resolved:
                imports.append((resolved, node.lineno))

    imports.extend(_literal_dynamic_imports(tree))
    return imports


def _layer_from_module(module: str) -> str | None:
    parts = module.split(".")
    if len(parts) >= 2 and parts[0] == PACKAGE and parts[1] in LAYERS:
        return parts[1]
    return None


def _cycle(layer_edges: set[tuple[str, str]]) -> tuple[str, ...] | None:
    adjacency: dict[str, set[str]] = {layer: set() for layer in LAYERS}
    for source, target in layer_edges:
        if source != target:
            adjacency[source].add(target)

    visited: set[str] = set()
    active: list[str] = []
    active_set: set[str] = set()

    def visit(layer: str) -> tuple[str, ...] | None:
        if layer in active_set:
            start = active.index(layer)
            return (*active[start:], layer)
        if layer in visited:
            return None

        visited.add(layer)
        active.append(layer)
        active_set.add(layer)
        for target in sorted(adjacency[layer]):
            found = visit(target)
            if found:
                return found
        active.pop()
        active_set.remove(layer)
        return None

    for layer in LAYERS:
        found = visit(layer)
        if found:
            return found
    return None


def check(root: Path) -> list[Violation]:
    package_root = root / PACKAGE
    if not package_root.is_dir():
        return [Violation(str(package_root), 0, "package root does not exist")]

    violations: list[Violation] = []
    layer_edges: set[tuple[str, str]] = set()
    stdlib = sys.stdlib_module_names

    for path in sorted(package_root.rglob("*.py")):
        relative = path.relative_to(package_root)
        if relative.parts and relative.parts[0] in LAYERS:
            source_layer = relative.parts[0]
            root_equivalent = False
        else:
            # Package-root files are not inside a recognized layer. They are
            # reachable from any layer (including kernel) via `import cortex_ascend`,
            # so they must satisfy the strictest third-party deny.
            source_layer = None
            root_equivalent = True

        try:
            imports = _imports_for_file(path, package_root)
        except SyntaxError as exc:
            violations.append(
                Violation(str(path), exc.lineno or 0, f"cannot parse Python source: {exc.msg}")
            )
            continue

        for module, line in imports:
            target_layer = _layer_from_module(module)
            if source_layer is not None and target_layer is not None:
                layer_edges.add((source_layer, target_layer))
                if target_layer not in ALLOWED_LAYER_IMPORTS[source_layer]:
                    violations.append(
                        Violation(
                            str(path),
                            line,
                            f"forbidden layer import: {source_layer} -> {target_layer} ({module})",
                        )
                    )
                continue

            top_level = module.split(".", 1)[0]
            if (
                (source_layer == "kernel" or root_equivalent)
                and top_level not in stdlib
                and top_level != PACKAGE
            ):
                location = "package-root" if root_equivalent else "kernel"
                violations.append(
                    Violation(
                        str(path),
                        line,
                        f"prohibited {location} third-party import: {module}",
                    )
                )

    found_cycle = _cycle(layer_edges)
    if found_cycle:
        violations.append(
            Violation(
                str(package_root),
                0,
                "architecture cycle: " + " -> ".join(found_cycle),
            )
        )

    return sorted(set(violations))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check Cortex Ascend dependency boundaries.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("src"),
        help="Source root containing cortex_ascend/ (default: src)",
    )
    args = parser.parse_args(argv)

    violations = check(args.root)
    if not violations:
        print("architecture check: OK")
        return 0

    for violation in violations:
        location = f"{violation.path}:{violation.line}" if violation.line else violation.path
        print(f"{location}: {violation.message}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
