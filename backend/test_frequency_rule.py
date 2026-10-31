from database import SessionLocal
from models import AMLRule
from rule_engine import check_high_frequency


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-002"
    ).first()

    if rule is None:
        print("ERROR: AML-002 rule not found.")
    else:
        # Test 1: Below the threshold of 10
        result1 = check_high_frequency(5, rule)
        print("Test 1 — 5 transactions:", result1)
        assert result1["triggered"] is False

        # Test 2: At the threshold of 10
        result2 = check_high_frequency(10, rule)
        print("Test 2 — 10 transactions:", result2)
        assert result2["triggered"] is True

        print("Both AML-002 tests passed!")

finally:
    db.close()