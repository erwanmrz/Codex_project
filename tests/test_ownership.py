from app.models import OwnershipEntry
from app.services.ownership import OwnershipRuleEngine


def test_rule_1_applied_when_stakes_disclosed():
    out = OwnershipRuleEngine.apply(
        disclosed_with_stakes=[OwnershipEntry(name="Founder A", stake=51.0, evidence=["S1"])],
        disclosed_without_stakes=[],
        disclosed_investors=[],
    )
    assert out.rule_applied == 1
    assert out.entries[0].stake == 51.0


def test_rule_2_applied_when_names_without_stakes():
    out = OwnershipRuleEngine.apply(
        disclosed_with_stakes=[],
        disclosed_without_stakes=[OwnershipEntry(name="Family Office", evidence=["S2"])],
        disclosed_investors=[],
    )
    assert out.rule_applied == 2
    assert out.entries[0].stake is None
    assert "not publicly disclosed" in out.note.lower()


def test_rule_3_applied_for_disclosed_investors_only():
    out = OwnershipRuleEngine.apply(
        disclosed_with_stakes=[],
        disclosed_without_stakes=[],
        disclosed_investors=[OwnershipEntry(name="XYZ PE", round="Series B", evidence=["S3"])],
    )
    assert out.rule_applied == 3


def test_rule_4_applied_when_nothing_disclosed():
    out = OwnershipRuleEngine.apply(disclosed_with_stakes=[], disclosed_without_stakes=[], disclosed_investors=[])
    assert out.rule_applied == 4
