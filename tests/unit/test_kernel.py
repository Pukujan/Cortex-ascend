from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from cortex_ascend.kernel import (
    ArtifactDigest,
    AuthorityGrant,
    Decision,
    EvidenceReceipt,
    Generation,
    ModelIdentity,
    ProjectSnapshot,
    WorkContract,
    WorkId,
    adjudicate,
    adjudicate_against_base,
    canonical_hash,
    canonical_json,
    decision_digest,
    is_evidence_bound,
    is_fresh,
)


def test_generation_monotonic() -> None:
    g = Generation(3)
    assert g.next() == Generation(4)


def test_model_identity_compatibility() -> None:
    assert ModelIdentity("litellm/grok-4.6", "litellm/grok-4.6").compatible()
    assert not ModelIdentity("litellm/grok-4.6", "litellm/qwen3.6-plus").compatible()
    assert not ModelIdentity("litellm/grok-4.6").compatible()


def test_canonical_hash_stable_and_deterministic() -> None:
    snapshot = ProjectSnapshot(commit="abc123", tree_hash="def456")
    first = canonical_hash(snapshot)
    second = canonical_hash(snapshot)
    assert first == second
    assert len(first) == 64


def test_metadata_does_not_affect_canonical_hash() -> None:
    base = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        metadata={"note": "first"},
    )
    mutated = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        metadata={"note": "second"},
    )
    assert canonical_hash(base) == canonical_hash(mutated)


def test_material_changes_alter_hash() -> None:
    first = WorkContract(work_id=WorkId("w1"), generation=Generation(1))
    second = WorkContract(work_id=WorkId("w1"), generation=Generation(2))
    assert canonical_hash(first) != canonical_hash(second)


def test_adjudicate_rejects_missing_authority() -> None:
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        requested_model="m1",
        metadata={"actual_model": "m1"},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="w1",
        )
    )
    decision = adjudicate(contract)
    assert decision.decision == Decision.REJECT
    assert "authority" in decision.reason


def test_adjudicate_admits_valid_contract() -> None:
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        requested_model="m1",
        authority=AuthorityGrant("owner", "admit", "g1"),
        metadata={"actual_model": "m1"},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="owner-w1",
        )
    )
    decision = adjudicate(contract)
    assert decision.decision == Decision.ADMIT


def test_evidence_binding_rejects_unbound_receipt() -> None:
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="other-work",
        )
    )
    assert not is_evidence_bound(contract)
    decision = adjudicate(contract)
    assert decision.decision == Decision.REJECT


def test_model_identity_mismatch_rejected() -> None:
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        requested_model="m1",
        authority=AuthorityGrant("owner", "admit", "g1"),
        metadata={"actual_model": "m2"},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="w1",
        )
    )
    decision = adjudicate(contract)
    assert decision.decision == Decision.REJECT
    assert "model" in decision.reason


def test_stale_base_decision() -> None:
    old = ProjectSnapshot(commit="old", tree_hash="old")
    new = ProjectSnapshot(commit="new", tree_hash="new")
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        base=old,
        requested_model="m1",
        authority=AuthorityGrant("owner", "admit", "g1"),
        metadata={"actual_model": "m1"},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="w1",
        )
    )
    assert is_fresh(contract, old)
    decision = adjudicate_against_base(contract, new)
    assert decision.decision == Decision.STALE


def test_decision_digest_stable() -> None:
    contract = WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        requested_model="m1",
        authority=AuthorityGrant("owner", "admit", "g1"),
        metadata={"actual_model": "m1"},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="w1",
        )
    )
    decision = adjudicate(contract)
    digest = decision_digest(decision)
    assert digest.algorithm == "sha256"
    assert len(digest.hex) == 64


@given(st.integers(min_value=0, max_value=10_000))
def test_generation_next_is_greater(n: int) -> None:
    g = Generation(n)
    assert g.next().value == n + 1


@given(st.text(), st.text())
def test_canonical_json_is_ascii(requested: str, actual: str) -> None:
    model = ModelIdentity(requested, actual)
    encoded = canonical_json(model)
    assert encoded.isascii()
    assert encoded == canonical_json(ModelIdentity(requested, actual))
