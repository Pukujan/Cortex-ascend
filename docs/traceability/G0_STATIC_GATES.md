# G0 Static Gate Traceability

## Contract

Requirement: `ASC-G0-R2`  
Invariants: `ASC-INV-FND-002`, `ASC-INV-FND-005`

The intended locked static-quality commands are:

```text
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen mypy --strict src/cortex_ascend tools
python tools/check_static_negative.py
```

Ruff targets Python 3.12. Mypy is configured in strict mode for the package and qualification tooling. Deliberately invalid static fixtures are excluded from the positive repository scan and exercised separately by the negative harness.

## Deliberate negative cases

- an unused import must produce Ruff `F401`;
- a function declared to return `int` but returning `str` must produce Mypy's incompatible-return diagnostic.

## Bootstrap execution status

This branch deliberately pins Ruff `0.16.3` and Mypy `2.3.1` in the project development dependency group, but it is **not merge-ready** until a trusted environment can resolve those packages, regenerate `uv.lock`, and execute both positive and negative commands with `--frozen`.

The current bootstrap runner has no outbound PyPI connectivity and no preloaded Ruff/Mypy distributions. Hand-authoring the lockfile is prohibited; a real `uv` resolution is required before acceptance evidence can be claimed.
