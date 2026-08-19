from __future__ import annotations

from copy import deepcopy

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
)


def _valid_contract() -> WorkContract:
    return WorkContract(
        work_id=WorkId("w1"),
        generation=Generation(1),
        requested_model="m1",
        base=ProjectSnapshot(commit="abc", tree_hash="def"),
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


def test_mutant_missing_authority_is_rejected() -> None:
    contract = _valid_contract()
    mutant = deepcopy(contract)
    mutant = WorkContract(
        version=mutant.version,
        work_id=mutant.work_id,
        generation=mutant.generation,
        base=mutant.base,
        requested_model=mutant.requested_model,
        worker_claims=mutant.worker_claims,
        evidence=mutant.evidence,
        authority=AuthorityGrant("", "", ""),
        metadata=mutant.metadata,
    )
    assert adjudicate(mutant).decision == Decision.REJECT


def test_mutant_unbound_evidence_is_rejected() -> None:
    contract = _valid_contract()
    mutant = contract.with_evidence(
        EvidenceReceipt(
            predicate="test",
            artifact_digest=ArtifactDigest("sha256", "00"),
            generation=Generation(1),
            authority="other-work",
        )
    )
    assert adjudicate(mutant).decision == Decision.REJECT


def test_mutant_model_substitution_is_rejected() -> None:
    contract = _valid_contract()
    mutant = contract.with_model_identity(ModelIdentity("m1", "m2"))
    assert adjudicate(mutant).decision == Decision.REJECT


def test_mutant_stale_base_is_stale() -> None:
    contract = _valid_contract()
    new_base = ProjectSnapshot(commit="xyz", tree_hash="xyz")
    decision = adjudicate_against_base(contract, new_base)
    assert decision.decision == Decision.STALE


def test_mutant_empty_evidence_is_rejected() -> None:
    contract = _valid_contract()
    mutant = WorkContract(
        version=contract.version,
        work_id=contract.work_id,
        generation=contract.generation,
        base=contract.base,
        requested_model=contract.requested_model,
        worker_claims=contract.worker_claims,
        evidence=(),
        authority=contract.authority,
        metadata=contract.metadata,
    )
    assert adjudicate(mutant).decision == Decision.REJECT
