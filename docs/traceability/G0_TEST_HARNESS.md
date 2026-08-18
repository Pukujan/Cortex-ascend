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

This branch deliberately pins Pytest `9.1.1` and Hypothesis `6.165.10` in the project development dependency group, but it is **not merge-ready** until a trusted environment can resolve those packages, regenerate `uv.lock`, and execute both positive and deliberate-negative tests with `--frozen`.

The current bootstrap runner has no outbound PyPI connectivity and no preloaded Hypothesis distribution. The unrelated globally installed Pytest is not accepted as locked project evidence. Hand-authoring the lockfile is prohibited; a real `uv` resolution is required before acceptance evidence can be claimed.
