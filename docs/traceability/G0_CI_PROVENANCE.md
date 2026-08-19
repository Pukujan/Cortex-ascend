# G0 CI and Provenance Traceability

## Contract

Requirement IDs: `ASC-G0-R6`, `ASC-G0-R7`  
Invariants: `ASC-INV-FND-002`, `ASC-INV-FND-004`, `ASC-INV-FND-005`

GitHub Actions is an explicit member of the G0 bootstrap trusted computing base.
It does not introduce AWS runtime authority.

## Workflow identities

Required check names for later branch protection (#14):

| Workflow file | Job `name` | Check name |
|---|---|---|
| `.github/workflows/check.yml` | `check` | `check` |
| `.github/workflows/security-provenance.yml` | `security-provenance` | `security-provenance` |

`check` invokes the same `make check` graph as local development. It does not
reimplement qualification as a divergent step list.

## Runtime

Both workflows pin CPython **3.12** through `astral-sh/setup-uv` and assert
`sys.version_info[:2] == (3, 12)` before qualification. `.python-version`
records `3.12` as the local default. Newer interpreters may exist on developer
machines; they cannot replace the 3.12 CI receipt.

## Provenance controls

- Third-party Actions are pinned to full 40-character commit SHAs.
- Workflow `permissions` are explicit and minimal (`contents: read`).
- `persist-credentials: false` on checkout.
- `fetch-depth: 0` so history-sensitive scans see the commit graph.
- Project tools run through `uv run --frozen`; unlocked `pip install` is
  rejected.
- uv itself is version-pinned (`0.12.5`) with a linux-x86_64 checksum on CI.

## Future AWS credential path

Normal CI does not use AWS. Long-lived `AWS_ACCESS_KEY_ID` /
`AWS_SECRET_ACCESS_KEY` / `AWS_SESSION_TOKEN` values are forbidden in
workflows. When AWS is later required, the only permitted path is GitHub OIDC
(`id-token: write` plus `role-to-assume`). `id-token: write` without an OIDC
role is itself a policy failure.

## Secret and history scanning

`tools/check_secrets.py` scans tracked files and git history for credential
shapes, including AWS access-key IDs, GitHub PATs, and private-key sentinels.
The only allowlisted occurrence is the documented fake fixture under
`tests/ci/fixtures/secrets/`.

## Deliberate negatives

```text
python tools/check_github_workflows.py
python tools/check_github_workflows_negative.py
python tools/check_secrets.py
python tools/check_secrets_negative.py
```

Expected-failure fixtures reject a movable Action tag, excessive permissions,
an unfrozen `uv run`, long-lived AWS keys, and a seeded fake credential.

## G0 boundary

This lane qualifies CI/provenance controls. It does not enable protected-main
required checks (#14), consolidate the full negative corpus (#15), or close G0
(#18). Green CI is qualification-grade for this lane only after these
workflows are the required checks on the protected commit.
