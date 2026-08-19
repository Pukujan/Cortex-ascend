from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class SeatRole(Enum):
    """Adversarial/red-team seat roles for G6-G7."""

    RED_ARCH = "RED_ARCH"
    RED_SEC = "RED_SEC"
    RED_DIST = "RED_DIST"
    MUTANT = "MUTANT"
    FORMAL_ADV = "FORMAL_ADV"
    CHAOS_PLAN = "CHAOS_PLAN"


@dataclass(frozen=True)
class SeatIdentity:
    """Independence metadata for a model seat.

    This is a structured claim, not a cryptographic proof. It exists so that
    admission evidence can record who produced a finding and whether the
    required independence vectors were satisfied.
    """

    role: SeatRole
    vendor: str
    model: str
    provider: str
    account: str
    transport: str
    context: str
    runtime: str
    credentials: str
    holdout_visibility: str
    controller: str


@dataclass(frozen=True)
class AttackHypothesis:
    """A model-generated attack hypothesis converted into executable form."""

    hypothesis_id: str
    seat: SeatIdentity
    target_invariant: str
    description: str
    # Opaque normalized form for deduplication.
    fingerprint: str


@dataclass(frozen=True)
class HoldoutItem:
    """Reference to a sealed holdout case.

    The public repository stores only identity, version, count, and hash.
    Actual case/answer material lives in verifier-controlled storage.
    """

    item_id: str
    version: str
    answer_hash: str


@dataclass(frozen=True)
class HoldoutSuite:
    """A sealed holdout suite."""

    suite_id: str
    count: int
    items: tuple[HoldoutItem, ...]

    def fingerprint(self) -> str:
        return f"{self.suite_id}@{self.count}:" + ",".join(
            f"{item.item_id}#{item.version}:{item.answer_hash}" for item in self.items
        )


@dataclass(frozen=True)
class ChaosFault:
    """A declared chaos fault with expected outcome and target invariant."""

    fault_id: str
    schedule: str
    target_invariant: str
    expected_outcome: str


@dataclass(frozen=True)
class RedTeamReceipt:
    """Receipt that a red-team seat produced a finding or attack hypothesis."""

    seat: SeatIdentity
    hypothesis: AttackHypothesis
    # Deterministic harness result, if executed.
    harness_result: str | None = None
