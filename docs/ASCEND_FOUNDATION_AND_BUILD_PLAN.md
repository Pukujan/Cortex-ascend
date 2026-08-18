# Cortex Ascend — Final Adversarial Review, Foundation Contract, and Build Plan

**Date:** 2026-08-18  
**Decision:** `REVISE -> START G0 ONLY`  
**Scope:** architecture freeze, bootstrap trust, foundation engineering, assurance pipeline, and bounded implementation order.  
**Not authorized yet:** production deployment, broad autonomous work, or treating Ascend as its own qualification authority.

---

## 1. Purpose

Cortex Ascend is an evidence-driven software-engineering assurance kernel for bounded AI work executed on mature infrastructure.

The project does **not** aim to become a workflow engine, model gateway, cloud runtime, universal multi-agent framework, knowledge-graph platform, CI replacement, theorem prover, or database. Those capabilities should be rented from mature systems when possible.

The differentiating problem is narrower:

> An untrusted probabilistic software worker produces a candidate artifact under an exact work contract. Independent assurance produces evidence bound to the exact artifact, project state, authority, model identity, and generation. A small deterministic kernel decides whether the evidence is sufficient to admit the work.

Conceptually:

```text
bounded engineering intent
        |
        v
immutable WorkContract
        |
        v
untrusted AI execution
        |
        +-----------> adversarial search
        |              models / mutants / red teams
        v
candidate artifact
        |
        v
independent qualification
 deterministic + formal + empirical evidence
        |
        v
EvidenceReceipt set
        |
        v
Cortex Ascend kernel
 ADMIT | REJECT | STALE | BLOCKED
        |
        +--------> GitHub current project state
        |
        +--------> FOSSIL durable intellectual/evidence lineage
```

---

## 2. Final adversarial review

### 2.1 Verdict

The architecture survives adversarial review, but only after four revisions:

1. **Start with a minimal WorkContract IR, not a universal Spec IR.** A richer Spec IR must earn its complexity later through measured traceability or assurance value.
2. **Ascend must bootstrap from an external trust base.** Ascend cannot initially certify itself. Git/GitHub controls, deterministic CI, formal tools, human ownership, and independent reviewers qualify the first kernel.
3. **Model diversity is search diversity, not authority.** Multiple vendors, Qwen, VibeThinker, or frontier models may search for failures; their agreement is not evidence of correctness.
4. **Formal methods and specialist models enter only when a bounded property and an oracle exist.** No formal-method or model collection is installed merely because it is sophisticated.

This is therefore a `REVISE -> START G0 ONLY` decision: begin the foundation and bootstrap work, but do not authorize a large implementation yet.

### 2.2 Adversarial finding: metasystem bloat remains the largest architectural risk

The easiest way to destroy Ascend is to add one subsystem for every interesting idea: orchestration, KG memory, ontology service, model router, formal-language layer, agent society, custom scheduler, custom CI, and several theorem provers.

**Disposition:** keep the semantic kernel small. Infrastructure is adapter territory. Any new mechanism must beat a serious simpler baseline or be removed.

### 2.3 Adversarial finding: self-verification is circular

If the first Ascend implementation is accepted because Ascend says it is correct, there is no independent root of trust.

**Disposition:** bootstrap in stages. The first releases are qualified by external deterministic tooling and owner review. Ascend initially runs in audit-only mode and must reproduce externally established decisions before it can become a required admission gate.

### 2.4 Adversarial finding: IR can become false authority

A machine-readable representation can be syntactically perfect and semantically wrong. LLM-generated IR can misread the requirement, omit an exception, or encode the wrong invariant.

**Disposition:** the first IR is only a narrow `WorkContract`: an immutable executable work envelope. It is an addressable artifact, not truth. A richer `Spec IR` is deferred until a benchmark shows that it improves requirement-to-work-to-evidence traceability enough to justify another semantic layer.

### 2.5 Adversarial finding: formal verification can prove the wrong thing

A proof/model-check pass establishes a property of the formalized model under its assumptions. It does not automatically establish that the property expresses the human requirement or that the executable implementation conforms to the formal model.

Lean's own validation guidance explicitly distinguishes proof validity from the meaning of the theorem statement and states that assurance depends on the formal theorem corresponding to its intended meaning. P and FizzBee both provide mechanisms aimed at connecting formal models to implementation/runtime behavior.

**Disposition:** treat these as separate obligations:

```text
requirement
   | semantic conformance
   v
formal property/model
   | proof/model checking
   v
verified model
   | implementation conformance
   v
executable artifact
   | runtime/release evidence
   v
observed system
```

Every arrow can fail and needs proportionate evidence.

### 2.6 Adversarial finding: unlimited inference can create noise and overfitting

Cheap or unlimited model calls can produce thousands of critiques without improving assurance. Repeated exposure to the same benchmark also converts a holdout into a development set.

**Disposition:** inference is budgeted by role and novelty. Outputs are deduplicated and converted into executable hypotheses. Sealed holdouts remain inaccessible to builders and normal critics. Models search; deterministic or explicitly classified judgment oracles decide.

### 2.7 Adversarial finding: cross-vendor is not automatically independent

Two models can differ in vendor while sharing transport, account/quota, prompt packet, controller, runtime, hidden test leakage, or verifier.

**Disposition:** every assurance seat records independence dimensions explicitly. Independence is a vector, not a boolean.

### 2.8 Adversarial finding: AgentCore isolation does not separate actors inside one microVM

AgentCore provides strong session isolation, but AWS documents that code and commands within a Runtime microVM share that microVM trust boundary and may access the execution role credentials available to it.

**Disposition:** worker, hidden evaluator, and admission/verifier credentials must not coexist in one worker session. Use separate runtime sessions/roles and least privilege. Same-account separation is acceptable for the first bounded build; stronger account-level isolation can be introduced only if the risk model requires it.

### 2.9 Adversarial finding: a public repository cannot contain a real sealed holdout

Anything committed to this public repository is visible to the worker and eventually to model providers.

**Disposition:** sealed cases/answers live outside the repository, initially in a private verifier-controlled store such as a private S3 prefix or private repository. The public repo stores only holdout identity/version/count/hash and sanitized aggregate receipts.

### 2.10 Adversarial finding: CI itself is part of the trusted computing base

A green CI badge is weak evidence if dependencies float, third-party Actions are referenced by movable tags, cloud credentials are long-lived, or required checks can be bypassed.

**Disposition:** lock dependencies; pin third-party Actions to full commit SHAs; use GitHub OIDC for short-lived AWS credentials; minimize workflow permissions; make required checks/rulesets part of G0; and treat provenance as evidence that must itself be verified.

### 2.11 Adversarial finding: documentation drift can make a technically correct repo operationally unsafe

Fresh agents can implement against stale architecture if current state is fragmented across issues, old plans, chat transcripts, and historical FOSSIL proposals.

**Disposition:** current-state documentation and machine-readable handoff are part of Definition of Done. Semantic changes that do not update the required documentation fail CI.

### 2.12 Adversarial finding: FOSSIL can become an accidental runtime dependency or fake audit trail

Writing JSON or Markdown that resembles FOSSIL data is not a canonical FOSSIL commit.

**Disposition:** GitHub remains current project/source truth. Ascend must run when FOSSIL is unavailable. FOSSIL receives durable intellectual/evidence lineage only through its real validated commit boundary, with an actual receipt. Graph databases remain FOSSIL projections, not Ascend runtime authority.

### 2.13 Adversarial finding: distributed side effects are harder than code correctness

Retries, duplicate delivery, delayed evidence, revocation, stale generations, crash-after-effect-before-ack, and reconciliation can violate semantics even when every individual function is correct.

**Disposition:** generation fencing, authority, idempotency/effect identity, and stale evidence are the first distributed semantics to model and test. Do not begin with complex business workloads.

### 2.14 Adversarial finding: formal-tool proliferation is another form of bloat

TLA+, P, FizzBee, Lean, Dafny, Z3, Alloy, CrossHair, and theorem provers solve overlapping but different problems. Installing all of them does not create assurance.

**Disposition:** one bounded lifecycle example will compare P, TLA+, and FizzBee for the same invariant. One primary distributed formalism will then be selected. Lean remains optional for theorem-shaped pure-kernel obligations. Z3/symbolic tools remain local instruments for small constraints.

### 2.15 Adversarial finding: specialist models can become decorative complexity

VibeThinker-3B is explicitly aimed at verifiable math/code/STEM reasoning, but its maintainers do not recommend it for tool-calling or autonomous coding-agent work.

**Disposition:** VibeThinker enters only as a specialist formal/mathematical adversary or counterexample generator after a deterministic target exists. It does not own the repository, tool execution, or admission.

---

## 3. Cortex Ascend constitution

The following rules are intended to be stable unless a concrete trigger justifies reopening architecture.

1. **Git/GitHub owns current executable project state.**
2. **FOSSIL owns durable intellectual/evidence lineage, not live runtime state.**
3. **The kernel is pure domain logic.** No AWS, AgentCore, LiteLLM, OpenCode, FOSSIL, GitHub, graph, or model SDK imports are permitted in the kernel.
4. **Architectural boundaries that matter must be executable constraints.** Import/dependency violations fail CI.
5. **The initial IR is a minimal immutable WorkContract.** A richer Spec IR is not assumed necessary.
6. **No probabilistic actor can declare its own work admissible.** Models may propose code, tests, formalizations, critiques, or evidence hypotheses.
7. **Requested and actual model identity are distinct evidence fields.** Semantic fallback requires explicit authorization; transport behavior cannot silently rewrite a model seat.
8. **Development checks and qualification evidence are distinct.** Worker-local tests may guide repair; consequential evidence must be independently reproduced or produced outside the worker trust domain.
9. **Evidence binds exact identities.** At minimum: work contract, project snapshot, generation, artifact digest, verifier/tool version, and relevant model identity.
10. **Freshness is semantic.** Successful evidence for a superseded generation may be `STALE`, not success.
11. **Authority is explicit.** Declared scope is not the same as a valid AuthorityGrant. Issuance, expiry, revocation, replay, and allowed effects are modeled separately from infrastructure IAM.
12. **Model diversity is adversarial search, not voting authority.** Agreement is metadata.
13. **Hidden holdouts are inaccessible to builders.** Holdout leakage invalidates the affected qualification claim.
14. **Formal proof is one evidence class.** Semantic correctness, implementation conformance, security, empirical testing, and operational evidence remain separate obligations.
15. **Chaos is hypothesis-driven.** Every injected fault names the invariant and expected result.
16. **Documentation is part of completion.** Consequential changes are incomplete until code, executable evidence, current-state documentation, and resumability state agree.
17. **No fake FOSSIL.** Only a successful canonical validated FOSSIL commit is called a FOSSIL write.
18. **Ascend must function without FOSSIL online.**
19. **Infrastructure is rented unless Ascend semantics require ownership.** GitHub Actions, AgentCore, AWS orchestration, model providers, and mature verification tools remain replaceable adapters.
20. **Architecture review stops after this gate.** Reopen architecture only for a formal counterexample, failed acceptance test, production incident, new requirement, security finding, measured benchmark failure, or unavoidable infrastructure constraint. Another clever idea is not sufficient.

---

## 4. Bootstrap trust ladder: how Ascend is built correctly before Ascend exists

### B0 — Genesis trust

Trusted externally:

- repository owner;
- Git object identity;
- GitHub repository controls;
- reviewed planning documents;
- external official toolchains.

The two genesis commits that create this README/plan are administrative bootstrap exceptions. After G0, direct semantic changes to `main` are prohibited by policy/ruleset.

### B1 — External deterministic foundation

Build the repository foundation using ordinary mature tooling only. Ascend has no authority yet.

Required external checks:

- Python 3.12+;
- `uv` project and lockfile;
- `src/` package layout;
- Ruff format/lint;
- Mypy strict;
- Pytest;
- Hypothesis;
- Import Linter architectural contracts;
- selected mutation testing on semantic modules;
- dependency/security audit;
- documentation/handoff consistency checks;
- GitHub Actions pinned to immutable SHAs;
- GitHub OIDC for AWS access;
- branch/ruleset + required checks;
- reproducible `make check`.

The foundation is not accepted merely because these tools run. G0 includes deliberate negative tests proving that malformed imports, missing documentation, type violations, and broken invariants actually make CI fail.

### B2 — Pure kernel qualification

Implement only the smallest domain objects and pure predicates. No AWS.

Candidate primitives:

- `ProjectSnapshot`
- `WorkId`
- `Generation`
- `ArtifactDigest`
- `AuthorityGrant`
- `ModelIdentity`
- `EvidenceReceipt`
- `AdmissionDecision`

Initial decisions:

- `ADMIT`
- `REJECT`
- `STALE`
- `BLOCKED`

The kernel is qualified with unit/property tests, mutation testing, architecture constraints, and external review. At least one independently run critic from a different model/vendor should attack the frozen contract before consequential agent execution is enabled.

### B3 — Formal lifecycle qualification

Model one distributed invariant: stale-generation/effect admission under retries and delayed events.

Run a bounded comparison of:

- TLA+ / TLC;
- P / P-Checker (and runtime conformance potential via PObserve);
- FizzBee model checking / model-based testing where practical.

The comparison scores:

- ability to express the invariant;
- counterexample quality;
- CI reproducibility;
- implementation-conformance story;
- toolchain burden;
- maintainability by humans and agents.

Freeze **one** primary distributed formalism after the experiment. The others are removed from the normal dependency/tool path unless a later concrete property justifies them.

### B4 — Audit-only Ascend

Ascend starts consuming immutable work/evidence fixtures and emits what it *would* decide, but its result is not a required merge/release gate.

Compare its decisions against externally established expected decisions across:

- stale generation;
- revoked authority;
- artifact substitution;
- evidence replay;
- requested/actual model mismatch;
- duplicate/retry cases;
- seeded semantic mutants.

No false `ADMIT` is acceptable in the qualification corpus.

### B5 — Independent execution/verification

Introduce AgentCore and model seats.

At minimum use two trust domains:

```text
worker runtime / role
       |
       v
immutable candidate artifact
       |
======= trust boundary =======
       |
       v
verifier runtime / role
       |
       v
EvidenceReceipts
       |
======= trust boundary =======
       |
       v
Ascend admission
```

The worker cannot read sealed holdouts or verifier credentials. The verifier does not trust worker claims that checks passed; it reproduces required checks against the exact artifact digest.

### B6 — Authoritative gate

Ascend becomes a required gate only after audit-mode qualification demonstrates agreement with external expected decisions and the failure corpus shows no false admissions for the covered invariants.

Human break-glass authority remains explicit and auditable rather than hidden.

---

## 5. Foundation repository contract (G0)

Target structure:

```text
Cortex-ascend/
├── .github/
│   ├── workflows/
│   │   ├── check.yml
│   │   ├── docs-gate.yml
│   │   └── security-provenance.yml
│   └── CODEOWNERS
├── docs/
│   ├── ASCEND_FOUNDATION_AND_BUILD_PLAN.md
│   ├── CONSTITUTION.md
│   ├── CURRENT_STATE.md
│   ├── HANDOFF.md
│   ├── adr/
│   └── traceability/
├── schemas/
│   ├── work-contract.schema.json
│   └── evidence-receipt.schema.json
├── src/
│   └── cortex_ascend/
│       ├── kernel/
│       ├── application/
│       ├── ports/
│       ├── adapters/
│       └── cli/
├── tests/
│   ├── architecture/
│   ├── unit/
│   ├── property/
│   ├── integration/
│   └── fixtures/
├── formal/
├── infra/
│   └── terraform/
├── tools/
│   ├── docs_check.py
│   └── render_handoff.py
├── handoff.yaml
├── pyproject.toml
├── uv.lock
├── .python-version
├── Makefile
└── README.md
```

### G0 mandatory checks

`make check` must be the local/CI source of truth and should run, at minimum:

```text
uv lock/check discipline
ruff format --check
ruff check
mypy --strict
import-linter contracts
pytest unit
pytest property
architecture tests
documentation/handoff gate
selected security/dependency audit
```

Mutation testing may run in a slower workflow initially, but semantic kernel PRs must eventually meet an explicit mutation threshold for high-value guards.

### Architecture dependency direction

```text
adapters
   |
   v
application
   |
   v
kernel
```

`kernel` may not import `application`, `ports`, `adapters`, cloud SDKs, model SDKs, GitHub clients, FOSSIL, graph libraries, or orchestration libraries.

Ports define Ascend-owned capability contracts. Adapters implement those contracts for AWS/GitHub/models/FOSSIL.

### Documentation/handoff gate

`handoff.yaml` is the machine-readable current-state manifest. `docs/HANDOFF.md` and relevant portions of `docs/CURRENT_STATE.md` are rendered/validated from it.

The manifest contains at least:

- repository identity;
- authoritative commit;
- current gate;
- implemented capabilities;
- active invariants;
- open blockers;
- next bounded work;
- authoritative ADRs/contracts;
- FOSSIL canonical receipt status when applicable.

CI must reject consequential changes where required documentation disposition is missing.

Examples:

- `kernel/**` change -> invariant/traceability + handoff impact required;
- `schemas/**` change -> schema/version documentation required;
- `ports/**` change -> boundary/ADR disposition required;
- `infra/**` change -> deployment/security documentation required;
- formal model change -> property-to-code/test traceability required.

Generated facts are auto-updated/validated. Architectural meaning is proposed and reviewed; an agent may not silently rewrite the constitution or ADRs.

---

## 6. Initial IR strategy

### 6.1 WorkContract v1 enters in G1

The initial machine-readable IR is a canonical bounded work contract, not a programming language and not a claim of truth.

Minimum conceptual fields:

```text
work_id
project_snapshot
base_git_sha
config/schema identities
generation
requirement references / bounded intent
allowed scope/effects
AuthorityGrant reference
requested ModelSeat
acceptance predicates
AssurancePlan
secret/egress rules
time budget
```

The canonical representation is hashable and immutable after issuance.

### 6.2 Spec IR is deferred

A separate Spec IR is introduced only if a later experiment demonstrates that it improves at least one of:

- requirement-to-code traceability;
- formal-property derivation;
- invalidation/supersession handling;
- hidden evaluation construction;
- reviewer reconstruction accuracy.

If a WorkContract plus versioned engineering documents provides equivalent value more simply, do not add Spec IR.

---

## 7. When TLA+, P, FizzBee, Lean, Z3, and VibeThinker enter

### G0: none of them are foundation dependencies

The foundation must be understandable and testable without formal or specialist-model tooling.

### G1: WorkContract + pure kernel

Use ordinary Python types, strict typing, Pytest, Hypothesis, and mutation testing first.

### G2: TLA+ / P / FizzBee bounded bakeoff

Formalize the same stale-generation/retry/revocation lifecycle problem in a deliberately small experiment. Freeze one primary distributed formalism.

Current evidence makes P particularly interesting because the P project provides state-machine modeling, systematic checking, AI-assisted P generation, and PObserve for checking service logs against P monitors. FizzBee is attractive for Python-like modeling and model-based testing. TLA+ remains the mature baseline for distributed design/model checking.

The project does not carry three primary formalisms after the bakeoff.

### G3/G4: VibeThinker specialist adversary

VibeThinker-3B is introduced only after we have deterministic or formal targets. Suitable seats:

- smallest counterexample search;
- invariant attack;
- mathematical/constraint review;
- distinguishing-input generation;
- formalization critique.

It does **not** own autonomous repository work, API orchestration, or admission.

Run multiple independent samples when useful, cluster/deduplicate hypotheses, and send surviving cases to deterministic execution/checkers.

### Lean: optional and late

Lean is not required for the first distributed system. Add it only when a pure kernel obligation is genuinely theorem-shaped and the proof gives material value beyond property/symbolic testing.

If Lean is introduced, qualification must distinguish:

- theorem proof accepted by the Lean kernel;
- theorem statement correctly expressing the intended requirement;
- implementation conforming to the theorem/model.

For high-risk Lean evidence, use independent proof rechecking such as `lean4checker` where appropriate.

### Z3 / symbolic tools

Use narrowly for constraints and pure predicates where the translation is small and inspectable. Do not turn the whole system into SMT.

---

## 8. Model-seat and adversarial assurance model

Initial seats:

| Seat | Typical model/tool | Purpose | Admission authority |
|---|---|---|---|
| `BUILD` | Qwen 27B / qualified frontier coder | bounded implementation | none |
| `RED_ARCH` | independent frontier vendor | architecture/semantic attack | none |
| `RED_SEC` | independent frontier/security reasoning | IAM, secret, authority, supply-chain attack | none |
| `RED_DIST` | Qwen/frontier/VibeThinker where suitable | race/retry/state-machine counterexamples | none |
| `MUTANT` | Qwen/frontier | plausible semantic defects | none |
| `FORMAL_ADV` | VibeThinker / reasoning model | invariant/proof/counterexample attack | none |
| `CHAOS_PLAN` | reasoning models | fault schedules | none |
| `HOLDOUT_AUTHOR` | isolated model/human process | sealed cases | none |
| `VERIFIER` | deterministic tooling / isolated execution | produce qualification facts | evidence-only |
| `ADJUDICATOR` | owner/independent reviewer when judgment irreducible | resolve ambiguity | explicit human/judgment class |
| `ADMISSION` | Ascend deterministic kernel | semantic decision | final gate |

### Independence dimensions

Every consequential receipt should be able to state relevant dimensions such as:

```text
vendor
model family
provider/account
transport
prompt/context lineage
runtime
credentials
verifier implementation
holdout visibility
controller
```

Do not label evidence simply `independent=true`.

### Unlimited inference rule

Abundant inference is used for **search**, especially:

- many candidate implementations;
- semantic mutant generation;
- adversarial requirements interpretation;
- distinguishing inputs;
- race/fault schedules;
- security attack hypotheses;
- counterexamples.

The pipeline must deduplicate and mechanically exercise candidate findings. Majority vote is not an oracle.

---

## 9. Assurance and release pipeline

Risk drives assurance depth.

Baseline classes include:

- formatter/lint/type checks;
- unit/property tests;
- deterministic integration tests;
- mutation testing;
- static/security/dependency analysis;
- formal/model checking for selected lifecycle/authority invariants;
- independent model red teams;
- sealed holdouts;
- fault injection / chaos;
- artifact/provenance checks;
- shadow execution without effect authority;
- controlled canary/A-B where production traffic is appropriate;
- operational observation.

### Red team vs chaos

Red team asks how an intelligent adversary can violate assumptions. Chaos tests whether declared invariants survive environmental failures and event schedules.

Models may propose the attack/fault schedule. The harness executes it. Deterministic/explicit oracles decide the result.

Example:

```text
RED_DIST proposes:
G6 effect succeeds -> ack lost -> G7 issued -> G6 retried -> old verifier result arrives

CHAOS executor reproduces schedule

oracle asserts:
G6 cannot become ADMITTED after G7 is authoritative
```

---

## 10. GitHub Actions, LiteLLM/OpenCode, Qwen, and AgentCore integration

### GitHub Actions

Acts as control/qualification plane:

- exact commit identity;
- deterministic foundation checks;
- OIDC to AWS;
- launch bounded external work;
- retrieve evidence receipts;
- required merge checks;
- provenance/attestation where useful.

Do not use GitHub Actions as the primary long-running inference runtime.

### OpenCode + LiteLLM

Development/model-access lane, not semantic authority.

Before consequential use, qualify:

- pinned OpenCode version/config;
- intended 600-second request envelope;
- requested/actual model identity;
- no hidden cross-model fallback;
- read-only vs mutation capabilities;
- sanitized fixture behavior;
- egress/secret policy.

LiteLLM may normalize transport. It does not decide that one semantic ModelSeat can silently become another.

### Qwen API

Use direct or through a qualified adapter for repository implementation, repeated reviews, test generation, mutant generation, and distributed failure search. Record the provider-returned actual model identity and terms/entitlement appropriate to automated use.

### AgentCore

Use as isolated execution substrate. Separate worker and verifier trust domains/roles. Follow least privilege. Do not store durable authoritative state only in the ephemeral worker session.

### Step Functions

Not required for the first vertical slice. Introduce only when durable orchestration of parallel/retry-heavy assurance stages is demonstrably useful.

---

## 11. First vertical slice

The first end-to-end workload is intentionally small:

> **No result from a stale generation may become admitted.**

Required scenarios:

1. current generation succeeds;
2. G6 finishes after G7 becomes authoritative;
3. duplicate G6 result;
4. replayed G6 evidence;
5. artifact hash swapped between verifier/admission;
6. verification begins before replacement but admission occurs after replacement;
7. authority revoked mid-attempt;
8. effect succeeds then worker crashes before acknowledgement;
9. provider fallback returns a different actual model;
10. verifier crashes and retries.

Evidence must demonstrate that stale/unauthorized/mismatched work cannot produce `ADMIT`.

This slice is valuable because it exercises identity, generation, authority, retry, evidence binding, verifier separation, model identity, and recovery without needing a large product workload.

---

## 12. Implementation sequence

### PR/Gate 0 — Foundation scaffold

Deliver:

- Python/uv project;
- package/layer structure;
- Ruff + strict Mypy;
- Pytest + Hypothesis;
- Import Linter contracts;
- `make check`;
- CI pinned by full Action SHAs;
- docs/handoff gate;
- security/dependency checks;
- branch/ruleset requirements;
- negative tests proving the gates fail correctly.

**Exit:** foundation failures are mechanically blocked before semantic code exists.

### PR/Gate 1 — Pure identities and admission skeleton

Deliver immutable domain types and decision enum. No AWS/model SDK imports.

**Exit:** strict types, architecture tests, unit/property tests green.

### PR/Gate 2 — WorkContract and EvidenceReceipt v1

Deliver canonical schemas/serialization/hashing and stale-binding rules.

**Exit:** any material identity change changes the contract/receipt digest; stale-base evidence is rejected.

### PR/Gate 3 — Stale-generation semantics + formal bakeoff

Implement pure stale-generation admission logic, mutation tests, and the P/TLA+/FizzBee bounded comparison.

**Exit:** one primary formalism chosen by ADR; seeded stale mutants are killed; model checker produces reproducible counterexamples for broken variants.

### PR/Gate 4 — Bootstrap model lane qualification

Qualify OpenCode/LiteLLM and direct Qwen against sanitized fixtures.

**Exit:** exact model identity, timeout envelope, fallback policy, egress policy, and mutation/read-only modes are proven by receipts.

### PR/Gate 5 — AgentCore worker/verifier separation

Terraform two minimal roles/runtimes or equivalent isolated domains. GitHub Actions assumes AWS roles through OIDC.

**Exit:** worker cannot access holdout/verifier secrets; verifier independently re-runs required checks against exact artifact digest.

### PR/Gate 6 — Adversarial inference

Add bounded model seats for architecture/security/distributed criticism and semantic mutants. Introduce VibeThinker only if its controlled benchmark adds unique useful counterexamples.

**Exit:** model-generated attacks become executable cases; no model vote is treated as a pass.

### PR/Gate 7 — Sealed holdout + chaos

Private verifier-controlled holdout and declared fault schedules.

**Exit:** builders cannot retrieve cases/answers; only sanitized receipts leave verifier domain; stale/retry chaos cases pass.

### PR/Gate 8 — Audit-only Ascend admission

Run Ascend decisions alongside external expected decisions without merge authority.

**Exit:** zero false admits on the qualification corpus; discrepancies are explained/fixed.

### PR/Gate 9 — Required admission gate

Only now make Ascend admission a protected required check for covered work classes.

**Exit:** bypass/break-glass path explicit and auditable; current-state docs and handoff automatically updated.

### PR/Gate 10 — Real FOSSIL lineage

Integrate only through real FOSSIL validation/authorize/commit service boundaries.

**Exit:** canonical FOSSIL receipt exists and projection failure cannot block Ascend runtime/merge semantics.

---

## 13. Build-right acceptance criteria

The foundation is considered successful only if we can deliberately create each of the following defects and observe the expected failure:

```text
kernel imports boto3                 -> CI FAIL
untyped kernel function              -> CI FAIL
bad formatting/lint                  -> CI FAIL
architecture layer cycle             -> CI FAIL
semantic change without handoff      -> CI FAIL
schema change without version docs   -> CI FAIL
mutated stale guard                  -> tests/mutation FAIL
stale evidence presented             -> STALE
revoked authority used               -> REJECT/BLOCKED
actual model != authorized seat      -> evidence invalid
worker claims tests passed           -> insufficient until independent verification
hidden holdout access from worker    -> IAM/access FAIL
fake FOSSIL JSON only                -> no canonical FOSSIL receipt
```

These negative tests are more important than a long checklist saying the tools are installed.

---

## 14. External evidence anchors

The architecture is a synthesis; these sources support key mechanisms but do not prove Cortex Ascend as a whole.

- AWS AgentCore Runtime security: dedicated microVM isolation; code/actors inside the VM can access execution-role credentials; command execution shares the VM trust boundary: <https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-security-best-practices.html>
- GitHub Actions OIDC: short-lived cloud tokens instead of long-lived GitHub cloud secrets: <https://docs.github.com/en/actions/concepts/security/openid-connect>
- GitHub Actions secure use: pin third-party Actions to full-length commit SHAs for immutable references: <https://docs.github.com/en/actions/reference/security/secure-use>
- uv project structure/lock workflow: <https://docs.astral.sh/uv/concepts/projects/layout/>
- Ruff linter/formatter: <https://docs.astral.sh/ruff/>
- Mypy command-line strict checking: <https://mypy.readthedocs.io/en/stable/command_line.html>
- Hypothesis property-based testing: <https://hypothesis.readthedocs.io/en/latest/>
- P framework: formal state-machine modeling/checking; PObserve runtime conformance; AWS usage: <https://p-org.github.io/P/>
- FizzBee model-based testing/refinement mapping: <https://fizzbee.io/testing/>
- Lean proof validation and semantic-trust boundary: <https://lean-lang.org/doc/reference/latest/ValidatingProofs/>
- VibeThinker-3B: verifiable reasoning specialist; model card explicitly discourages autonomous tool-calling/coding-agent use: <https://huggingface.co/WeiboAI/VibeThinker-3B>
- SLSA artifact/provenance verification: <https://slsa.dev/spec/v1.2/verifying-artifacts>

---

## 15. What would falsify this plan

Ascend should be narrowed or stopped if evidence shows any of the following:

- the WorkContract/admission layer adds no measurable defect-detection or governance value beyond conventional CI;
- independent assurance cannot be made meaningfully separate without unacceptable operational cost;
- hidden holdouts cannot be administered without contaminating the development process;
- model identity/fallback cannot be reliably observed from selected providers;
- formal lifecycle modeling does not find or prevent bugs beyond property/integration tests at reasonable cost;
- inference-scaled red teaming mostly creates noise rather than reproducible failures;
- the kernel grows into an infrastructure framework rather than remaining a small semantics package.

Mechanisms that fail these tests are removed rather than defended for architectural aesthetics.

---

## 16. Immediate next action

Implement **G0 only**.

Do not begin AgentCore, Step Functions, FOSSIL integration, universal Spec IR, Lean, or autonomous red-team swarms until the repository can first prove that its own ordinary software-engineering and documentation boundaries are mechanically enforced.

After G0 is green and protected, proceed one bounded gate at a time.
