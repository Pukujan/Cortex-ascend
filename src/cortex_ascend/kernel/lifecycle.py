from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from cortex_ascend.kernel.contract import WorkContract
from cortex_ascend.kernel.predicates import adjudicate_against_base
from cortex_ascend.kernel.types import (
    AdmissionDecision,
    ArtifactDigest,
    Decision,
    Generation,
    ProjectSnapshot,
)


class AttemptState(Enum):
    """Lifecycle state of a single admission attempt."""

    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ADMITTED = auto()
    REJECTED = auto()
    STALE = auto()
    REVOKED = auto()


@dataclass(frozen=True)
class Attempt:
    """A single attempt to admit a contract at a specific generation."""

    generation: Generation
    state: AttemptState = AttemptState.PENDING
    # Decision rendered at completion, if any.
    decision: AdmissionDecision | None = None


@dataclass(frozen=True)
class Lifecycle:
    """Mutable-in-place simulation of admission attempts across generations.

    This is an executable model of stale-generation semantics. It is not part
    of the production admission oracle; it exists to test that no stale
    generation can produce ADMIT against a current base.
    """

    current_base: ProjectSnapshot
    attempts: dict[int, Attempt] = field(default_factory=dict)
    current_generation: Generation = field(default_factory=lambda: Generation(0))
    # Authority grants that have been revoked.
    revoked_grants: frozenset[str] = field(default_factory=frozenset)

    def replace_base(self, new_base: ProjectSnapshot) -> Lifecycle:
        """Return a lifecycle with a new authoritative base/generation."""
        return Lifecycle(
            current_base=new_base,
            attempts=dict(self.attempts),
            current_generation=self.current_generation.next(),
            revoked_grants=self.revoked_grants,
        )

    def start_attempt(self, generation: Generation) -> Lifecycle:
        """Record that an attempt at `generation` has started."""
        if generation.value in self.attempts:
            return self
        attempts = dict(self.attempts)
        attempts[generation.value] = Attempt(generation, AttemptState.RUNNING)
        return Lifecycle(
            current_base=self.current_base,
            attempts=attempts,
            current_generation=self.current_generation,
            revoked_grants=self.revoked_grants,
        )

    def complete_attempt(
        self,
        generation: Generation,
        contract: WorkContract,
    ) -> Lifecycle:
        """Complete an attempt by adjudicating its contract against the current base."""
        attempts = dict(self.attempts)
        decision = adjudicate_against_base(contract, self.current_base)

        # Authority revocation mid-attempt is modeled at the lifecycle level.
        if (
            decision.decision == Decision.ADMIT
            and contract.authority.grant_id in self.revoked_grants
        ):
            from cortex_ascend.kernel.serialization import canonical_hash

            decision = AdmissionDecision(
                decision=Decision.REJECT,
                contract_digest=ArtifactDigest(algorithm="sha256", hex=canonical_hash(contract)),
                reason="authority grant was revoked before completion",
                generation=contract.generation,
            )

        state = _state_from_decision(decision.decision)
        attempts[generation.value] = Attempt(generation=generation, state=state, decision=decision)
        return Lifecycle(
            current_base=self.current_base,
            attempts=attempts,
            current_generation=self.current_generation,
            revoked_grants=self.revoked_grants,
        )

    def revoke_grant(self, grant_id: str) -> Lifecycle:
        """Revoke a grant; does not retroactively change completed attempts."""
        return Lifecycle(
            current_base=self.current_base,
            attempts=dict(self.attempts),
            current_generation=self.current_generation,
            revoked_grants=self.revoked_grants | {grant_id},
        )

    def any_admit_from_stale_generation(self) -> bool:
        """True if any attempt from a generation before current_generation is ADMIT."""
        return any(
            attempt.generation.value < self.current_generation.value
            and attempt.decision is not None
            and attempt.decision.decision == Decision.ADMIT
            for attempt in self.attempts.values()
        )


def _state_from_decision(decision: Decision) -> AttemptState:
    mapping = {
        Decision.ADMIT: AttemptState.ADMITTED,
        Decision.REJECT: AttemptState.REJECTED,
        Decision.STALE: AttemptState.STALE,
        Decision.BLOCKED: AttemptState.REVOKED,
    }
    return mapping.get(decision, AttemptState.REJECTED)
