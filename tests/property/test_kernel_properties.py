from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from cortex_ascend.kernel import (
    ArtifactDigest,
    Decision,
    EvidenceReceipt,
    Generation,
    ProjectSnapshot,
    WorkContract,
    WorkId,
    adjudicate,
    canonical_hash,
    is_fresh,
)

st_work_id = st.builds(WorkId, value=st.text())
st_generation = st.builds(Generation, value=st.integers(min_value=0, max_value=1_000_000))
st_snapshot = st.builds(
    ProjectSnapshot,
    commit=st.text(),
    tree_hash=st.text(),
    description=st.text(),
)


@given(st_work_id, st_generation)
def test_canonical_hash_respects_identity(work_id: WorkId, generation: Generation) -> None:
    a = WorkContract(work_id=work_id, generation=generation)
    b = WorkContract(work_id=work_id, generation=generation)
    assert canonical_hash(a) == canonical_hash(b)


@given(st_snapshot, st_snapshot)
def test_freshness_is_equality(base: ProjectSnapshot, other: ProjectSnapshot) -> None:
    contract = WorkContract(base=base)
    assert is_fresh(contract, base)
    if base != other:
        assert not is_fresh(contract, other)


@given(st.text(), st.text(), st.text())
def test_evidence_binding_requires_work_id(work_id: str, authority: str, predicate: str) -> None:
    contract = WorkContract(work_id=WorkId(work_id)).with_evidence(
        EvidenceReceipt(
            predicate=predicate,
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(0),
            authority=authority,
        )
    )
    decision = adjudicate(contract)
    if work_id in authority:
        assert decision.decision != Decision.REJECT or "model" not in decision.reason
    else:
        assert decision.decision == Decision.REJECT
