from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from cortex_ascend.kernel import (
    ArtifactDigest,
    AuthorityGrant,
    Decision,
    EvidenceReceipt,
    Generation,
    Lifecycle,
    ProjectSnapshot,
    WorkContract,
    WorkId,
)


def _valid_contract(
    work_id: str = "w1",
    generation: int = 1,
    base_commit: str = "base",
    requested_model: str = "m1",
    actual_model: str = "m1",
) -> WorkContract:
    return WorkContract(
        work_id=WorkId(work_id),
        generation=Generation(generation),
        requested_model=requested_model,
        base=ProjectSnapshot(commit=base_commit, tree_hash=base_commit),
        authority=AuthorityGrant("owner", "admit", "g1"),
        metadata={"actual_model": actual_model},
    ).with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(generation),
            authority=f"owner-{work_id}",
        )
    )


def test_stale_generation_cannot_admit() -> None:
    old_base = ProjectSnapshot(commit="old", tree_hash="old")
    new_base = ProjectSnapshot(commit="new", tree_hash="new")

    lifecycle = Lifecycle(current_base=old_base)
    lifecycle = lifecycle.start_attempt(Generation(1))
    contract = _valid_contract(generation=1, base_commit="old")
    lifecycle = lifecycle.complete_attempt(Generation(1), contract)

    # Base advances; the old completed attempt must not be considered current.
    lifecycle = lifecycle.replace_base(new_base)
    assert lifecycle.current_generation == Generation(1)
    assert not lifecycle.any_admit_from_stale_generation()


def test_revoked_grant_does_not_admit() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    lifecycle = Lifecycle(current_base=base)
    lifecycle = lifecycle.start_attempt(Generation(1))
    lifecycle = lifecycle.revoke_grant("g1")
    contract = _valid_contract(generation=1, base_commit="b")
    lifecycle = lifecycle.complete_attempt(Generation(1), contract)
    assert lifecycle.attempts[1].decision is not None
    assert lifecycle.attempts[1].decision.decision != Decision.ADMIT


@given(st.integers(min_value=0, max_value=100), st.integers(min_value=0, max_value=100))
def test_advance_generation_monotonic(old: int, new: int) -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    lifecycle = Lifecycle(current_base=base, current_generation=Generation(old))
    lifecycle = lifecycle.replace_base(ProjectSnapshot(commit="c", tree_hash="c"))
    assert lifecycle.current_generation.value == old + 1


def test_replayed_old_result_still_stale() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    lifecycle = Lifecycle(current_base=base)
    lifecycle = lifecycle.start_attempt(Generation(1))
    contract = _valid_contract(generation=1, base_commit="b")
    lifecycle = lifecycle.complete_attempt(Generation(1), contract)
    # Simulate duplicate delivery of the same old contract after base advance.
    lifecycle = lifecycle.replace_base(ProjectSnapshot(commit="c", tree_hash="c"))
    lifecycle = lifecycle.start_attempt(Generation(1))
    lifecycle = lifecycle.complete_attempt(Generation(1), contract)
    assert not lifecycle.any_admit_from_stale_generation()
