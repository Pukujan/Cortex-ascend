from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Decision(Enum):
    """Admission decision values for a WorkContract."""

    ADMIT = "ADMIT"
    REJECT = "REJECT"
    STALE = "STALE"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ProjectSnapshot:
    """An immutable point-in-time view of project state used as a work base."""

    commit: str
    tree_hash: str
    # Human-readable description; not part of canonical identity.
    description: str = ""


@dataclass(frozen=True)
class WorkId:
    """Opaque identifier for a unit of work."""

    value: str


@dataclass(frozen=True)
class Generation:
    """Monotonic generation counter for a lineage of work."""

    value: int

    def next(self) -> Generation:
        return Generation(self.value + 1)


@dataclass(frozen=True)
class ArtifactDigest:
    """Cryptographic identity of an artifact."""

    algorithm: str
    hex: str


@dataclass(frozen=True)
class AuthorityGrant:
    """A scoped authorization to admit or reject work."""

    issuer: str
    scope: str
    # Opaque grant token; the kernel treats it as an identity string.
    grant_id: str


@dataclass(frozen=True)
class ModelIdentity:
    """Requested vs actual model identity for a piece of work."""

    requested: str
    actual: str | None = None

    def compatible(self) -> bool:
        """True when actual identity is known and matches the requested identity."""
        return self.actual is not None and self.actual == self.requested


@dataclass(frozen=True)
class EvidenceReceipt:
    """A machine-readable receipt that some predicate was satisfied."""

    predicate: str
    artifact_digest: ArtifactDigest
    # The generation at which the evidence was produced.
    generation: Generation
    # Canonical identity of the authority that issued the receipt.
    authority: str
    # Human-readable note; not part of canonical identity.
    note: str = ""


@dataclass(frozen=True)
class AdmissionDecision:
    """Result of adjudicating a WorkContract."""

    decision: Decision
    contract_digest: ArtifactDigest
    reason: str
    # The generation at which the decision was rendered.
    generation: Generation
