# ADR 0001 — Provenance-conscious GitHub Actions for G0

- **Status:** accepted
- **Date:** 2026-08-18
- **Requirement / invariant references:** `ASC-G0-R6`, `ASC-G0-R7`, `ASC-INV-FND-002`, `ASC-INV-FND-004`, `ASC-INV-FND-005`
- **Architecture reopening trigger:** none

## Context

G0 requires GitHub Actions to become part of the bootstrap trusted computing
base without introducing AWS runtime authority. A green badge is not
qualification-grade evidence if Actions float, permissions are implicit, or
dependencies are unlocked.

## Decision

- Use two stable workflow/check names: `check` and `security-provenance`.
- Make `check` call `make check` rather than a second command graph.
- Pin third-party Actions to full commit SHAs and uv to `0.12.5`.
- Run the qualification path on CPython 3.12.
- Keep workflow permissions at `contents: read`.
- Forbid long-lived AWS keys; document GitHub OIDC as the only future AWS
  credential path and reject `id-token: write` without `role-to-assume`.
- Enforce these rules with stdlib checkers plus deliberate negative fixtures,
  including a seeded fake credential that is never a real secret.

## Consequences

- `#14` can require the names `check` and `security-provenance`.
- Local `make check` now includes the same workflow/secret policy gates CI
  runs, preserving `ASC-INV-FND-002` for this lane.
- No AWS role is assumed in G0; OIDC is a constrained future path, not a live
  cloud login.

## Evidence

See `docs/traceability/G0_CI_PROVENANCE.md`.
