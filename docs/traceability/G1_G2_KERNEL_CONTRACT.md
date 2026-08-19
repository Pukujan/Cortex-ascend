# G1-G2 — Pure Kernel, WorkContract, and EvidenceReceipt

## Scope
Implement the smallest vendor-neutral semantic kernel and the initial
machine-readable work/evidence contracts, per issue #2.

## Delivered

| Deliverable | File | Notes |
|-------------|------|-------|
| Immutable domain types | `src/cortex_ascend/kernel/types.py` | `ProjectSnapshot`, `WorkId`, `Generation`, `ArtifactDigest`, `AuthorityGrant`, `ModelIdentity`, `EvidenceReceipt`, `AdmissionDecision` |
| Decision enum | `src/cortex_ascend/kernel/types.py` | `ADMIT`, `REJECT`, `STALE`, `BLOCKED` |
| WorkContract v1 | `src/cortex_ascend/kernel/contract.py` | Addressable adjudicated work envelope; not semantic truth |
| Canonical serialization | `src/cortex_ascend/kernel/serialization.py` | Deterministic JSON + SHA-256; `compare=False` metadata excluded from identity |
| Pure predicates | `src/cortex_ascend/kernel/predicates.py` | freshness, authority, evidence binding, model identity |
| Kernel package exports | `src/cortex_ascend/kernel/__init__.py` | Stable public API |
| Unit tests | `tests/unit/test_kernel.py` | 14 tests covering all types and predicates |
| Property tests | `tests/property/test_kernel_properties.py` | 3 Hypothesis properties |
| Mutation tests | `tests/unit/test_kernel_mutations.py` | 5 seeded mutants killed by adjudication |

## Hard constraints satisfied

- No AWS/AgentCore/LiteLLM/OpenCode/FOSSIL/GitHub/model SDK imports in `kernel`.
- `WorkContract` is an addressable adjudicated envelope, not semantic truth.
- Requested vs actual model identity are separate fields (`requested_model` and metadata `actual_model`).
- Worker-local claims do not constitute qualification evidence (`adjudicate` ignores `worker_claims`).
- Canonical hashes change when material identity changes and are stable when only `compare=False` metadata changes.

## Invariants exercised

| Invariant | How it is exercised |
|-----------|---------------------|
| ASC-INV-KRN-001 | `adjudicate_against_base` returns `STALE` when the contract base differs from the current snapshot. |
| ASC-INV-KRN-003 | `is_evidence_bound` requires every receipt authority to contain the contract's `work_id`. |
| ASC-INV-MDL-002 | `model_identity_compatible` rejects contracts whose actual model differs from the requested model. |

## Evidence
- `make check` passes, including all negative harnesses.
- Architecture checker remains green: no prohibited third-party imports in `kernel`.
- 19 unit tests and 4 property tests pass.

## Next phase
- Gate: G3 — Prove stale-generation lifecycle semantics and select one formalism.
- Issue: #3

## Related work
- Parent: #2
- Depends on: #1 (closed)
