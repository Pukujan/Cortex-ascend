from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from cortex_ascend.kernel.types import (
    AdmissionDecision,
    ArtifactDigest,
    AuthorityGrant,
    Decision,
    EvidenceReceipt,
    Generation,
    ModelIdentity,
    ProjectSnapshot,
    WorkId,
)


@dataclass(frozen=True)
class WorkContract:
    """Version 1 of an addressable, adjudicated work envelope.

    A WorkContract is not semantic truth; it is a bundle of claims about a
    piece of work, its base, the evidence that supports it, and the authority
    that may admit it.
    """

    version: int = 1
    work_id: WorkId = field(default_factory=lambda: WorkId(""))
    generation: Generation = field(default_factory=lambda: Generation(0))
    base: ProjectSnapshot = field(default_factory=lambda: ProjectSnapshot(commit="", tree_hash=""))
    requested_model: str = ""
    worker_claims: tuple[str, ...] = ()
    evidence: tuple[EvidenceReceipt, ...] = ()
    authority: AuthorityGrant = field(
        default_factory=lambda: AuthorityGrant(issuer="", scope="", grant_id="")
    )
    # Free-form metadata; must not affect canonical identity.
    metadata: dict[str, Any] = field(default_factory=dict, compare=False)

    def with_model_identity(self, model: ModelIdentity) -> WorkContract:
        """Return a new contract with actual model identity recorded."""
        return WorkContract(
            version=self.version,
            work_id=self.work_id,
            generation=self.generation,
            base=self.base,
            requested_model=model.requested,
            worker_claims=self.worker_claims,
            evidence=self.evidence,
            authority=self.authority,
            metadata={**self.metadata, "actual_model": model.actual},
        )

    def with_evidence(self, *receipts: EvidenceReceipt) -> WorkContract:
        """Return a new contract with additional evidence attached."""
        return WorkContract(
            version=self.version,
            work_id=self.work_id,
            generation=self.generation,
            base=self.base,
            requested_model=self.requested_model,
            worker_claims=self.worker_claims,
            evidence=(*self.evidence, *receipts),
            authority=self.authority,
            metadata=self.metadata,
        )

    def decide(self, decision: Decision, reason: str) -> AdmissionDecision:
        """Render an admission decision bound to this contract's identity."""
        from cortex_ascend.kernel.serialization import canonical_hash

        return AdmissionDecision(
            decision=decision,
            contract_digest=ArtifactDigest(algorithm="sha256", hex=canonical_hash(self)),
            reason=reason,
            generation=self.generation,
        )
