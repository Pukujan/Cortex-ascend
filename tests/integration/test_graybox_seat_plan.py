from __future__ import annotations

from cortex_ascend.kernel import (
    SeatAssignment,
    SeatIdentity,
    SeatPlan,
    SeatRole,
    validate_seat_plan,
)


def test_graybox_executioner_seat_is_independent_from_producer_and_red_teams() -> None:
    """A cross-vendor seat plan including the graybox executioner is admissible.

    This exercises issue #28 mechanically: producer, red-team, and executioner
    seats must differ by vendor and model family before any inference or
    execution begins.
    """
    producer = SeatAssignment(
        requested=SeatIdentity(
            role=SeatRole.MUTANT,
            vendor="xai",
            model="grok-4.6",
            model_family="grok-4",
            provider="ckff",
            account="producer-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="windows-desktop",
            credentials="xai-producer-key",
            holdout_visibility="none",
            controller="orchestrator",
        ),
        actual=SeatIdentity(
            role=SeatRole.MUTANT,
            vendor="xai",
            model="grok-4.6",
            model_family="grok-4",
            provider="ckff",
            account="producer-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="windows-desktop",
            credentials="xai-producer-key",
            holdout_visibility="none",
            controller="orchestrator",
        ),
    )
    red_arch = SeatAssignment(
        requested=SeatIdentity(
            role=SeatRole.RED_ARCH,
            vendor="google",
            model="gemini-3.1-pro-preview",
            model_family="gemini-3.1",
            provider="ckff",
            account="red-arch-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="gravebuster",
            credentials="google-red-key",
            holdout_visibility="none",
            controller="verifier",
        ),
        actual=SeatIdentity(
            role=SeatRole.RED_ARCH,
            vendor="google",
            model="gemini-3.1-pro-preview",
            model_family="gemini-3.1",
            provider="ckff",
            account="red-arch-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="gravebuster",
            credentials="google-red-key",
            holdout_visibility="none",
            controller="verifier",
        ),
    )
    red_sec = SeatAssignment(
        requested=SeatIdentity(
            role=SeatRole.RED_SEC,
            vendor="zhipu",
            model="glm-5.2",
            model_family="glm-5",
            provider="ckff",
            account="red-sec-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="gravebuster",
            credentials="zhipu-red-key",
            holdout_visibility="none",
            controller="verifier",
        ),
        actual=SeatIdentity(
            role=SeatRole.RED_SEC,
            vendor="zhipu",
            model="glm-5.2",
            model_family="glm-5",
            provider="ckff",
            account="red-sec-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="gravebuster",
            credentials="zhipu-red-key",
            holdout_visibility="none",
            controller="verifier",
        ),
    )
    executioner = SeatAssignment(
        requested=SeatIdentity(
            role=SeatRole.FORMAL_ADV,
            vendor="alibaba",
            model="qwen-3.7-flash",
            model_family="qwen-3.7",
            provider="ckff",
            account="executioner-a",
            transport="ssh",
            context="none",
            runtime="gravebuster-podman-runsc",
            credentials="none",
            holdout_visibility="none",
            controller="verifier",
        ),
        actual=SeatIdentity(
            role=SeatRole.FORMAL_ADV,
            vendor="alibaba",
            model="qwen-3.7-flash",
            model_family="qwen-3.7",
            provider="ckff",
            account="executioner-a",
            transport="ssh",
            context="none",
            runtime="gravebuster-podman-runsc",
            credentials="none",
            holdout_visibility="none",
            controller="verifier",
        ),
    )

    validate_seat_plan(
        SeatPlan(
            producer=producer,
            red_teams=(red_arch, red_sec),
            executioner=executioner,
        )
    )
