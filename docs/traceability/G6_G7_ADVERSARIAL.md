# G6-G7 — Adversarial Inference, Holdout, and Chaos

## Scope
Use abundant heterogeneous inference to search failure space while keeping
evaluation mechanically grounded and isolated, per issue #5.

## Delivered (kernel-side policy structures)

| Deliverable | File | Notes |
|-------------|------|-------|
| Adversarial seat identity | `src/cortex_ascend/kernel/adversarial.py` | `SeatIdentity` records vendor/model/provider/account/transport/context/runtime/credentials/holdout visibility/controller |
| Seat roles | `src/cortex_ascend/kernel/adversarial.py` | `RED_ARCH`, `RED_SEC`, `RED_DIST`, `MUTANT`, `FORMAL_ADV`, `CHAOS_PLAN` |
| Attack hypothesis | `src/cortex_ascend/kernel/adversarial.py` | `AttackHypothesis` with target invariant and dedup fingerprint |
| Sealed holdout suite | `src/cortex_ascend/kernel/adversarial.py` | `HoldoutItem` + `HoldoutSuite`; public metadata only |
| Chaos fault | `src/cortex_ascend/kernel/adversarial.py` | `ChaosFault` with schedule, target invariant, expected outcome |
| Red-team receipt | `src/cortex_ascend/kernel/adversarial.py` | `RedTeamReceipt` linking seat, hypothesis, and harness result |
| Tests | `tests/unit/test_kernel_adversarial.py` | 5 tests covering identity, dedup, holdout fingerprint, chaos, receipts |

## Invariants supported

- **ASC-INV-ADV-001**: model agreement is never a pass oracle — receipts record
  seat identity and deterministic harness results, not consensus.
- **ASC-INV-TRUST-001**: holdout metadata in the public repo contains no
  answers; actual material is verifier-controlled.

## Gaps requiring model/runtime integration

| Requirement | Status |
|-------------|--------|
| Qwen repeated repository review | Requires transport integration and sanitized fixtures. |
| VibeThinker-3B benchmark | Requires model access and benchmark corpus. |
| Dedup/novelty pipeline | Requires model output normalization; fingerprint field reserved. |
| Private verifier-controlled sealed holdout store | Requires encrypted storage and access controls. |
| Declared chaos fault schedules executed by deterministic harnesses | Requires harness wiring; `ChaosFault` structure defined. |
| Cross-vendor seat gating (issue #28) | Requires multi-vendor transport setup. |

## Exit criteria status

| Criterion | Status |
|-----------|--------|
| Model agreement is never used as a pass oracle | Partial — receipt structure supports this; execution pipeline pending. |
| Holdout cases/answers not retrievable by worker roles | Partial — metadata-only in repo; actual store pending. |
| Semantic mutants and chaos schedules executed by deterministic harnesses | Partial — structures defined; harness integration pending. |
| Stale-generation/retry corpus survives adversarial and chaos cases | Pending — requires harness integration. |
| VibeThinker benchmark-justified or removed | Pending — requires model access. |

## Recommendation
G6-G7 is **policy-structure complete** but **model/runtime integration incomplete**.
The next block should either provision multi-vendor model access and a sealed
holdout store, or explicitly defer those components.

## Next phase
- Gate: G8-G10 — Shadow Ascend admission, promote required gate, then integrate real FOSSIL lineage.
- Issue: #6

## Related work
- Parent: #5
- Depends on: #3, #4
- Related: #28 (cross-vendor seat gating)
