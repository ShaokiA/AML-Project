from database import SessionLocal
from models import AMLRule
from rule_engine import check_multiple_counterparties


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-006"
    ).first()

    if rule is None:
        print("ERROR: AML-006 rule not found.")
    else:
        # Test 1: Below the threshold of 15
        result1 = check_multiple_counterparties(8, rule)
        print("Test 1 — 8 counterparties:", result1)
        assert result1["triggered"] is False

        # Test 2: Exactly at the threshold
        result2 = check_multiple_counterparties(15, rule)
        print("Test 2 — 15 counterparties:", result2)
        assert result2["triggered"] is True

        # Test 3: Above the threshold
        result3 = check_multiple_counterparties(20, rule)
        print("Test 3 — 20 counterparties:", result3)
        assert result3["triggered"] is True

        print("All AML-006 tests passed!")

finally:
    db.close()