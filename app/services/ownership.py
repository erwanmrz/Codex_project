from __future__ import annotations

from typing import List

from app.models import Ownership, OwnershipEntry


class OwnershipRuleEngine:
    """Deterministic ownership fallback evaluator (exactly one rule)."""

    @staticmethod
    def apply(
        disclosed_with_stakes: List[OwnershipEntry],
        disclosed_without_stakes: List[OwnershipEntry],
        disclosed_investors: List[OwnershipEntry],
    ) -> Ownership:
        if disclosed_with_stakes:
            return Ownership(rule_applied=1, entries=disclosed_with_stakes)

        if disclosed_without_stakes:
            normalized = [
                OwnershipEntry(
                    name=e.name,
                    stake=None,
                    type=e.type,
                    evidence=e.evidence,
                    round=e.round,
                )
                for e in disclosed_without_stakes
            ]
            return Ownership(
                rule_applied=2,
                entries=normalized,
                note="Ownership percentages not publicly disclosed",
            )

        if disclosed_investors:
            normalized = [
                OwnershipEntry(
                    name=e.name,
                    stake=None,
                    type=e.type,
                    evidence=e.evidence,
                    round=e.round,
                )
                for e in disclosed_investors
            ]
            return Ownership(
                rule_applied=3,
                entries=normalized,
                note="Ultimate ownership structure not publicly disclosed",
            )

        return Ownership(rule_applied=4, entries=[], note="Ownership structure not publicly disclosed")
