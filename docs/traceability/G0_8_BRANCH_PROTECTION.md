# G0.8 — CODEOWNERS, Protected Main, and Required Checks

## Requirement
- ASC-G0-R8: repository controls enforce the G0 qualification gate before merge to `main`.

## What was changed
1. Added `.github/CODEOWNERS` assigning ownership of frozen architecture documents,
   CI/provenance configuration, toolchain lockfiles, and admission tooling to
   `@Pukujan`, with a wildcard fallback for remaining paths.
2. Enabled branch protection for `main` via the GitHub REST API.

## Branch protection state (mechanically re-read)

```json
{
  "allow_deletions": false,
  "allow_force_pushes": false,
  "contexts": ["check", "security-provenance"],
  "required_approving_review_count": 0,
  "strict": true
}
```

- **Require branches to be up to date before merging**: enabled (`strict: true`).
- **Required status checks**: `check`, `security-provenance`.
- **Require pull request reviews before merging**: disabled (`required_approving_review_count: 0`).
- **Allow force pushes**: disabled.
- **Allow deletions**: disabled.
- **Admin enforcement**: not enabled, so repository owner retains break-glass override.

## Required check identity
- Workflow `check.yml` defines a single job named `check`.
- Workflow `security-provenance.yml` defines a single job named `security-provenance`.
- These names are stable and match the required contexts configured above.

## Evidence of enforcement
- PR #29 (this change) passed both checks before merge.
- After merge, branch protection was applied and verified via `gh api`.

## Negative/evidence notes
- Direct pushes to `main` are now blocked unless checks pass.
- A controlled PR with an intentionally failing required check has not been run
  to avoid polluting `main` history; mechanical non-mergeability follows from
  GitHub's required-status-check semantics.

## Trust / architecture boundary
GitHub repository controls are now part of the active bootstrap root of trust.
Administrative override remains possible because the repository owner is the
sole bootstrap authority; this is an unavoidable infrastructure constraint
(documented in #17 Finding 10).

## Related work
- Parent: #1
- Depends on: #13
- Addresses findings: #17 Findings 1, 2, 6, 19, 30, 31.
