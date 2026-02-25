from app.models import CompanyInput, Profile, ProfileType
from app.services.validation import validate_profile


def test_requires_citation_for_populated_business_overview_field():
    p = Profile(profile_type=ProfileType.TARGET, company_input=CompanyInput(name="TestCo"))
    p.business_overview.overall.value = "Global industrial distributor"

    errors = validate_profile(p)

    assert "Missing citation for business_overview.overall" in errors


def test_narrative_requires_source_tag():
    p = Profile(profile_type=ProfileType.BUYER, company_input=CompanyInput(name="BuyerCo"))
    p.narratives.buyer_rationale.value = "Scale expansion in APAC"

    errors = validate_profile(p)

    assert "Buyer rationale bullets must include citations" in errors
