# G8-G10 — Shadow Ascend Admission, Gate Promotion, and FOSSIL Lineage

## Scope
Promote Ascend from externally qualified audit logic to a required semantic
admission gate without self-certification, per issue #6.

## Delivered (kernel-side audit/promotion/FOSSIL structures)

| Deliverable | File | Notes |
|-------------|------|-------|
| Audit mode | `src/cortex_ascend/kernel/promotion.py` | `AuditCase`, `AuditResult`, `AuditOutcome` |
| Audit runner | `src/cortex_ascend/kernel/promotion.py` | `audit`, `audit_corpus`, `any_false_admit` |
| Gate promotion policy | `src/cortex_ascend/kernel/promotion.py` | `GateMode`, `GatePolicy` with break-glass and promotion threshold |
| FOSSIL receipt | `src/cortex_ascend/kernel/promotion.py` | `FossilReceipt` placeholder with real/verified flag |
| Tests | `tests/unit/test_kernel_promotion.py` | 6 tests covering match, stale, mismatch, corpus, promotion, FOSSIL |

## Audit-mode behavior

- `AuditCase` binds a `WorkContract`, current `ProjectSnapshot`, externally
  expected `Decision`, and a category (positive, stale, model-mismatch, etc.).
- `audit()` runs `adjudicate_against_base` and compares to the expected decision.
- `AuditOutcome.FALSE_ADMIT` is the critical failure class for promotion.
- `GatePolicy.can_promote()` requires zero false admits in audit mode before
  promoting Ascend to a required gate.

## Seeded cases covered

| Category | Test |
|----------|------|
| Valid positive | `test_audit_match_for_valid_contract` |
| Stale base | `test_audit_false_admit_for_stale_contract` |
| Model mismatch | `test_audit_false_admit_for_model_mismatch` |
| Corpus no false admit | `test_corpus_detects_false_admit` |
| Promotion blocked on false admit | `test_gate_policy_blocks_promotion_with_false_admits` |

## Gaps

| Requirement | Status |
|-------------|--------|
| Real qualification corpus fed into Ascend | Partial — corpus structure exists; real PR/CI data integration pending. |
| Ascend as a protected required GitHub check | Pending — requires GitHub App/Action integration. |
| Break-glass policy auditable in GitHub | Pending — policy structure exists; enforcement via GitHub audit log pending. |
| Automatic current-state/handoff updates after admitted changes | Pending — requires bot/Action integration. |
| Real FOSSIL integration | Pending — `FossilReceipt.verified` remains `False` until real lineage write. |
| Ascend operational without FOSSIL | Supported — FOSSIL is not a runtime dependency. |

## Exit criteria status

| Criterion | Status |
|-----------|--------|
| Ascend is not its own bootstrap proof | Enforced — external evidence is required for every contract. |
| Required gate rejects stale/unauthorized/mismatched artifacts in covered cases | Partial — kernel logic ready; GitHub check wiring pending. |
| Current GitHub state and generated handoff agree | Verified by `tools/check_docs.py`. |
| No Markdown/manual JSON is described as a FOSSIL write | `FossilReceipt` explicitly distinguishes real vs placeholder. |

## Recommendation
G8-G10 is **kernel policy complete** but **integration incomplete**. The
remaining work is operational: wire Ascend into GitHub checks, build the real
audit corpus runner, and connect to FOSSIL at the validate/authorize/commit
boundary.

## Related work
- Parent: #6
- Depends on: #2, #3, #4, #5
