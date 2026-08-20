# Cortex Ascend — Current State

**Current decision:** `ALL GATES KERNEL-COMPLETE -> OPERATIONAL INTEGRATION GAPS REMAIN`  
**Current authorized gate:** `G0-G10 — Foundation through promotion gates (kernel policy complete)`  
**Current implementation status:** All gate issues (#7–#18 and #2–#6) are kernel-complete. Remaining work is operational integration: AWS OIDC/IAM roles, artifact store and verifier rerun, multi-vendor model transport, sealed holdout store, GitHub required-check integration, and real FOSSIL integration.

## Generated current facts

<!-- BEGIN GENERATED HANDOFF FACTS -->
> Generated from `handoff.yaml` by `tools/render_handoff.py`. Do not edit this block directly.

- Repository: `Pukujan/Cortex-ascend` (default branch `main`)
- Project status: `ALL GATES KERNEL-COMPLETE -> OPERATIONAL INTEGRATION GAPS REMAIN`
- Architecture frozen: `yes`
- Current gate: `G0-G10 — Foundation through promotion gates (kernel policy complete)` (issue #0)
- Current child issue: none
- Implemented capabilities: `python_3_12_plus_project_metadata`, `uv_lockfile`, `src_package_skeleton`, `architecture_boundary_checker`, `kernel_third_party_deny_by_default`, `architecture_negative_fixtures`, `handoff_manifest_validation`, `bounded_generated_handoff_facts`, `pr_contract_checker`, `adr_structure`, `docs_impact_policy`, `ruff_strict_mypy_gates`, `pytest_hypothesis_harness`, `reproducible_make_check`, `github_actions_qualification`, `sha_pinned_third_party_actions`, `cpython_3_12_ci_runtime`, `oidc_future_aws_credential_path`, `credential_history_scanning`, `independent_critic_receipt`, `codeowners_policy`, `protected_main_with_required_checks`, `consolidated_negative_qualification_receipt`, `transport_use_rationale_recorded`, `package_root_architecture_enforcement`, `immutable_kernel_domain_types`, `work_contract_v1`, `evidence_receipt_v1`, `canonical_serialization_and_hashing`, `pure_admission_predicates`, `mutation_test_harness`, `stale_generation_lifecycle_model`, `tla_plus_lifecycle_spec`, `formalism_bakeoff_adr`, `model_lane_policy`, `worker_verifier_runtime_profiles`, `adversarial_seat_identity`, `cross_vendor_seat_gating`, `graybox_execution_check`, `attack_hypothesis_receipt`, `sealed_holdout_suite`, `declared_chaos_fault_schedule`, `ascend_audit_mode`, `gate_promotion_policy`, `fossil_receipt_placeholder`
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
- machine-readable handoff covering G0–G10;
- G0 child issues #7–#18 and gate issues #2–#6 with dependency/evidence contracts;
- Python 3.12+ project metadata and committed `uv.lock`;
- `src/cortex_ascend/` kernel package with immutable domain types;
- executable architecture boundaries and deliberate architecture negative fixtures;
- restricted-grammar `handoff.yaml` parser/validator using only the Python standard library;
- bounded generated-fact blocks in `docs/HANDOFF.md` and `docs/CURRENT_STATE.md`;
- reproducible docs/handoff consistency checker and deliberate negative fixtures;
- PR contract checker and pull-request template;
- ADR structure and documentation-impact policy.
- locked Ruff, strict Mypy, Pytest, and Hypothesis qualification tooling;
- deliberate static, test-harness, docs, workflow, and secret negative fixtures;
- the G0 `make check` qualification graph with wrapper and propagation-failure evidence;
- SHA-pinned GitHub Actions workflows that run `make check` on CPython 3.12;
- workflow-policy, OIDC-future-path, and credential/history scanning with deliberate negatives;
- pure kernel domain types: `WorkContract`, `EvidenceReceipt`, `Generation`, `ProjectSnapshot`, deterministic admission predicates, canonical serialization/hashing;
- stale-generation lifecycle model with TLA+ formalism selection ADR;
- kernel-side model-lane policy, worker/verifier runtime profiles, and trust-domain separation;
- adversarial seat identity, cross-vendor seat gating, attack-hypothesis structures, sealed holdout suite metadata, declared chaos fault schedules;
- Ascend audit-mode admission comparison, gate promotion policy, and FOSSIL receipt placeholder;
- graybox execution check runner and receipt for isolated executioner runtime.

## What does not exist yet

- AWS OIDC/IAM roles and artifact store;
- multi-vendor model transport qualification against live providers;
- AgentCore worker/verifier runtime environments;
- sealed holdout store with verifier-controlled access;
- GitHub required-check integration on protected main;
- real FOSSIL integration.

## Immediate next work

Operational integration gaps listed in `handoff.yaml` are the remaining work. No further gate semantics are authorized until the corresponding operational gaps are closed and the architecture is reopened through a declared trigger.

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
