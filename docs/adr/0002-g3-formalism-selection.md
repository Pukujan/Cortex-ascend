# ADR 0002 — Primary distributed formalism for stale-generation semantics

## Status
Accepted

## Context
G3 requires a bounded comparison of TLA+/TLC, P/P-Checker, and FizzBee for the
same stale-generation lifecycle model, followed by selection of one primary
distributed formalism.

## Comparison

| Criterion | TLA+/TLC | P/P-Checker | FizzBee |
|-----------|----------|-------------|---------|
| Toolchain available in workspace | OpenJDK 21 present | Requires .NET 8 SDK; only .NET 6 SDK installed | Requires Go; not installed |
| Setup burden | Low (single JAR) | Medium (SDK upgrade + tool install) | Medium (Go install + tool install) |
| CI reproducibility | High (deterministic BFS, fixed seed) | High | High |
| Counterexample quality | Good (state trace + variable values) | Good | Unknown in this workspace |
| Implementation-conformance path | Manual mapping to Python predicates | Manual mapping | Manual mapping |
| Maintainability | High (large ecosystem, textual specs) | Medium | Lower (newer, smaller ecosystem) |
| Bounded model checked for G3 | Yes: 425 distinct states, no invariant violation | Not evaluated (blocked) | Not evaluated (blocked) |

## Decision
Select **TLA+/TLC** as the primary distributed formalism for G3 and subsequent
phases.

## Rationale
- TLA+/TLC is the only candidate that could be set up and run without
  installing new language SDKs in the workspace.
- The bounded lifecycle spec produced reproducible counterexamples during
  refinement and a clean final model-check result (1016 states generated,
  425 distinct states, `NoStaleAdmit` invariant held).
- P and FizzBee remain acceptable alternatives for future ADRs if their
  toolchain constraints change, but they are removed from the normal G3 path.

## Consequences
- Formal specs live under `tools/external/` as `.tla` and `.cfg` files.
- CI may invoke TLC via `java -cp tools/external/tla2tools.jar tlc2.TLC ...`
  once a Makefile target is added.
- Mapping from TLA+ invariants to executable Python tests is manual and must
  be documented per property.

## Related
- Issue #3
- `tools/external/StaleGenerationLifecycle.tla`
- `tools/external/StaleGenerationLifecycle.cfg`
- `src/cortex_ascend/kernel/lifecycle.py`
