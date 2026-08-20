# G6-G7 — Graybox Execution Receipt

## Scope

Exercise the executioner lane against the exact working-tree artifact in an
isolated gravebuster container, without model credentials or network access.

## Receipt

| Field | Value |
|-------|-------|
| Runner | `tools/run_graybox_check.py` |
| Base Git SHA | `d561353fcd58f3837cbe934debc56b248c1fde9e` |
| Container image | `python:3.12` |
| Container image ID | `37ee34ed0a73271658c2a4ae71c0eff28365ed150c0e8421bbd105f13d5d22a7` |
| Container network | `none` |
| Workspace mount during execution | read-only |
| Artifact digest verification | local and remote archive SHA-256 must match |
| Preparation network | enabled only to install locked dependencies before execution |
| Execution command | `make UV=/workspace/.venv/bin/uv check` |
| Execution result | PASS |
| Isolated rerun result | PASS |
| Rerun consistency | both invocations returned zero |
| Unit tests | 45 passed |
| Property tests | 4 passed |
| Negative qualification | all expected failures observed |

This runner is exercised by `make check` and by `tools/run_graybox_check.py`.
The integration test `tests/integration/test_graybox_seat_plan.py` verifies
that a seat plan containing the graybox executioner passes the cross-vendor
mechanical gate before execution.

## Boundary

This proves deterministic executioner runtime isolation and exact artifact
transfer for the local graybox path. It does not prove AWS AgentCore IAM
separation, sealed holdout storage, or model-provider independence.
