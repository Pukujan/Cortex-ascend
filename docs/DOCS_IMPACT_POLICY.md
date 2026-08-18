# Documentation Impact Policy

Cortex Ascend treats current-state documentation and resumability state as part of completion, not post-merge cleanup.

Every implementation PR must contain a `Documentation / handoff impact` disposition. A bare omission is invalid; “no impact” is acceptable only when the PR explains why the current machine-readable and human-readable state remains correct.

## Path-sensitive expectations

| Changed area | Required disposition |
|---|---|
| `src/cortex_ascend/kernel/**` | affected invariants/traceability plus handoff/current-state impact |
| `src/cortex_ascend/ports/**` | capability-boundary or ADR disposition plus handoff impact |
| `schemas/**` | schema/version documentation and compatibility disposition |
| `infra/**` | deployment/security documentation disposition |
| `formal/**` | property-to-code/test traceability disposition |
| `.github/workflows/**` | CI/provenance/current required-check documentation disposition |
| `tools/**` that alter qualification semantics | qualification/traceability plus current-state/handoff impact |

Generated facts are derived from `handoff.yaml` and may be rewritten only inside the marker-delimited blocks maintained by `tools/render_handoff.py`. Architectural prose, ADR decisions, the constitution, and requirement meaning are never silently generated.

The PR contract is mechanically checked by `tools/check_pr_contract.py`; path-sensitive enforcement can become stricter when the G0 convergence/CI lanes have reliable changed-file context.
