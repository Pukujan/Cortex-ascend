# G0.9 — Consolidated Adversarial Negative Foundation Qualification

## Requirement
- ASC-G0-R10: foundation invariants are qualified by deliberately seeded failures
  that are rejected for their declared reasons.

## Negative qualification corpus

| # | Class | Fixture / synthetic input | Checker | Expected diagnostic | Requirement | Invariant |
|---|-------|---------------------------|---------|---------------------|-------------|-----------|
| 1 | Prohibited kernel import | `tests/architecture/fixtures/prohibited_kernel_import` | `check_architecture_negative.py` | `prohibited kernel third-party import: boto3` | ASC-G0-R4 | FND-001 |
| 2 | Reverse layer import | `tests/architecture/fixtures/reverse_layer_import` | `check_architecture_negative.py` | `forbidden layer import: kernel -> application` | ASC-G0-R4 | FND-001 |
| 3 | Architecture cycle | `tests/architecture/fixtures/architecture_cycle` | `check_architecture_negative.py` | `architecture cycle:` containing `application` and `ports` | ASC-G0-R4 | FND-001 |
| 4 | Ruff lint failure | `tests/static/fixtures/ruff_unused_import.py` | `check_static_negative.py` | `F401` | ASC-G0-R3 | FND-002 |
| 5 | Mypy strict failure | `tests/static/fixtures/mypy_return_type.py` | `check_static_negative.py` | `Incompatible return value type` | ASC-G0-R3 | FND-002 |
| 6 | Deterministic test failure | `tests/test_harness_fixtures/deterministic_failure` | `check_test_negative.py` | `seeded deterministic failure` | ASC-G0-R5 | FND-002 |
| 7 | Hypothesis counter-example | `tests/test_harness_fixtures/property_failure` | `check_test_negative.py` | `Failing test case` containing `value=0` | ASC-G0-R5 | FND-002 |
| 8 | Stale generated handoff docs | synthetic stale `handoff.yaml` | `check_docs_negative.py` | `generated handoff facts are stale` | ASC-G0-R7 | FND-003 |
| 9 | Malformed handoff manifest | `tests/docs/fixtures/missing_current_gate` | `check_docs_negative.py` | `missing mapping 'current_gate'` | ASC-G0-R7 | FND-003 |
| 10 | Incomplete PR contract | `tests/docs/fixtures/pr_missing_requirements.md` | `check_docs_negative.py` | `missing required PR section: Requirement IDs` | ASC-G0-R7 | FND-003 |
| 11 | Movable Action tag | `tests/ci/fixtures/workflows/movable_action_tag.yml` | `check_github_workflows_negative.py` | `movable Action tag or non-SHA pin` | ASC-G0-R6 | FND-005 |
| 12 | Excessive workflow permissions | `tests/ci/fixtures/workflows/excessive_permissions.yml` | `check_github_workflows_negative.py` | `excessive permissions` | ASC-G0-R6 | FND-005 |
| 13 | Unfrozen `uv run` | `tests/ci/fixtures/workflows/unfrozen_uv.yml` | `check_github_workflows_negative.py` | `unfrozen uv run` | ASC-G0-R6 | FND-005 |
| 14 | Long-lived AWS keys | `tests/ci/fixtures/workflows/long_lived_aws_keys.yml` | `check_github_workflows_negative.py` | `long-lived AWS credential path` | ASC-G0-R6 | FND-005 |
| 15 | Seeded fake credential | `tests/ci/fixtures/secrets/seeded_fake_credential.txt` | `check_secrets_negative.py` | `aws-access-key-id` and `github-pat` | ASC-G0-R6 | FND-004 |
| 16 | Package-root third-party import | `tests/architecture/fixtures/package_root_third_party` | `check_architecture_negative.py` | `prohibited package-root third-party import: boto3` | ASC-G0-R4 | FND-001 |

## Machine-readable receipt
`tests/ci/negative_receipt.yaml` contains the same mapping in a structured form for future tooling.

## Harness integration
Each negative checker is invoked by `make check` after its positive counterpart:
- `tools/check_architecture_negative.py`
- `tools/check_static_negative.py`
- `tools/check_test_negative.py`
- `tools/check_docs_negative.py`
- `tools/check_github_workflows_negative.py`
- `tools/check_secrets_negative.py`

The negative harness is green only when every seeded bad case is correctly rejected.

## Verification
- `make check` passes on the normal repository tree.
- Each negative checker reports the expected number of expected failures.

## Related work
- Parent: #1
- Depends on: #8, #9, #10, #11, #12, #13, #14
- Addresses: ASC-G0-R10
