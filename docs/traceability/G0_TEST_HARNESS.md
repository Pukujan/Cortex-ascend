# G0 Test Harness Traceability

## Contract

Requirement: `ASC-G0-R3`  
Invariant: `ASC-INV-FND-005`

The intended locked baseline commands are:

```text
uv run --frozen pytest -q tests/unit
uv run --frozen pytest -q tests/property
python tools/check_test_negative.py
```

`pytest` is configured with strict config/marker handling and `src` on the import path. Hypothesis is present from the first property-test foundation. The positive tests are deliberately non-semantic: they exercise package importability and a simple reversible list property only.

## Deliberate negative cases

- a deterministic seeded failure must fail with the declared assertion message;
- a falsifiable Hypothesis property must shrink to `value=0` and report a falsifying example when run with the recorded seed.

A Hypothesis failure receipt should preserve the shrunk falsifying example and, when a seed is used, the seed needed to reproduce the run. The shrunk example is the primary debugging input; the seed records the generation path.

## Bootstrap execution status

Pytest `9.1.1` and Hypothesis `6.165.10` are pinned in the project
development dependency group and in the committed, real `uv.lock`. Their
locked positive and deliberate-negative commands are composed by `make check`.

This traceability document records the harness semantics; the exact CPython
3.12 qualification receipt remains part of the G0 exit evidence.
