from __future__ import annotations

from cortex_ascend.kernel import (
    AttackHypothesis,
    ChaosFault,
    HoldoutItem,
    HoldoutSuite,
    RedTeamReceipt,
    SeatAssignment,
    SeatAssignmentError,
    SeatIdentity,
    SeatPlan,
    SeatRole,
    validate_seat_plan,
)


def _seat(role: SeatRole, vendor: str, family: str, model: str) -> SeatIdentity:
    return SeatIdentity(
        role=role,
        vendor=vendor,
        model=model,
        model_family=family,
        provider="ckff",
        account=f"{vendor}-account",
        transport="litellm",
        context="fresh-task",
        runtime="isolated",
        credentials=f"{vendor}-key",
        holdout_visibility="none",
        controller="verifier",
    )


def test_seat_identity_records_independence_vectors() -> None:
    seat = SeatIdentity(
        role=SeatRole.RED_ARCH,
        vendor="google",
        model="gemini-3.1-pro-preview",
        model_family="gemini-3.1",
        provider="ckff",
        account="red-team-a",
        transport="litellm-railway",
        context="fresh-task",
        runtime="gravebuster",
        credentials="dedicated-key",
        holdout_visibility="none",
        controller="verifier",
    )
    assert seat.vendor == "google"
    assert seat.holdout_visibility == "none"


def test_attack_hypothesis_deduplication_fingerprint() -> None:
    a = AttackHypothesis(
        hypothesis_id="h1",
        seat=SeatIdentity(
            role=SeatRole.RED_ARCH,
            vendor="google",
            model="gemini-3.1-pro-preview",
            model_family="gemini-3.1",
            provider="ckff",
            account="red-team-a",
            transport="litellm-railway",
            context="fresh-task",
            runtime="gravebuster",
            credentials="dedicated-key",
            holdout_visibility="none",
            controller="verifier",
        ),
        target_invariant="ASC-INV-KRN-001",
        description="stale base replay",
        fingerprint="stale-base-replay-v1",
    )
    b = AttackHypothesis(
        hypothesis_id="h2",
        seat=a.seat,
        target_invariant="ASC-INV-KRN-001",
        description="stale base replay variant",
        fingerprint="stale-base-replay-v1",
    )
    assert a.fingerprint == b.fingerprint


def test_holdout_suite_fingerprint_includes_hashes() -> None:
    suite = HoldoutSuite(
        suite_id="s1",
        count=2,
        items=(
            HoldoutItem("i1", "v1", "deadbeef"),
            HoldoutItem("i2", "v1", "cafebabe"),
        ),
    )
    fp = suite.fingerprint()
    assert "deadbeef" in fp
    assert "cafebabe" in fp


def test_chaos_fault_declares_expected_outcome() -> None:
    fault = ChaosFault(
        fault_id="f1",
        schedule="after-admit-revoke-grant",
        target_invariant="ASC-INV-KRN-001",
        expected_outcome="REJECT",
    )
    assert fault.expected_outcome == "REJECT"


def test_red_team_receipt_links_seat_and_hypothesis() -> None:
    seat = SeatIdentity(
        role=SeatRole.MUTANT,
        vendor="alibaba",
        model="qwen3.6-plus",
        model_family="qwen3.6",
        provider="ckff",
        account="mutant-a",
        transport="litellm-railway",
        context="fresh-task",
        runtime="windows-desktop",
        credentials="shared",
        holdout_visibility="none",
        controller="orchestrator",
    )
    hypothesis = AttackHypothesis(
        hypothesis_id="h3",
        seat=seat,
        target_invariant="ASC-INV-MDL-002",
        description="model substitution",
        fingerprint="model-substitution-v1",
    )
    receipt = RedTeamReceipt(seat=seat, hypothesis=hypothesis, harness_result="killed")
    assert receipt.harness_result == "killed"


def test_seat_plan_accepts_distinct_producer_red_teams_and_executioner() -> None:
    producer = SeatAssignment(
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
    )

    validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))


def test_seat_plan_rejects_shared_model_family_even_across_vendors() -> None:
    producer = SeatAssignment(
        _seat(SeatRole.MUTANT, "openai", "gpt-5.6", "gpt-5.6-terra"),
        _seat(SeatRole.MUTANT, "openai", "gpt-5.6", "gpt-5.6-terra"),
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "proxy", "gpt-5.6", "gpt-5.6-sol"),
        _seat(SeatRole.FORMAL_ADV, "proxy", "gpt-5.6", "gpt-5.6-sol"),
    )

    try:
        validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))
    except SeatAssignmentError as exc:
        assert "producer and executioner" in str(exc)
    else:
        raise AssertionError("shared model family was accepted")


def test_seat_plan_rejects_shared_red_team_vendor() -> None:
    producer = SeatAssignment(
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "google", "gemini-3.5", "gemini-3.5-flash"),
        _seat(SeatRole.RED_SEC, "google", "gemini-3.5", "gemini-3.5-flash"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
    )

    try:
        validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))
    except SeatAssignmentError as exc:
        assert "red-team seats" in str(exc)
    else:
        raise AssertionError("shared red-team vendor was accepted")


def test_seat_plan_rejects_producer_vendor_in_a_red_team() -> None:
    producer = SeatAssignment(
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6"),
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "xai", "grok-3", "grok-3"),
        _seat(SeatRole.RED_ARCH, "xai", "grok-3", "grok-3"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
    )

    try:
        validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))
    except SeatAssignmentError as exc:
        assert "producer and red-team" in str(exc)
    else:
        raise AssertionError("producer vendor was accepted in a red-team seat")


def test_seat_plan_rejects_unauthorized_actual_model() -> None:
    requested = _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6")
    producer = SeatAssignment(
        requested, _seat(SeatRole.MUTANT, "google", "gemini-3.1", "gemini-3.1-pro")
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "zhipu", "glm-5", "glm-5.2"),
        _seat(SeatRole.RED_ARCH, "zhipu", "glm-5", "glm-5.2"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
        _seat(SeatRole.RED_SEC, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "deepseek", "deepseek-v4", "deepseek-v4-flash"),
        _seat(SeatRole.FORMAL_ADV, "deepseek", "deepseek-v4", "deepseek-v4-flash"),
    )

    try:
        validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))
    except SeatAssignmentError as exc:
        assert "actual model identity" in str(exc)
    else:
        raise AssertionError("unauthorized actual model was accepted")


def test_seat_plan_allows_authorized_actual_model_substitution() -> None:
    requested = _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6")
    producer = SeatAssignment(
        requested,
        _seat(SeatRole.MUTANT, "xai", "grok-4", "grok-4.6-revision"),
        actual_authorized=True,
    )
    red_arch = SeatAssignment(
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
        _seat(SeatRole.RED_ARCH, "google", "gemini-3.1", "gemini-3.1-pro"),
    )
    red_sec = SeatAssignment(
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
        _seat(SeatRole.RED_SEC, "zhipu", "glm-5", "glm-5.2"),
    )
    executioner = SeatAssignment(
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
        _seat(SeatRole.FORMAL_ADV, "alibaba", "qwen-3.7", "qwen-3.7-flash"),
    )

    validate_seat_plan(SeatPlan(producer, (red_arch, red_sec), executioner))
