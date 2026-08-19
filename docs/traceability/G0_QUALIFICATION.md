# G0 Qualification Command

## Contract

Requirement: `ASC-G0-R2`, `ASC-G0-R3`, `ASC-G0-R4`, `ASC-G0-R5`  
Invariants: `ASC-INV-FND-001`, `ASC-INV-FND-002`, `ASC-INV-FND-003`, `ASC-INV-FND-005`

`make check` is the single local/CI G0 qualification entrypoint. It runs the
same ordered graph in every environment and stops at the first non-zero gate:

1. `uv lock --check` verifies that `pyproject.toml` and the committed `uv.lock`
   are synchronized.
2. Locked Ruff format and lint checks run over the repository.
3. Locked strict Mypy checks run over `src/cortex_ascend` and `tools`.
4. The executable architecture-boundary check runs against `src`.
5. Locked unit and property-test baselines run separately.
6. The handoff manifest and generated documentation consistency gate runs.
7. GitHub Actions workflow-policy and credential/history scans run.
8. `uv pip check` verifies installed dependency compatibility.
9. Architecture, static, test-harness, documentation, workflow-policy, and
   secret-scan deliberate-negative harnesses each prove that their invalid
   fixtures fail with expected diagnostics.

All project tools are invoked through `uv run --frozen`; the lockfile is an
existing resolved artifact and is never generated or edited by this target.
The negative harnesses intentionally run failing child commands, but return
success only when each child fails as expected. A direct failure in any
positive or negative harness therefore propagates as a failed `make check`.

## G0 boundary

This target qualifies the foundation command graph, including the local
equivalents of CI/provenance policy checks added by #13. It does not add
semantic kernel behavior or claim protected-main, consolidated-negative,
independent-critic, or final-G0-exit evidence owned by later G0 issues.
