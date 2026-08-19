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

Ruff `0.16.3` and Mypy `2.3.1` are pinned in the project development
dependency group and in the committed, real `uv.lock`. Their locked positive
and deliberate-negative commands are composed by `make check`.

This traceability document records the gate semantics; the exact CPython 3.12
qualification receipt remains part of the G0 exit evidence.
