# G0 CI and provenance fixtures

These fixtures are deliberately invalid. The provenance negative harnesses are
green only when each bad input is rejected for its declared reason.

- `fixtures/workflows/movable_action_tag.yml`: third-party Action referenced by a movable tag.
- `fixtures/workflows/excessive_permissions.yml`: workflow permissions are not minimal.
- `fixtures/workflows/unfrozen_uv.yml`: CI invokes `uv run` without `--frozen`.
- `fixtures/workflows/long_lived_aws_keys.yml`: long-lived AWS keys instead of OIDC.
- `fixtures/secrets/seeded_fake_credential.txt`: documented fake credential material.

The live workflows under `.github/workflows/` are checked separately.
The seeded fake credential is excluded from the positive repository scan.
