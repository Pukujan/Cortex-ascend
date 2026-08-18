# Architecture Decision Records

ADRs capture consequential architecture or trust-boundary decisions without replacing the frozen canonical plan.

## Naming

Use `NNNN-short-title.md`, starting with `0001`. Keep `0000-template.md` as the template only.

## Required fields

- Status: `proposed`, `accepted`, `superseded`, or `rejected`.
- Date.
- Context.
- Decision.
- Consequences.
- Requirement/invariant references.
- Architecture-reopening trigger, when applicable.

Architecture remains frozen during G0. An ADR may document an implementation choice inside the frozen constraints; it cannot reopen architecture unless one of the canonical reopening triggers is actually present.
