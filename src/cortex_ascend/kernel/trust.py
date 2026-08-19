from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FallbackPolicy(Enum):
    """Policy controlling cross-model fallback for a model lane."""

    DENY = "DENY"
    ALLOW_EXACT_VENDOR = "ALLOW_EXACT_VENDOR"
    ALLOW_ANY = "ALLOW_ANY"


class EgressPolicy(Enum):
    """Egress policy for a worker runtime."""

    NONE = "NONE"
    READ_ONLY = "READ_ONLY"
    MUTATION = "MUTATION"


@dataclass(frozen=True)
class ModelLanePolicy:
    """Policy for a single model lane.

    Cross-model fallback is off by default. Semantic switching is owned by
    Ascend seating policy, not by the transport.
    """

    requested_model: str
    allowed_models: frozenset[str]
    fallback_policy: FallbackPolicy = FallbackPolicy.DENY
    max_attempts: int = 3
    timeout_seconds: int = 600

    def permits_actual(self, actual: str) -> bool:
        """True when the actual model is permitted by this policy."""
        if actual == self.requested_model:
            return True
        if self.fallback_policy == FallbackPolicy.DENY:
            return False
        if self.fallback_policy == FallbackPolicy.ALLOW_ANY:
            return actual in self.allowed_models
        # ALLOW_EXACT_VENDOR would need vendor parsing; treat as allowed set.
        return actual in self.allowed_models


@dataclass(frozen=True)
class RuntimeProfile:
    """Runtime profile defining egress and mutation capabilities."""

    name: str
    egress: EgressPolicy
    can_mutate_repository: bool = False
    can_access_verifier_secrets: bool = False


WORKER_PROFILE = RuntimeProfile(
    name="worker",
    egress=EgressPolicy.READ_ONLY,
    can_mutate_repository=False,
    can_access_verifier_secrets=False,
)

VERIFIER_PROFILE = RuntimeProfile(
    name="verifier",
    egress=EgressPolicy.READ_ONLY,
    can_mutate_repository=False,
    can_access_verifier_secrets=True,
)

READONLY_PROFILE = RuntimeProfile(
    name="readonly",
    egress=EgressPolicy.READ_ONLY,
    can_mutate_repository=False,
    can_access_verifier_secrets=False,
)
