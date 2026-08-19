from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from cortex_ascend.kernel.contract import WorkContract
from cortex_ascend.kernel.predicates import adjudicate_against_base
from cortex_ascend.kernel.types import AdmissionDecision, Decision, ProjectSnapshot


class AuditOutcome(Enum):
    """Result of comparing Ascend's decision to an externally expected one."""

    MATCH = "MATCH"
    FALSE_ADMIT = "FALSE_ADMIT"
    FALSE_REJECT = "FALSE_REJECT"
    FALSE_STALE = "FALSE_STALE"
    FALSE_BLOCKED = "FALSE_BLOCKED"


@dataclass(frozen=True)
class AuditCase:
    """A single audit case with an externally expected decision."""

    case_id: str
    contract: WorkContract
    current_base: ProjectSnapshot
    expected: Decision
    category: str


@dataclass(frozen=True)
class AuditResult:
    """Result of running Ascend on an audit case."""

    case: AuditCase
    actual: AdmissionDecision
    outcome: AuditOutcome


def audit(case: AuditCase) -> AuditResult:
    """Run Ascend on an audit case and compare to the expected decision."""
    actual = adjudicate_against_base(case.contract, case.current_base)
    if actual.decision == case.expected:
        outcome = AuditOutcome.MATCH
    elif actual.decision == Decision.ADMIT:
        outcome = AuditOutcome.FALSE_ADMIT
    elif actual.decision == Decision.REJECT:
        outcome = AuditOutcome.FALSE_REJECT
    elif actual.decision == Decision.STALE:
        outcome = AuditOutcome.FALSE_STALE
    else:
        outcome = AuditOutcome.FALSE_BLOCKED
    return AuditResult(case=case, actual=actual, outcome=outcome)


def audit_corpus(cases: tuple[AuditCase, ...]) -> tuple[AuditResult, ...]:
    """Run Ascend over a corpus of audit cases."""
    return tuple(audit(case) for case in cases)


def any_false_admit(results: tuple[AuditResult, ...]) -> bool:
    """True if any audit case produced a false ADMIT."""
    return any(result.outcome == AuditOutcome.FALSE_ADMIT for result in results)


class GateMode(Enum):
    """Admission gate operating mode."""

    AUDIT = "AUDIT"
    REQUIRED = "REQUIRED"
    BREAK_GLASS = "BREAK_GLASS"


@dataclass(frozen=True)
class GatePolicy:
    """Policy controlling when Ascend admission is a required gate."""

    mode: GateMode
    break_glass_authority: str
    # Audit-mode false-admit count required before promotion.
    max_false_admits_for_promotion: int = 0

    def can_promote(self, audit_results: tuple[AuditResult, ...]) -> bool:
        """True when the audit corpus is clean enough to promote the gate."""
        if self.mode != GateMode.AUDIT:
            return False
        false_admits = sum(
            1 for result in audit_results if result.outcome == AuditOutcome.FALSE_ADMIT
        )
        return false_admits <= self.max_false_admits_for_promotion


@dataclass(frozen=True)
class FossilReceipt:
    """A canonical FOSSIL lineage receipt.

    Until real FOSSIL integration exists, this is a placeholder structure that
    records the expected fields without claiming a real write.
    """

    receipt_id: str
    status: str
    # URL or path to the canonical FOSSIL record, if available.
    canonical_url: str | None = None
    # True if the receipt was produced by real FOSSIL integration.
    verified: bool = False

    def is_real(self) -> bool:
        return self.verified and self.canonical_url is not None
