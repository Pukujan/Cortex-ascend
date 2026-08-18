# Cortex Ascend — Current State

**Current decision:** `REVISE -> START G0 ONLY`  
**Current authorized gate:** `G0 — Foundation and bootstrap qualification`  
**Current implementation status:** planning/genesis only; no semantic kernel is authorized or implemented yet.

## Current authority

1. `docs/ASCEND_FOUNDATION_AND_BUILD_PLAN.md` — architecture, constitution, adversarial findings, bootstrap trust ladder, implementation sequence.
2. `docs/PHASE_REQUIREMENTS_AND_INVARIANTS.md` — per-phase requirements, invariants, evidence and exit conditions.
3. `handoff.yaml` — machine-readable fresh-session bootstrap state.
4. GitHub issues #1–#6 — bounded implementation work packages.

Historical Cortex V6 material is donor/evidence/failure-corpus material. It is not current architecture authority for Cortex Ascend.

## What exists now

- initialized public repository;
- final adversarial review and frozen architecture plan;
- constitution and architecture reopening rule;
- explicit bootstrap trust model so Ascend does not self-certify its first implementation;
- phase requirement/invariant contract;
- machine-readable handoff;
- six bounded build issues covering G0 through G10.

## What does not exist yet

- Python project scaffold;
- `uv.lock`;
- Ruff/Mypy/Pytest/Hypothesis/Import Linter configuration;
- reproducible `make check`;
- GitHub Actions qualification workflows;
- protected-main required rules/checks;
- semantic kernel;
- WorkContract/EvidenceReceipt schemas;
- formal lifecycle model;
- qualified OpenCode/LiteLLM/Qwen transport;
- AgentCore worker/verifier environments;
- sealed holdout;
- adversarial inference seats;
- chaos experiments;
- Ascend admission gate;
- real FOSSIL integration.

## Immediate next work

Only issue #1 is authorized for execution.

The new implementation session should decompose #1 into small PR-sized G0 work packages while preserving the requirements and invariants in `docs/PHASE_REQUIREMENTS_AND_INVARIANTS.md`.

Recommended G0 order:

1. Python/uv/src-layout skeleton.
2. Ruff + strict Mypy.
3. Pytest + Hypothesis baseline.
4. Import Linter and explicit kernel dependency boundary.
5. single reproducible `make check`.
6. CI with locked/pinned provenance controls.
7. negative foundation fixtures proving expected failures.
8. machine-readable handoff/current-state generation or validation.
9. branch/ruleset/required-check enforcement.
10. sanitized OpenCode/LiteLLM bootstrap qualification if the lane is needed for consequential development.
11. genuinely independent external plan critique and disposition.
12. close G0 only after all exit evidence exists.

## Credential/bootstrap configuration

Local Codex may provision the real model transport credentials through GitHub/AWS secret stores. Never commit API keys or credential-bearing URLs.

Expected logical configuration names:

- secret: `LITELLM_API_KEY`
- variable: `LITELLM_BASE_URL` (use a secret instead if the URL embeds credentials)
- secret: `QWEN_API_KEY`
- variable: `QWEN_BASE_URL` when a custom endpoint is required

These credentials do not themselves qualify the transport. Before consequential Ascend work uses the lane, G0/G4 requirements still require sanitized-fixture qualification of timeout, exact requested/actual model identity, fallback behavior, and isolation.

## Architecture reopening

Do not reopen architecture because another framework/model/paper is interesting. Reopen only for a formal counterexample, failed qualification test, production incident, new requirement, security finding, measured benchmark failure, or unavoidable infrastructure constraint.
