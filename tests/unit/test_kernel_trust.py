from __future__ import annotations

from cortex_ascend.kernel import (
    VERIFIER_PROFILE,
    WORKER_PROFILE,
    EgressPolicy,
    FallbackPolicy,
    ModelLanePolicy,
    RuntimeProfile,
)


def test_model_lane_permits_requested_model() -> None:
    policy = ModelLanePolicy(
        requested_model="litellm/grok-4.6",
        allowed_models=frozenset({"litellm/qwen3.6-plus"}),
        fallback_policy=FallbackPolicy.DENY,
    )
    assert policy.permits_actual("litellm/grok-4.6")
    assert not policy.permits_actual("litellm/qwen3.6-plus")


def test_model_lane_allows_vendor_fallback() -> None:
    policy = ModelLanePolicy(
        requested_model="litellm/grok-4.6",
        allowed_models=frozenset({"litellm/qwen3.6-plus"}),
        fallback_policy=FallbackPolicy.ALLOW_ANY,
    )
    assert policy.permits_actual("litellm/qwen3.6-plus")


def test_worker_profile_cannot_access_verifier_secrets() -> None:
    assert not WORKER_PROFILE.can_access_verifier_secrets
    assert WORKER_PROFILE.egress == EgressPolicy.READ_ONLY
    assert not WORKER_PROFILE.can_mutate_repository


def test_verifier_profile_can_access_verifier_secrets() -> None:
    assert VERIFIER_PROFILE.can_access_verifier_secrets
    assert VERIFIER_PROFILE.egress == EgressPolicy.READ_ONLY
    assert not VERIFIER_PROFILE.can_mutate_repository


def test_runtime_profile_mutation_requires_explicit_flag() -> None:
    readonly = RuntimeProfile(
        name="readonly",
        egress=EgressPolicy.READ_ONLY,
        can_mutate_repository=False,
        can_access_verifier_secrets=False,
    )
    assert not readonly.can_mutate_repository
