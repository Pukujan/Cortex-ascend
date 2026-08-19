from __future__ import annotations

from cortex_ascend.kernel import (
    ArtifactDigest,
    AuditCase,
    AuditOutcome,
    AuthorityGrant,
    Decision,
    EvidenceReceipt,
    FossilReceipt,
    GateMode,
    GatePolicy,
    Generation,
    ProjectSnapshot,
    WorkContract,
    WorkId,
    any_false_admit,
    audit,
    audit_corpus,
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


def test_audit_match_for_valid_contract() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    contract = _valid_contract(generation=1, base_commit="b")
    case = AuditCase(
        case_id="valid",
        contract=contract,
        current_base=base,
        expected=Decision.ADMIT,
        category="positive",
    )
    result = audit(case)
    assert result.outcome == AuditOutcome.MATCH


def test_audit_false_admit_for_stale_contract() -> None:
    new = ProjectSnapshot(commit="new", tree_hash="new")
    contract = _valid_contract(generation=1, base_commit="old")
    case = AuditCase(
        case_id="stale",
        contract=contract,
        current_base=new,
        expected=Decision.STALE,
        category="stale",
    )
    result = audit(case)
    assert result.outcome == AuditOutcome.MATCH


def test_audit_false_admit_for_model_mismatch() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    contract = _valid_contract(
        generation=1, base_commit="b", requested_model="m1", actual_model="m2"
    )
    case = AuditCase(
        case_id="mismatch",
        contract=contract,
        current_base=base,
        expected=Decision.REJECT,
        category="model-mismatch",
    )
    result = audit(case)
    assert result.outcome == AuditOutcome.MATCH


def test_corpus_detects_false_admit() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    valid = AuditCase(
        case_id="valid",
        contract=_valid_contract(generation=1, base_commit="b"),
        current_base=base,
        expected=Decision.ADMIT,
        category="positive",
    )
    mismatch = AuditCase(
        case_id="mismatch",
        contract=_valid_contract(
            generation=1, base_commit="b", requested_model="m1", actual_model="m2"
        ),
        current_base=base,
        expected=Decision.REJECT,
        category="model-mismatch",
    )
    results = audit_corpus((valid, mismatch))
    assert not any_false_admit(results)


def test_gate_policy_blocks_promotion_with_false_admits() -> None:
    base = ProjectSnapshot(commit="b", tree_hash="b")
    # Ascend sees a valid contract, but external oracle knows it should be rejected.
    bad = AuditCase(
        case_id="bad",
        contract=_valid_contract(generation=1, base_commit="b"),
        current_base=base,
        expected=Decision.REJECT,
        category="false-positive",
    )
    results = audit_corpus((bad,))
    policy = GatePolicy(mode=GateMode.AUDIT, break_glass_authority="owner")
    assert not policy.can_promote(results)
    assert any_false_admit(results)


def test_fossil_receipt_placeholder_not_real() -> None:
    receipt = FossilReceipt(receipt_id="r1", status="pending")
    assert not receipt.is_real()
