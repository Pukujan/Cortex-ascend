# G0.12 — G0 Exit Evidence and Foundation Gate Closure

## Scope
Assemble and mechanically verify the complete G0 evidence set required to close
issue #1 and authorize advancement to G1-G2.

## Exit checklist

| # | Required evidence | Location / command | Status |
|---|-------------------|--------------------|--------|
| 1 | Reproducible green `make check` from a clean checkout | `make check` | PASS |
| 2 | Expected-failure receipts for deliberate negative fixtures | `tests/ci/negative_receipt.yaml` | PASS |
| 3 | Mechanically re-read protected-main state | `gh api repos/Pukujan/Cortex-ascend/branches/main/protection` | PASS |
| 4 | Credential/history scan evidence | `tools/check_secrets.py` | PASS |
| 5 | Fresh-session handoff reconstructs state | `docs/HANDOFF.md`, `docs/CURRENT_STATE.md` | PASS |
| 6 | Independent critic receipt with adjudication | `docs/traceability/G0_17_INDEPENDENT_CRITIQUE_RECEIPT.md` | PASS |
| 7 | Requirement/invariant traceability matrix | `docs/traceability/G0_9_NEGATIVE_QUALIFICATION.md` | PASS |
| 8 | Bootstrap transport qualified or N/A | `docs/traceability/G0_10_TRANSPORT_QUALIFICATION.md` | N/A with rationale |

## Mechanical verification output

```text
$ make check
...all gates green...
architecture negative fixtures: OK (4 expected failures)
static negative fixtures: OK (2 expected failures)
test negative fixtures: OK (2 expected failures)
documentation negative fixtures: OK (3 expected failures)
github workflow negative fixtures: OK (4 expected failures)
secret negative fixtures: OK (1 expected failure)
```

## Protected-main state (re-read)

```json
{
  "allow_deletions": false,
  "allow_force_pushes": false,
  "contexts": ["check", "security-provenance"],
  "required_approving_review_count": 0,
  "strict": true
}
```

## Known residual risks accepted at G0 exit

| Risk | Mitigation / why acceptable |
|------|----------------------------|
| GitHub admin is break-glass | Documented infrastructure constraint; rulesets still raise accidental-bypass bar. |
| Single owner holds all roles | Solo-developer bootstrap reality; future operational improvement. |
| FND-001 is static-only | Scope clarified; runtime import controls are later work. |
| BOOT-001 not mechanically enforced | Deferred to G8-G9 audit-only promotion path. |
| Partial independence of critics | Different vendors used; full account/controller separation is G6 work. |

## Reopening ledger resolved during G0

- **Finding 11** from `docs/traceability/G0_17_INDEPENDENT_CRITIQUE_RECEIPT.md`
  (package-root modules bypassing `check_architecture.py`) is now fixed.
  `tools/check_architecture.py` scans all files under `cortex_ascend/` and
  treats package-root files as kernel-equivalent for third-party import denial.
  A new negative fixture verifies the fix.

## Gate-closing adjudication

- All G0 child issues (#7 through #18) are completed or explicitly dispositioned.
- Architecture remains frozen.
- No G1 semantics have been introduced.
- The repository is authorized to advance to G1-G2 work as defined in issue #2.

## Next phase
- Gate: G1-G2
- Issue: #2
- Authorized work: substantive AgentCore/kernel foundation types and bounded
  autonomous execution harnesses, per `docs/PHASE_REQUIREMENTS_AND_INVARIANTS.md`.

## Receipt metadata
- Date: 2026-08-19
- Adjudicator: repository owner / orchestrator
- Admission authority: none for Ascend itself; this is a human/bootstrap gate closure.
