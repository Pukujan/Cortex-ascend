# Cortex Ascend — Current State

**Current decision:** `REVISE -> START G0 ONLY`  
**Current authorized gate:** `G0 — Foundation and bootstrap qualification`  
**Current implementation status:** G0.1–G0.6 foundations complete. G0.7 (CI/provenance #13) PR open. G0.11 (#17 independent critique) complete, adjudicated, with formal counterexample (architecture checker bypass) tracked for fix.

## Generated current facts

<!-- BEGIN GENERATED HANDOFF FACTS -->
> Generated from `handoff.yaml` by `tools/render_handoff.py`. Do not edit this block directly.

- Repository: `Pukujan/Cortex-ascend` (default branch `main`)
- Project status: `ALL GATES KERNEL-COMPLETE -> OPERATIONAL INTEGRATION GAPS REMAIN`
- Architecture frozen: `yes`
- Current gate: `G0-G10 — Foundation through promotion gates (kernel policy complete)` (issue #0)
- Current child issue: none
- Implemented capabilities: `python_3_12_plus_project_metadata`, `uv_lockfile`, `src_package_skeleton`, `architecture_boundary_checker`, `kernel_third_party_deny_by_default`, `architecture_negative_fixtures`, `handoff_manifest_validation`, `bounded_generated_handoff_facts`, `pr_contract_checker`, `adr_structure`, `docs_impact_policy`, `ruff_strict_mypy_gates`, `pytest_hypothesis_harness`, `reproducible_make_check`, `github_actions_qualification`, `sha_pinned_third_party_actions`, `cpython_3_12_ci_runtime`, `oidc_future_aws_credential_path`, `credential_history_scanning`, `independent_critic_receipt`, `codeowners_policy`, `protected_main_with_required_checks`, `consolidated_negative_qualification_receipt`, `transport_use_rationale_recorded`, `package_root_architecture_enforcement`, `immutable_kernel_domain_types`, `work_contract_v1`, `evidence_receipt_v1`, `canonical_serialization_and_hashing`, `pure_admission_predicates`, `mutation_test_harness`, `stale_generation_lifecycle_model`, `tla_plus_lifecycle_spec`, `formalism_bakeoff_adr`, `model_lane_policy`, `worker_verifier_runtime_profiles`, `adversarial_seat_identity`, `attack_hypothesis_receipt`, `sealed_holdout_suite`, `declared_chaos_fault_schedule`, `ascend_audit_mode`, `gate_promotion_policy`, `fossil_receipt_placeholder`
- Completed G0 child issues: #7, #8, #9, #10, #11, #12, #13, #14, #15, #16, #17, #18
- Active G0 child issues: none
- G0 convergence issue: #12
<!-- END GENERATED HANDOFF FACTS -->

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
- G0 child issues #7–#18 with dependency/evidence contracts;
- Python 3.12+ project metadata and committed `uv.lock`;
- minimal `src/cortex_ascend/` package skeleton with no semantic behavior;
- executable architecture boundaries and deliberate architecture negative fixtures;
- restricted-grammar `handoff.yaml` parser/validator using only the Python standard library;
- bounded generated-fact blocks in `docs/HANDOFF.md` and `docs/CURRENT_STATE.md`;
- reproducible docs/handoff consistency checker and deliberate negative fixtures;
- PR contract checker and pull-request template;
- ADR structure and documentation-impact policy.
- locked Ruff, strict Mypy, Pytest, and Hypothesis qualification tooling;
- deliberate static and test-harness negative fixtures;
- the G0 `make check` qualification graph with wrapper and propagation-failure evidence;
- SHA-pinned GitHub Actions workflows that run `make check` on CPython 3.12;
- workflow-policy, OIDC-future-path, and credential/history scanning with deliberate negatives.

## What does not exist yet

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

Only G0 is authorized. G0.1 (#7), G0.2 Ruff/Mypy (#8), G0.3 Pytest/Hypothesis (#9), executable architecture boundaries (#10), resumability/PR-contract mechanics (#11), and the #12 `make check` convergence lane are complete.

#13 is installing provenance-conscious GitHub Actions: the same `make check` graph, CPython 3.12, SHA-pinned Actions, minimal permissions, credential/history scanning, and OIDC as the future AWS path. Protected-main enforcement (#14) waits for these stable check names. Consolidated negative qualification (#15), independent critique (#17), and final G0 exit (#18) remain later G0 work. #16 is conditional on consequential use of the bootstrap model lane.

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
