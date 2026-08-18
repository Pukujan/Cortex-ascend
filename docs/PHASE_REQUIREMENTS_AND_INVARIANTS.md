# Cortex Ascend — Phase Requirements and Invariants

**Status:** Frozen planning contract for implementation sequencing  
**Decision:** `REVISE -> START G0 ONLY`  
**Authority:** subordinate to `docs/ASCEND_FOUNDATION_AND_BUILD_PLAN.md`; this file operationalizes that plan into phase entry criteria, requirements, invariants, evidence, and exit criteria.

## How to use this file

Every implementation issue/PR must declare:

- phase;
- requirement IDs implemented;
- invariant IDs affected;
- exact acceptance evidence;
- documentation/handoff impact;
- whether the change crosses a trust or architecture boundary.

A later phase cannot be treated as authorized merely because its issue exists. Its entry criteria must be satisfied mechanically or explicitly adjudicated.

---

## G0 — Foundation and bootstrap qualification

### Goal
Create a repository and CI foundation that rejects structurally unsafe work before Cortex semantics exist.

### Requirements

- `ASC-G0-R1` — Python 3.12+ project using `uv`, `src/` layout, and committed lockfile.
- `ASC-G0-R2` — Ruff format/lint and strict Mypy run from one reproducible local/CI command.
- `ASC-G0-R3` — Pytest and Hypothesis available from the first semantic commit.
- `ASC-G0-R4` — Import Linter or equivalent mechanically enforces `adapters -> application -> kernel` dependency direction.
- `ASC-G0-R5` — Kernel dependency allowlist forbids AWS, AgentCore, LiteLLM, OpenCode, FOSSIL, GitHub, graph, orchestration, and model SDK dependencies.
- `ASC-G0-R6` — CI uses locked dependencies, pinned third-party Actions by immutable commit SHA, minimum permissions, and reproducible checks.
- `ASC-G0-R7` — GitHub OIDC is the future AWS credential path; long-lived AWS keys are not required for normal CI.
- `ASC-G0-R8` — Protected-main/ruleset and required checks are enabled after genesis bootstrap.
- `ASC-G0-R9` — `handoff.yaml`, `docs/HANDOFF.md`, `docs/CURRENT_STATE.md`, and ADR structure exist; semantic changes have a docs-impact disposition.
- `ASC-G0-R10` — Deliberate negative fixtures prove bad imports, type failures, architecture cycles, stale generated docs, and seeded broken invariants fail qualification.
- `ASC-G0-R11` — OpenCode/LiteLLM bootstrap use, if used during G0, is qualified only on sanitized fixtures before consequential repo work.
- `ASC-G0-R12` — At least one genuinely independent external model/vendor critic re-attacks the frozen plan before G1 consequential kernel work.

### Invariants

- `ASC-INV-FND-001` — No prohibited infrastructure dependency can enter `kernel` while required checks are green.
- `ASC-INV-FND-002` — A local `make check` (or single equivalent command) and CI execute the same qualification semantics.
- `ASC-INV-FND-003` — A semantic change cannot be merge-complete while mandatory current-state/handoff documentation is stale.
- `ASC-INV-FND-004` — No credential value is committed to repository history.
- `ASC-INV-FND-005` — Green CI is not called qualification-grade evidence unless the CI/provenance controls required by G0 are active.

### Exit evidence

- reproducible green `make check`;
- expected failure receipts for deliberately broken fixtures;
- mechanically re-read protected-main/ruleset status;
- fresh-session handoff successfully reconstructs current state;
- independent critic receipt and adjudicated disagreements.

### Forbidden during G0

- substantive semantic kernel implementation;
- AgentCore production execution;
- broad autonomous repository mutation;
- Spec IR language design;
- FOSSIL claims without a real canonical receipt.

---

## G1–G2 — Pure semantic kernel and minimal WorkContract IR

### Goal
Implement the smallest portable semantics for work identity, authority, freshness, evidence binding, model identity, and admission.

### Requirements

- `ASC-G12-R1` — Immutable types: `ProjectSnapshot`, `WorkId`, `Generation`, `ArtifactDigest`, `AuthorityGrant`, `ModelIdentity`, `EvidenceReceipt`, `AdmissionDecision`.
- `ASC-G12-R2` — Decisions are exactly `ADMIT`, `REJECT`, `STALE`, `BLOCKED` unless constitutionally revised.
- `ASC-G12-R3` — `WorkContract` v1 is canonical, machine-readable, hashable, and bounded; it is not declared truth.
- `ASC-G12-R4` — Requested and actual model identity are separate fields.
- `ASC-G12-R5` — Evidence receipts bind exact work/project/generation/artifact/verifier/tool identities.
- `ASC-G12-R6` — Freshness, authority, evidence sufficiency, and model-identity compatibility are pure predicates.
- `ASC-G12-R7` — Property tests and selected mutation tests target high-value guards.

### Invariants

- `ASC-INV-KRN-001` — A stale project base or generation cannot satisfy current-work evidence requirements.
- `ASC-INV-KRN-002` — Invalid/revoked/expired authority cannot authorize a new consequential effect.
- `ASC-INV-KRN-003` — Evidence for artifact A cannot admit artifact B.
- `ASC-INV-KRN-004` — Unauthorized requested/actual model substitution invalidates evidence for an exact-model seat.
- `ASC-INV-KRN-005` — A worker-local claim that a check passed is not qualification evidence by itself.

### Exit evidence

- unit/property/mutation evidence;
- canonical hash stability/change tests;
- architecture contracts still green;
- no infrastructure SDK dependency in kernel.

---

## G3 — Distributed lifecycle formalization

### Goal
Prove and empirically test the first consequential lifecycle invariant: stale generations cannot be admitted.

### Requirements

- `ASC-G3-R1` — One bounded lifecycle model covers generation replacement, retry, duplicate/replay, revocation, verifier crash, and crash-after-effect-before-ack.
- `ASC-G3-R2` — Compare TLA+/TLC, P/P-Checker, and FizzBee on the same problem.
- `ASC-G3-R3` — Select one primary distributed formalism by ADR using counterexample quality, CI reproducibility, implementation-conformance path, toolchain burden, and maintainability.
- `ASC-G3-R4` — Map formal properties/transitions to executable code/tests.

### Invariants

- `ASC-INV-DST-001` — No result from generation `g < authoritative_generation` may become `ADMIT`.
- `ASC-INV-DST-002` — Duplicate/replayed delivery cannot create a second semantically distinct admission/effect for the same idempotent effect identity.
- `ASC-INV-DST-003` — Evidence produced before a superseding state transition is re-evaluated for freshness at admission time.
- `ASC-INV-DST-004` — Formal pass claims are explicitly scoped to the model and assumptions; implementation conformance is a separate obligation.

### Lean / Z3 rule

Lean is not mandatory here. It enters only if a theorem-shaped pure-kernel obligation cannot be adequately covered by the selected distributed formalism plus executable/property/symbolic tests. Z3/symbolic tools may be used narrowly for small constraints.

---

## G4–G5 — Model transport and AgentCore trust separation

### Goal
Qualify real inference and isolated execution without granting transport/runtime semantic authority.

### Requirements

- `ASC-G45-R1` — Pinned OpenCode build/config on sanitized fixtures.
- `ASC-G45-R2` — LiteLLM/direct-provider path preserves exact requested/actual model identity.
- `ASC-G45-R3` — Cross-model fallback is off by default; semantic switching belongs to Ascend seating policy.
- `ASC-G45-R4` — Qualified Qwen API seat.
- `ASC-G45-R5` — Worker and verifier use separate AgentCore roles/sessions/trust domains.
- `ASC-G45-R6` — Worker cannot read verifier/holdout credentials or sealed material.
- `ASC-G45-R7` — Verifier re-runs required checks against the exact immutable candidate digest.

### Invariants

- `ASC-INV-MDL-001` — Transport timeout/fallback cannot be recorded as a model-capability success/failure without preserving actual route/model/termination identity.
- `ASC-INV-MDL-002` — Unexpected actual-model substitution cannot satisfy an exact-model seat.
- `ASC-INV-TRUST-001` — Worker compromise does not grant sealed verifier/holdout access.
- `ASC-INV-TRUST-002` — Worker-local pass claims cannot directly become independent qualification receipts.

---

## G6–G7 — Adversarial inference, VibeThinker, hidden holdout, mutation, chaos

### Goal
Use abundant heterogeneous inference to search failure space while keeping adjudication grounded in independent/mechanical oracles.

### Requirements

- `ASC-G67-R1` — Seats include at least `RED_ARCH`, `RED_SEC`, `RED_DIST`, `MUTANT`, `FORMAL_ADV`, and `CHAOS_PLAN`.
- `ASC-G67-R2` — Independence is recorded as a vector: vendor, model, provider/account, transport, context, runtime, credentials, holdout visibility, controller.
- `ASC-G67-R3` — Qwen can be scaled for repository review, test generation, semantic mutants, and distributed failure search.
- `ASC-G67-R4` — VibeThinker-3B is benchmarked only as a narrow mathematical/formal/counterexample specialist after deterministic targets exist.
- `ASC-G67-R5` — Model outputs are deduplicated and converted into executable attack hypotheses rather than votes.
- `ASC-G67-R6` — Sealed holdout cases/answers live outside this public repository and outside worker-readable credentials.
- `ASC-G67-R7` — Chaos experiments declare fault, invariant, expected result, and evidence collection before injection.

### Invariants

- `ASC-INV-ADV-001` — Model agreement is never a pass oracle.
- `ASC-INV-ADV-002` — Holdout leakage invalidates the affected qualification claim.
- `ASC-INV-ADV-003` — Semantic mutants are judged by whether executable assurance kills them, not whether another model dislikes them.
- `ASC-INV-CHAOS-001` — Chaos cannot be called assurance unless the tested invariant and expected outcome were declared before the fault was injected.
- `ASC-INV-VIBE-001` — VibeThinker remains only if it contributes unique reproducible counterexamples beyond the baseline ensemble; otherwise remove it.

---

## G8–G9 — Audit-only self-hosting, then required admission

### Goal
Allow Ascend to earn authority without circular self-certification.

### Requirements

- `ASC-G89-R1` — Ascend first consumes immutable fixtures/real receipts in audit-only mode.
- `ASC-G89-R2` — Expected decisions are established externally for the qualification corpus.
- `ASC-G89-R3` — Seed stale, revocation, replay, artifact substitution, model mismatch, retry, and mutant cases.
- `ASC-G89-R4` — Promotion to required check requires zero false `ADMIT` on the covered qualification corpus and documented residual risk.
- `ASC-G89-R5` — Break-glass behavior is explicit and auditable.

### Invariants

- `ASC-INV-BOOT-001` — Ascend is not evidence for the correctness of the first Ascend implementation.
- `ASC-INV-BOOT-002` — Audit-only decisions cannot block/authorize real consequential effects until promotion criteria are met.
- `ASC-INV-BOOT-003` — After promotion, a required admission result is bound to the exact protected commit/artifact/evidence set it evaluated.

---

## G10 — FOSSIL lineage integration

### Goal
Persist durable intellectual/evidence lineage without making FOSSIL a runtime dependency.

### Requirements

- `ASC-G10-R1` — Use the real FOSSIL validate/authorize/commit boundary.
- `ASC-G10-R2` — Store/verify actual canonical FOSSIL receipt/status.
- `ASC-G10-R3` — GitHub remains current project/source truth.
- `ASC-G10-R4` — Graph/Neo4j/Graphiti remain projections, not Ascend authority.

### Invariants

- `ASC-INV-FOS-001` — Manual JSON/Markdown is never described as a FOSSIL write.
- `ASC-INV-FOS-002` — Ascend remains operational if FOSSIL or graph projection is unavailable.
- `ASC-INV-FOS-003` — Durable lineage can preserve contradiction/supersession/history without changing current executable project truth.

---

## Architecture reopening rule

The architecture is frozen after this planning gate. Reopen only for one of:

- formal counterexample;
- failed acceptance/qualification test;
- production incident;
- new requirement;
- security finding;
- measured benchmark failure;
- unavoidable infrastructure constraint.

A new interesting technique, model, framework, or paper is not by itself sufficient.
