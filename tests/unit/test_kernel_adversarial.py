from __future__ import annotations

from cortex_ascend.kernel import (
    AttackHypothesis,
    ChaosFault,
    HoldoutItem,
    HoldoutSuite,
    RedTeamReceipt,
    SeatIdentity,
    SeatRole,
)


def test_seat_identity_records_independence_vectors() -> None:
    seat = SeatIdentity(
        role=SeatRole.RED_ARCH,
        vendor="google",
        model="gemini-3.1-pro-preview",
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
