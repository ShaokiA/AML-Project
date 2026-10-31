from decimal import Decimal

from database import SessionLocal
from models import AMLRule
from rule_engine import check_unusual_customer_behavior


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-007"
    ).first()

    if rule is None:
        print("ERROR: AML-007 rule not found.")
    else:
        # Historical average = 10,000; standard deviation = 2,000
        # Test 1: 12,000 is only 1 standard deviation away
        result1 = check_unusual_customer_behavior(
            Decimal("12000"), Decimal("10000"),
            Decimal("2000"), rule
        )
        print("Test 1 — Normal variation:", result1)
        assert result1["triggered"] is False

        # Test 2: 16,000 is exactly 3 standard deviations away
        result2 = check_unusual_customer_behavior(
            Decimal("16000"), Decimal("10000"),
            Decimal("2000"), rule
        )
        print("Test 2 — At threshold:", result2)
        assert result2["triggered"] is True

        # Test 3: Zero standard deviation cannot be evaluated
        result3 = check_unusual_customer_behavior(
            Decimal("15000"), Decimal("10000"),
            Decimal("0"), rule
        )
        print("Test 3 — Zero standard deviation:", result3)
        assert result3["triggered"] is False

        print("All AML-007 tests passed!")

finally:
    db.close()