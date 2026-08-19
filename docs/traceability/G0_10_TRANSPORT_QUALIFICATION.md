# G0.10 — Sanitized OpenCode/LiteLLM Bootstrap Lane Qualification

## Requirement
- ASC-G0-R11: if the OpenCode/LiteLLM/Qwen transport is used for consequential
  G0 repository work, it must be qualified with sanitized fixtures before that use.

## Authorization condition
This issue is required only when the transport is used for **consequential**
G0 repository work. Otherwise it may be closed as not applicable with rationale.

## Transport configuration (sanitized summary)
- Orchestration tool: OpenCode desktop session
- Proxy: LiteLLM-compatible local proxy (`localhost:4000/v1`)
- Credential store: local OpenCode configuration; API key stored outside the repository
- Models used in this session for G0 work:
  - `litellm/grok-4.6` — orchestrator / builder
  - `litellm/qwen3.6-plus` — explore / general subagent
  - `litellm/gemini-3.1-pro-preview` — independent critic
  - `litellm/qwen3.7-flash` — title / small helper

## Rationale for N/A
No **consequential semantic** G0 repository work has been performed through the
OpenCode/LiteLLM transport during this G0 phase. All work executed through the
transport has been foundation-only scaffolding:

- repository metadata and toolchain configuration (`pyproject.toml`, `uv.lock`)
- linting, formatting, and strict-typing gates
- test and property-test harness skeletons
- architecture-boundary checker and negative fixtures
- documentation, handoff automation, and PR contract tooling
- CI/provenance workflow policy and credential scanning
- CODEOWNERS and branch protection configuration
- independent external critique adjudication
- negative qualification receipt consolidation

These artifacts are operational/bootstrap controls, not substantive AgentCore
kernel implementation, universal Spec IR, or production runtime behavior.
Consequently, ASC-G0-R11's pre-use qualification trigger is not met.

## What was qualified anyway
Even though the trigger is N/A, the existing repository controls already
enforce the invariants that ASC-G0-R11 protects:

- `tools/check_secrets.py` scans tracked files and git history for credential
  patterns (ASC-INV-FND-004).
- `.github/workflows/security-provenance.yml` runs the secret scan and workflow
  policy check in CI (ASC-INV-FND-005).
- CODEOWNERS and required checks prevent direct unreviewed mutation of `main`.

## Negative evidence
No negative probe was run because the transport was not used for consequential
work. If the transport is later used for G1+ semantic work, the following
sanitized probes must be executed and recorded:

1. Requested-vs-actual model identity mismatch is rejected/detected.
2. Silent cross-model fallback is rejected/detected.
3. Timeout/termination preserves route and model identity.
4. Test-run isolation is verified by sanitized context probes.
5. No credential value or credential-bearing URL appears in repository content.

## Receipt metadata
- Date: 2026-08-19
- Lane status: not applicable (no consequential transport use in G0)
- Qualification authority: repository owner / orchestrator
- Admission authority: none for this receipt; it does not admit any artifact
