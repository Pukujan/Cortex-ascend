# G4-G5 — Model Lanes and Worker/Verifier Trust Domains

## Scope
Qualify the real model transport and AWS execution path without granting
model/runtime components semantic authority, per issue #4.

## Delivered (kernel-side policy)

| Deliverable | File | Notes |
|-------------|------|-------|
| Model lane policy | `src/cortex_ascend/kernel/trust.py` | `ModelLanePolicy`, `FallbackPolicy`, requested/actual model checks |
| Runtime profiles | `src/cortex_ascend/kernel/trust.py` | `RuntimeProfile`, `WORKER_PROFILE`, `VERIFIER_PROFILE`, `READONLY_PROFILE` |
| Egress policy | `src/cortex_ascend/kernel/trust.py` | `EgressPolicy` enum |
| Trust domain tests | `tests/unit/test_kernel_trust.py` | 5 tests for fallback, egress, and profile separation |

## Kernel-side invariants enforced

- **Cross-model fallback is off by default** (`FallbackPolicy.DENY`).
- **Exact requested/actual model identity** is checkable via `ModelLanePolicy.permits_actual`.
- **Worker cannot access verifier secrets**: `WORKER_PROFILE.can_access_verifier_secrets == False`.
- **Verifier can access verifier secrets**: `VERIFIER_PROFILE.can_access_verifier_secrets == True`.
- **Worker has read-only egress** and cannot mutate repository.

## Infrastructure gaps (require AWS/GitHub/credential setup)

The following G4-G5 exit items are **not implemented** in this changeset because
they require cloud infrastructure and credentials not available in this session:

| Requirement | Why blocked |
|-------------|-------------|
| GitHub Actions -> AWS via OIDC | Requires AWS account + IAM identity provider configuration. |
| Separate worker/verifier IAM roles/sessions | Requires AWS IAM role creation and trust policy. |
| Least-privilege IAM policies | Requires AWS account and resource ARNs. |
| Immutable candidate artifact handoff to verifier | Requires artifact store (e.g., S3 + signed URLs). |
| Verifier independently reruns checks against exact artifact digest | Requires runner isolation and artifact store. |
| Pinned OpenCode config/version on sanitized fixtures | Requires reproducible OpenCode installation and fixture harness. |
| Qwen direct/API seat qualification | Requires API credentials and sanitized fixture design. |

## Exit criteria status

| Exit criterion | Status |
|----------------|--------|
| Transport timeout/fallback cannot masquerade as model capability evidence | Partial — kernel policy exists; transport integration pending. |
| Unexpected actual-model substitution invalidates evidence | Partial — `ModelLanePolicy` supports this; wiring to evidence validation pending. |
| Worker compromise does not grant sealed verifier material | Partial — runtime profiles enforce this in policy; actual IAM isolation pending. |
| Verifier does not trust worker-local "tests passed" claims | Partial — verifier profile is defined; independent rerun infrastructure pending. |

## Recommendation
G4-G5 should be considered **kernel-policy complete** but **infrastructure incomplete**.
The next work block should either (a) provision AWS/GitHub OIDC and IAM, or (b)
record an explicit decision to defer operational qualification until a later
phase.

## Next phase
- Gate: G6-G7 — Add adversarial inference, specialist counterexample search, sealed holdout, and chaos.
- Issue: #5

## Related work
- Parent: #4
- Depends on: #1, #2, #3
