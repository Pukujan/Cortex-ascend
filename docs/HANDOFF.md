# Cortex Ascend — Fresh Session Handoff

## Decision

`REVISE -> START G0 ONLY`

Architecture is frozen. Do not reopen it absent a declared reopening trigger.

## Read first

1. `README.md`
2. `docs/ASCEND_FOUNDATION_AND_BUILD_PLAN.md`
3. `docs/PHASE_REQUIREMENTS_AND_INVARIANTS.md`
4. `docs/CURRENT_STATE.md`
5. `handoff.yaml`
6. GitHub issue #1 and the active G0 child issue

## Current authorization

Only `G0 — Foundation and bootstrap qualification` is authorized.

G0.1 (#7) is merged. Executable architecture boundaries (#10) are complete after this merge. Active parallel-foundation work is #8 (Ruff/Mypy), #9 (Pytest/Hypothesis), and #11 (handoff/docs/PR contract). These converge at #12 (`make check`). Their existence does not authorize G1 semantics.

The architecture boundary is now mechanically checked with a stdlib-only equivalent to Import Linter. During G0 the kernel may import only Python standard-library modules and `cortex_ascend` internals; third-party imports are deny-by-default.

## G0 mission

Build a foundation that mechanically rejects bad architecture and stale project state before Cortex semantics exist:

- Python 3.12+ / `uv` / `src/` layout;
- Ruff;
- strict Mypy;
- Pytest + Hypothesis;
- Import Linter / dependency-boundary enforcement;
- one reproducible local+CI qualification command;
- locked dependencies and provenance-conscious CI;
- pinned third-party GitHub Actions;
- docs/handoff impact gate;
- deliberate negative foundation fixtures;
- GitHub branch/ruleset/required-check enforcement;
- sanitized OpenCode/LiteLLM bootstrap qualification if used for consequential development;
- one genuinely independent external critic pass before G1.

## Stable architectural direction

```text
adapters -> application -> kernel
```

Ports are inward-facing capability contracts; adapters may depend on ports, and ports may depend on kernel types. Kernel cannot depend outward on ports, application, adapters, or CLI.

The kernel cannot import AWS, AgentCore, LiteLLM, OpenCode, FOSSIL, GitHub, graph, orchestration, or model SDKs. During G0 this is enforced more strictly as an empty third-party allowlist.

Initial machine-readable semantic representation is a minimal immutable `WorkContract`, not a universal Spec IR.

Models search the failure space. Deterministic/mechanical or explicitly classified oracles decide covered predicates. No model may declare its own work admissible.

Worker and independent verifier/holdout material must not share the same AgentCore worker trust domain.

Git/GitHub owns current executable project state. FOSSIL later owns durable intellectual/evidence lineage through its real canonical commit boundary and is not a runtime dependency.

## Later sequence — not yet authorized

- G1–G2: pure kernel, WorkContract, EvidenceReceipt.
- G3: stale-generation distributed invariant; compare TLA+/P/FizzBee and keep one primary formalism.
- G4–G5: qualify OpenCode/LiteLLM/Qwen and AgentCore worker/verifier separation.
- G6–G7: adversarial inference, Qwen scaling, VibeThinker formal-adversary benchmark, semantic mutation, sealed holdout, chaos.
- G8–G9: Ascend audit-only, then promotion to required admission gate only after external conformance.
- G10: real FOSSIL lineage integration.

Lean is optional and enters only for a theorem-shaped pure-kernel obligation that earns its additional cost.

## Secrets/configuration

Credentials may be provisioned by local Codex into GitHub/AWS secret stores. Never commit credential values.

Logical names:

- `LITELLM_API_KEY` — secret
- `LITELLM_BASE_URL` — variable unless credential-bearing
- `QWEN_API_KEY` — secret
- `QWEN_BASE_URL` — variable unless credential-bearing

Provisioning these values does not qualify the transport; timeout, exact requested/actual model identity, fallback, and isolation behavior still require explicit tests.

## Reopening triggers

Architecture can be reopened only for:

- formal counterexample;
- failed acceptance/qualification test;
- production incident;
- new requirement;
- security finding;
- measured benchmark failure;
- unavoidable infrastructure constraint.

Another clever framework, model, paper, or architectural idea is not sufficient.
