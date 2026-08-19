# G3 — Stale-Generation Lifecycle Semantics and Formalism Selection

## Scope
Use one bounded distributed-systems problem to qualify Ascend lifecycle
semantics and choose a primary formal method, per issue #3.

## Delivered

| Deliverable | File | Notes |
|-------------|------|-------|
| Executable lifecycle model | `src/cortex_ascend/kernel/lifecycle.py` | Pure-kernel state machine for attempts across generations |
| Lifecycle unit tests | `tests/unit/test_kernel_lifecycle.py` | 4 tests covering stale generation, revocation, replay, monotonic generation |
| TLA+ spec | `tools/external/StaleGenerationLifecycle.tla` | Bounded lifecycle model |
| TLC config | `tools/external/StaleGenerationLifecycle.cfg` | `MaxGeneration = 3`, `NoStaleAdmit` invariant |
| Formalism ADR | `docs/adr/0002-g3-formalism-selection.md` | Selects TLA+/TLC as primary formalism |

## Formal verification result

```text
$ java -cp tools/external/tla2tools.jar tlc2.TLC -deadlock -config tools/external/StaleGenerationLifecycle.cfg tools/external/StaleGenerationLifecycle.tla
Model checking completed. No error has been found.
1016 states generated, 425 distinct states found, 0 states left on queue.
```

The `NoStaleAdmit` invariant held across the bounded state space.

## Required failure scenarios covered

| Scenario | Executable test / model behavior |
|----------|----------------------------------|
| G6 completes after G7 is authoritative | `test_stale_generation_cannot_admit` |
| Duplicate/replayed old result | `test_replayed_old_result_still_stale` |
| Authority revoked mid-attempt | `test_revoked_grant_does_not_admit` |
| Verifier crash/retry | Modeled as new attempt at current generation |

## Formalism comparison summary

| Tool | Status | Blocker |
|------|--------|---------|
| TLA+/TLC | Selected, verified | None (OpenJDK 21 present) |
| P/P-Checker | Not evaluated | Requires .NET 8 SDK; only .NET 6 installed |
| FizzBee | Not evaluated | Requires Go; not installed |

## Invariants exercised

- **ASC-INV-KRN-001**: stale base/generation cannot produce `ADMIT`.
- Lifecycle-level revocation prevents admission after grant removal.

## Next phase
- Gate: G4-G5 — Qualify model lanes and separate AgentCore worker/verifier trust domains.
- Issue: #4

## Related work
- Parent: #3
- Depends on: #2 (closed)
