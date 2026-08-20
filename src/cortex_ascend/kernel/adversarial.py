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
    model_family: str
    provider: str
    account: str
    transport: str
    context: str
    runtime: str
    credentials: str
    holdout_visibility: str
    controller: str


@dataclass(frozen=True)
class SeatAssignment:
    """Requested and actual identity for one pre-inference model seat."""

    requested: SeatIdentity
    actual: SeatIdentity
    actual_authorized: bool = False


@dataclass(frozen=True)
class SeatPlan:
    """Cross-vendor producer, red-team, and executioner assignment."""

    producer: SeatAssignment
    red_teams: tuple[SeatAssignment, ...]
    executioner: SeatAssignment


class SeatAssignmentError(ValueError):
    """Raised when an adversarial seating plan violates independence policy."""


def _same_vendor_or_family(left: SeatIdentity, right: SeatIdentity) -> bool:
    return left.vendor == right.vendor or left.model_family == right.model_family


def _actual_identity_is_authorized(assignment: SeatAssignment) -> bool:
    return assignment.actual.model == assignment.requested.model or assignment.actual_authorized


def validate_seat_plan(plan: SeatPlan) -> None:
    """Reject a plan before inference when required independent seats overlap."""
    assignments = (plan.producer, *plan.red_teams, plan.executioner)
    if len(plan.red_teams) < 2:
        raise SeatAssignmentError("at least two red-team seats are required")
    if any(not _actual_identity_is_authorized(assignment) for assignment in assignments):
        raise SeatAssignmentError("actual model identity differs without explicit authorization")

    producer = plan.producer.actual
    executioner = plan.executioner.actual
    if _same_vendor_or_family(producer, executioner):
        raise SeatAssignmentError("producer and executioner must differ by vendor and model family")

    for red_team in plan.red_teams:
        if _same_vendor_or_family(producer, red_team.actual):
            raise SeatAssignmentError(
                "producer and red-team seats must differ by vendor and model family"
            )
        if _same_vendor_or_family(executioner, red_team.actual):
            raise SeatAssignmentError(
                "executioner and red-team seats must differ by vendor and model family"
            )

    for index, red_team in enumerate(plan.red_teams):
        for other in plan.red_teams[index + 1 :]:
            if _same_vendor_or_family(red_team.actual, other.actual):
                raise SeatAssignmentError(
                    "red-team seats must differ from each other by vendor and model family"
                )


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
