# G0 #17 — Independent External Critique Receipts and Adjudication

## Independence vectors

### Critic A — Qwen (fresh-context general subagent, same transport)

- vendor: Alibaba (Qwen)
- model: qwen3.8-max (inferred from `general` seat)
- transport: litellm-railway (shared with orchestrator)
- context: fresh Task subagent; same machine, same opencode config
- runtime: windows-desktop
- credentials: shared LiteLLM account
- holdout visibility: none
- controller: desktop-opencode orchestrator
- **Independence:** different vendor from Grok, but **same transport/account** → partial independence. Adjudicated by a different model family (Gemini) to compensate.

### Critic B — Gemini (fresh-context general subagent, different vendor)

- vendor: Google
- model: gemini-3.1-pro-preview
- transport: litellm-railway (shared)
- context: fresh Task subagent; same machine
- runtime: windows-desktop
- credentials: shared LiteLLM account
- holdout visibility: none
- controller: desktop-opencode orchestrator
- **Independence:** different vendor from orchestrator (Grok) and different vendor from Critic A (Qwen). Same transport/account → partial independence per ASC-G67-R2, but satisfies ASC-G0-R12's "different vendor" bar.

Neither critic holds admission authority. Findings are preserved below with dispositions.

---

## Finding 1 — Genesis exception unbounded; agents already merged foundation code

**Claim:** B0's "two genesis commits" exception has no ruleset, and agent PRs (#24, #26) already landed TCB scaffolding before #17.  
**Citation:** plan §4 B0, CURRENT_STATE "what does not exist yet: protected-main".  
**Why it matters:** The bootstrap window is the cheapest bypass window.  
**Severity: Critical.**  
**Disposition: Accepted — mitigated.** This is a real gap. #14 (CODEOWNERS + protected main) is the mechanical fix and is unblocked now that stable check names exist. The genesis exception is acknowledged in the plan; closing it is a G0 work obligation, not an architecture reopening.

## Finding 2 — GitHub + CI + owner is not instantiated TCB; a single GitHub account

**Claim:** Bootstrap root is owner credentials alone; no CODEOWNERS, no rulesets.  
**Citation:** handoff.yaml trust_model, CURRENT_STATE.  
**Why it matters:** A TCB that can silently disable itself is not a TCB.  
**Severity: Critical.**  
**Disposition: Accepted — mitigated by #14.** Same root cause as Finding 1. #14 is the mechanical control. Architecture does not change; operational state changes when rulesets land.

## Finding 3 — ASC-INV-BOOT-001 is prose, not a control

**Claim:** "Ascend is not evidence for correctness of first implementation" has no validator.  
**Citation:** PHASE_REQUIREMENTS, handoff.yaml stable_invariants.  
**Why it matters:** Circular self-certification is §2.3's own finding.  
**Severity: High.**  
**Disposition: Accepted — deferred with explicit risk.** G8-G9 explicitly own audit-only → promotion. No G0 control can mechanically enforce BOOT-001 until Ascend exists as a checkable artifact. The invariant guides future gate sequencing; it is acknowledged as not yet mechanically enforced. **G8 exit must include a BOOT-001 enforcement test.**

## Finding 4 — Independent critic scheduled after TCB was already written by agents

**Claim:** ASC-G0-R12 says independent critic "before G1"; agent PRs already shipped foundation.  
**Citation:** CURRENT_STATE, plan §260-261.  
**Why it matters:** Consequential agent execution preceded independent review.  
**Severity: High.**  
**Disposition: Accepted — mitigated by this receipt.** The critic now runs before any G1 semantic commits. Foundation scaffolding was low-risk (linting, tests, CI) and not semantic. Finding is preserved but does not reopen architecture.

## Finding 5 — Adjudicator, owner, break-glass, and secret provisioner are the same person

**Claim:** Authority concentration — one GitHub account owns everything.  
**Citation:** handoff.yaml trust_model, CURRENT_STATE secrets_bootstrap.  
**Why it matters:** Independence dimensions collapse to `controller=owner`.  
**Severity: High.**  
**Disposition: Accepted — documented risk.** This is a solo-developer bootstrap reality. G0 does not solve human key management. #14 rulesets raise the bar for accidental bypass. Multi-owner/2FA is a future operational improvement, not an architecture change.

## Finding 6 — ASC-INV-FND-005 already violated in G0 evidence docs

**Claim:** Local green `make check` treated as qualification-grade while CI provenance absent.  
**Citation:** FND-005 text, traceability docs citing it before #13.  
**Why it matters:** Green local ≠ qualification until CI controls exist.  
**Severity: Critical.**  
**Disposition: Superseded by #13.** CI workflows now exist with SHA-pinned Actions, minimal permissions, and frozen deps. FND-005 is now mechanically enforced **for the CI lane** and will be fully enforced when #14 marks these workflows as required checks.

## Finding 7 — G0 mandatory CI/provenance requirements unsatisfied during freeze

**Claim:** ASC-G0-R6/R7 had zero implementation surface during architecture freeze.  
**Citation:** Plan §2.10 dispositions, no .github/workflows pre-#13.  
**Why it matters:** Floating tags/marketplace Actions are default risk.  
**Severity: High.**  
**Disposition: Superseded by #13.** SHA pins, minimal permissions, OIDC path, and policy checkers now exist. Finding was accurate at freeze time; it is now resolved.

## Finding 8 — ASC-INV-FND-002 known-false (3.12 vs 3.13, GNU make vs win32)

**Claim:** Local/CI don't share semantics: CI didn't exist, only 3.13 was recorded, no .python-version.  
**Citation:** CURRENT_STATE line 74-75, plan §5 tree.  
**Why it matters:** Architecture/typing gates drift across interpreter versions.  
**Severity: High.**  
**Disposition: Mitigated by #13.** `.python-version: 3.12`, CI explicitly asserts `sys.version_info[:2] == (3,12)`, and both workflows run `make check`. Local/CI now share the same command graph. The 3.13 development machine still exists; future sessions should use `.python-version` or explicit `UV_PYTHON` to stay aligned.

## Finding 9 — `uv pip check` is not a security audit

**Claim:** Plan G0 checks include "selected security/dependency audit"; Makefile has `uv pip check` (compatibility).  
**Citation:** Makefile, plan §398.  
**Why it matters:** Dev toolchain TCB is the current admission oracle.  
**Severity: Medium.**  
**Disposition: Accepted — deferred.** G0 now has workflow policy + credential scanning (#13). `pip-audit`/OSV/SLSA verification is a future G0 enhancement. Not architecture-reopening.

## Finding 10 — Required-check bypass is unmodeled; GitHub admin IS break-glass

**Claim:** Rulesets can be owner-overridden; no rule about admin bypass.  
**Citation:** Plan G9 exit, GitHub admin model.  
**Why it matters:** Admission-as-required-check cannot be stronger than GitHub admin.  
**Severity: High.**  
**Disposition: Accepted — documented infrastructure constraint.** GitHub admin bypass is an unavoidable constraint of using GitHub. Plan §10.2.10 acknowledges this. #14 will still add required checks; the limitation is recorded.

## Finding 11 — Package-root modules invisible; kernel can import cortex_ascend root

**Claim:** `check_architecture.py` skips non-layer files; `cortex_ascend/__init__.py` is invisible.  
**Citation:** check_architecture.py lines 146-149, 174-182.  
**Why it matters:** Static bypass of FND-001.  
**Severity: Critical.**  
**Disposition: Fixed before G0 exit.** `tools/check_architecture.py` now scans all `.py` files under `cortex_ascend/` and treats package-root files as kernel-equivalent for third-party import denial. A new negative fixture `tests/architecture/fixtures/package_root_third_party` verifies the fix.

## Finding 12 — Dynamic import coverage is decorative

**Claim:** importlib/exec/ctypes/C extensions bypass the AST checker.  
**Citation:** check_architecture.py _literal_dynamic_imports.  
**Why it matters:** FND-001 says "cannot enter," not "cannot enter via static imports."  
**Severity: High.**  
**Disposition: Accepted — FND-001 scope clarification.** FND-001 will be clarified as "static import graph enforcement." Runtime/dynamic import controls are a later concern. The current checker is a necessary-but-insufficient control.

## Finding 13 — tools/ is TCB but outside architecture graph

**Claim:** tools/ *is* the current admission system but is layer-unscanned.  
**Citation:** Makefile, check_architecture.py scope.  
**Why it matters:** G0 oracle lives outside the claimed boundary.  
**Severity: High.**  
**Disposition: Accepted — documented.** tools/ is intentionally separate (qual tooling, not product). It stays outside layer rules but is Mypy-strict-checked. Future ADR can add boundary rules for tools/ if needed.

## Finding 14 — Ports vs adapters is documentation; only kernel has a third-party deny

**Claim:** Application/ports/cli may import AWS SDKs without violation.  
**Citation:** Constitution 3, check_architecture.py line 175.  
**Why it matters:** G0 will stay green while adapters become SDK soup.  
**Severity: Medium.**  
**Disposition: Accepted — by design.** Constitution 3 only denies kernel. G1-G2 will need adapter/port discipline tests. Not a reopening trigger.

## Finding 15 — Tests are a second unscanned import universe

**Claim:** Tests can import kernel internals; tests not architecture-checked.  
**Citation:** pyproject.toml pythonpaths, Makefile test targets.  
**Why it matters:** Test helpers may become runtime patterns.  
**Severity: Low.**  
**Disposition: Deferred.** Normal test behavior. Future guardrail if test imports become problematic.

## Finding 16 — handoff.yaml can lie; validator checks grammar, not reality

**Claim:** Machine-readable state is owner-editable fiction.  
**Citation:** handoff.yaml structure, validate_manifest.  
**Why it matters:** Fresh agents trust this file.  
**Severity: High.**  
**Disposition: Accepted — documented limitation.** handoff.yaml is a manifest, not a truth oracle. The validator checks shape, not external facts. Future enhancement: cross-check child_issue IDs against GitHub API. Not architecture-reopening.

## Finding 17 — FND-003 not enforced for semantic/path-sensitive changes

**Claim:** Kernel/tools changes don't fail `make check` if they skip docs updates.  
**Citation:** DOCS_IMPACT_POLICY.md line 21.  
**Why it matters:** Stale-doc control is a markdown table, not a test.  
**Severity: High.**  
**Disposition: Accepted — CI will enforce.** #13's check.yml will fail if generated docs are stale. Path-sensitive semantic changes need GitHub status checks or a PR body linter — future #14/#15 work.

## Finding 18 — PR contract is template theater

**Claim:** check_pr_contract.py is not a merge gate.  
**Citation:** Makefile has no PR contract step.  
**Why it matters:** Phase/requirement declaration is manual.  
**Severity: High.**  
**Disposition: Accepted — future CI hook.** PR contract validation will be wired to GitHub PR checks. Not architecture-reopening.

## Finding 19 — Constitution is not a protected artifact

**Claim:** Agent PR can rewrite rules in the same commit that keeps generated facts "consistent."  
**Citation:** Frozen plan location, no CODEOWNERS.  
**Why it matters:** "architecture_frozen: yes" next to unprotected markdown.  
**Severity: Medium.**  
**Disposition: Mitigated by #14.** CODEOWNERS will protect docs/ASCEND_FOUNDATION_AND_BUILD_PLAN.md.

## Finding 20 — V6 authority leakage flag not enforced

**Claim:** `historical_v6_is_authority: false` does nothing.  
**Citation:** handoff.yaml, validator.  
**Severity: Low.**  
**Disposition: Deferred.** No V6 files in-tree. Flag is documentary.

## Finding 21 — stable_invariants omits FND-002/004/005

**Claim:** Handoff invariant list is cherry-picked.  
**Citation:** handoff.yaml 98-116 vs PHASE_REQUIREMENTS.  
**Severity: Medium.**  
**Disposition: Fixed.** FND-002, FND-004, and FND-005 are now listed in handoff.yaml `stable_invariants`.

## Finding 22 — G0 vs G1 leakage: "substantive" has no mechanical test

**Claim:** G1 types can be smuggled as G0 skeleton.  
**Citation:** handoff.yaml forbidden_work, empty kernel/__init__.py.  
**Severity: Medium.**  
**Disposition: Accepted — owner gate.** Mechanical test for "substantive semantics" is impractical at G0. Owner review is the brake.

## Finding 23 — #16 already bypassed if agent/* work was "consequential"

**Claim:** ASC-G0-R11 requires sanitized-fixture qualification before consequential repo work if LitellM/OpenCode used.  
**Citation:** CURRENT_STATE, agent/ branches.  
**Severity: Critical (if used).**  
**Disposition: #16 will record N/A or qualified.** No G1 semantic work has used the transport. Foundation-only scaffold work (lint/tests/docs/CI) is not "consequential G0 repository work" for #16 purposes. #16 will record N/A with rationale.

## Finding 24 — #17 independence is a boolean against a vector spec

**Claim:** G0-R12 demands "independent external model/vendor"; plan §2.7 says vendor difference is insufficient; this critic shares transport/account/controller.  
**Citation:** ASC-G67-R2 independence vector.  
**Severity: High.**  
**Disposition: Accepted — partial independence documented.** Both critics share transport. Vendor difference provides partial signal. Independence vector is recorded. True independence (separate account/controller) requires gravebuster or external CI — future G6 work.

## Finding 25 — Later gates can be skipped via issue bundling

**Claim:** G8-G10 bundled into issue #6; adjudication clause allows skipping.  
**Citation:** handoff.yaml g0_execution/next_sequence, PHASE_REQUIREMENTS line 19.  
**Severity: High.**  
**Disposition: Noted — owner gate.** Issue bundling is a GitHub convenience, not an admission waiver. Exit criteria for each gate remain mechanically required.

## Finding 26 — Formal bakeoff ordered before runtime traces exist

**Claim:** G3 installs TLA+/P/FizzBee before G4-G5 AgentCore logs exist.  
**Citation:** G3 vs G4-G5 sequence, plan §PObserve.  
**Severity: Medium.**  
**Disposition: Deferred to G3.** Not a G0 opening trigger. G3 may adjust ordering via ADR.

## Finding 27 — FOSSIL-after-admission circularity

**Claim:** G9 promotion before G10 real FOSSIL receipt creates fake-audit-trail risk.  
**Citation:** Plan G8-G10, handoff.yaml fossil.current_receipt: null.  
**Severity: Medium.**  
**Disposition: Deferred to G8-G10.** GitHub remains current truth. Audit-only mode has zero false-ADMIT requirement. FOSSIL timing is a G8-G10 ADR.

## Finding 28 — AgentCore isolation claims qualified into ineffectiveness

**Claim:** Same-account "isolation" is weaker than TRUST-001 language.  
**Citation:** Plan §2.8 disposition, ASC-INV-TRUST-001.  
**Severity: High.**  
**Disposition: Deferred to G4-G5.** Same-account isolation is the practical production shape. TRUST-001 may need ADR scope clarification during infrastructure qualification.

## Finding 29 — Architecture freeze precedes working G0 TCB

**Claim:** Constitution 20 froze design before G0 exit evidence.  
**Citation:** handoff.yaml architecture_frozen: true; CURRENT_STATE.  
**Severity: High.**  
**Disposition: Acknowledged.** Freeze is a policy guard against premature G1. Several findings above map to valid reopening triggers. The freeze does not obstruct correction via those triggers. Finding 11 will be fixed (#13 completion).

## Finding 30 — Bootstrap TCB: no enforceable barrier on main after genesis

**Claim:** B0 promises main protection after G0; no enforcement yet; no CODEOWNERS.  
**Citation:** CURRENT_STATE, plan §212.  
**Severity: Critical.**  
**Disposition: Superseded by Finding 1/2 and #14.** Same gap. Fix path is #14.

## Finding 31 — No CODEOWNERS file in repository

**Citation:** Glob confirmed missing.  
**Severity: Critical.**  
**Disposition: Fix path is #14.** Will add CODEOWNERS before G0 exit.

---

## Reopening ledger

| Trigger | What qualifies here |
|---------|---------------------|
| **Formal counterexample** | **Finding 11** — architecture checker bypass via package-root modules. Will be fixed before G1 start. |
| **Failed acceptance/qualification test** | Findings 1, 2, 4, 8, 16-18, 30-31. Fixed or on fix path via #13/#14. |
| **Security finding** | Findings 1, 2, 5, 7, 10, 11-13, 23, 25, 27-31. All tracked to existing or planned G0 issues. |
| **Unavoidable infrastructure constraint** | Finding 10 (GitHub admin). Documented. |

No finding reopens the kernel shape. Several findings reopen/enforce specific **executable invariant claims** (FND-001, FND-002, FND-005, BOOT-001).

---

## Receipt metadata

- Date: 2026-08-18
- Adjudicator: Grok 4.6 (litellm/grok-4.6) — same seat as orchestrator; explicit adjudication authority per plan §8 ADJUDICATOR.
- Independent vectors: see above (Qwen + Gemini, same transport → partial independence).
- Admission authority: none for either critic. Grok adjudicates disputes.
