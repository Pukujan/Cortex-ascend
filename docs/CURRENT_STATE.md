# Cortex Ascend — Current State

**Current decision:** `REVISE -> START G0 ONLY`  
**Current authorized gate:** `G0 — Foundation and bootstrap qualification`  
**Current implementation status:** G0 foundation implementation has started; the G0.1 Python/uv substrate is present on this branch, but no semantic kernel is authorized or implemented.

## Current authority

1. `docs/ASCEND_FOUNDATION_AND_BUILD_PLAN.md` — architecture, constitution, adversarial findings, bootstrap trust ladder, implementation sequence.
2. `docs/PHASE_REQUIREMENTS_AND_INVARIANTS.md` — per-phase requirements, invariants, evidence and exit conditions.
3. `handoff.yaml` — machine-readable fresh-session bootstrap state.
4. GitHub issue #1 and child issues #7–#18 — bounded G0 implementation work packages.

Historical Cortex V6 material is donor/evidence/failure-corpus material. It is not current architecture authority for Cortex Ascend.

## What exists now

- initialized public repository;
- final adversarial review and frozen architecture plan;
- constitution and architecture reopening rule;
- explicit bootstrap trust model so Ascend does not self-certify its first implementation;
- phase requirement/invariant contract;
- machine-readable handoff;
- bounded build issues covering G0 through G10;
- G0 child issues #7–#18 with dependency/evidence contracts;
- Python 3.12+ project metadata;
- committed `uv.lock`;
- minimal `src/cortex_ascend/` package skeleton with no semantic behavior.

## What does not exist yet

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

Only G0 is authorized. The current bounded execution unit is child issue #7 (`G0.1`).

After #7 merges, the safe parallel wave is:

1. #8 — Ruff + strict Mypy.
2. #9 — Pytest + Hypothesis baseline.
3. #10 — Import Linter and explicit kernel dependency boundary.
4. #11 — machine-readable handoff/current-state and PR-contract mechanics.

Those converge at #12, which establishes the single reproducible `make check`. CI/provenance (#13), protected-main enforcement (#14), consolidated negative qualification (#15), independent critique (#17), and final G0 exit (#18) follow according to their recorded dependencies. #16 is conditional on consequential use of the bootstrap model lane.

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
