from __future__ import annotations

from typing import Iterable, List

from app.models import Profile


def _has_evidence(evidence: Iterable[str]) -> bool:
    return len(list(evidence)) > 0


def validate_profile(profile: Profile) -> List[str]:
    errors: List[str] = []

    bo = profile.business_overview
    for name, field in {
        "business_overview.overall": bo.overall,
        "business_overview.segments": bo.segments,
        "business_overview.clients": bo.clients,
        "business_overview.industrial_setup": bo.industrial_setup,
    }.items():
        if field.value and not _has_evidence(field.evidence):
            errors.append(f"Missing citation for {name}")

    if profile.ownership.rule_applied not in (1, 2, 3, 4):
        errors.append("Ownership rule_applied must be one of 1,2,3,4")

    if profile.narratives.buyer_rationale.value and "[S" not in profile.narratives.buyer_rationale.value:
        errors.append("Buyer rationale bullets must include citations")

    if profile.narratives.prospect_talking_points.value and "[S" not in profile.narratives.prospect_talking_points.value:
        errors.append("Prospect talking points must include citations")

    return errors
