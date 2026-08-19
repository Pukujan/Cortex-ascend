from __future__ import annotations

from cortex_ascend.kernel.contract import WorkContract
from cortex_ascend.kernel.serialization import canonical_hash
from cortex_ascend.kernel.types import (
    AdmissionDecision,
    ArtifactDigest,
    Decision,
    ProjectSnapshot,
)


def is_fresh(contract: WorkContract, current_base: ProjectSnapshot) -> bool:
    """True when the contract's base matches the current project snapshot.

    Stale-base evidence cannot satisfy current work (ASC-INV-KRN-001).
    """
    return contract.base == current_base


def has_authority(contract: WorkContract) -> bool:
    """True when the contract carries a non-empty authority grant."""
    return bool(contract.authority.issuer and contract.authority.grant_id)


def is_evidence_bound(contract: WorkContract) -> bool:
    """True when every evidence receipt names the contract's work id.

    Evidence for one artifact cannot admit another artifact (ASC-INV-KRN-003).
    For now we require the authority field of each receipt to contain the
    work id; future versions may use a dedicated binding field.
    """
    return all(contract.work_id.value in receipt.authority for receipt in contract.evidence)


def model_identity_compatible(contract: WorkContract) -> bool:
    """True when the actual model identity matches the requested one.

    Unexpected model substitution cannot satisfy an exact-model seat
    (ASC-INV-MDL-002).
    """
    actual: str | None = contract.metadata.get("actual_model")
    if actual is None:
        return False
    return actual == contract.requested_model


def adjudicate(contract: WorkContract) -> AdmissionDecision:
    """Render a deterministic admission decision for a contract.

    This is a pure predicate; it does not consult external oracles. Worker
    claims do not constitute qualification evidence (G1-G2 constraint).
    """
    if not has_authority(contract):
        return contract.decide(Decision.REJECT, "missing authority grant")
    if not contract.evidence:
        return contract.decide(Decision.REJECT, "no evidence receipts attached")
    if not is_evidence_bound(contract):
        return contract.decide(Decision.REJECT, "evidence not bound to this work id")
    if not model_identity_compatible(contract):
        return contract.decide(Decision.REJECT, "requested vs actual model identity mismatch")
    return contract.decide(Decision.ADMIT, "all pure predicates satisfied")


def adjudicate_against_base(
    contract: WorkContract, current_base: ProjectSnapshot
) -> AdmissionDecision:
    """Adjudicate a contract against the current project base.

    If the base has moved on, the contract is STALE regardless of other
    predicates.
    """
    if not is_fresh(contract, current_base):
        return contract.decide(Decision.STALE, "contract base does not match current snapshot")
    return adjudicate(contract)


def decision_digest(decision: AdmissionDecision) -> ArtifactDigest:
    """Canonical digest of an admission decision."""
    return ArtifactDigest(algorithm="sha256", hex=canonical_hash(decision))
