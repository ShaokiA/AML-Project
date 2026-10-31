from database import SessionLocal
from models import AMLRule
from rule_engine import check_layering_pattern


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-008"
    ).first()

    if rule is None:
        print("ERROR: AML-008 rule not found.")
    else:
        # Test 1: Below the threshold of 4
        result1 = check_layering_pattern(2, rule)
        print("Test 1 — 2 intermediary accounts:", result1)
        assert result1["triggered"] is False

        # Test 2: Exactly at the threshold
        result2 = check_layering_pattern(4, rule)
        print("Test 2 — 4 intermediary accounts:", result2)
        assert result2["triggered"] is True

        # Test 3: Above the threshold
        result3 = check_layering_pattern(6, rule)
        print("Test 3 — 6 intermediary accounts:", result3)
        assert result3["triggered"] is True

        print("All AML-008 tests passed!")

finally:
    db.close()