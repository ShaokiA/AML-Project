from decimal import Decimal

from database import SessionLocal
from models import AMLRule
from rule_engine import check_rapid_fund_movement


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-004"
    ).first()

    if rule is None:
        print("ERROR: AML-004 rule not found.")
    else:
        # Test 1: Movement within 30 minutes
        result1 = check_rapid_fund_movement(30, rule)
        print("Test 1 — 30 minutes:", result1)
        assert result1["triggered"] is True

        # Test 2: Movement exactly at 60 minutes
        result2 = check_rapid_fund_movement(60, rule)
        print("Test 2 — 60 minutes:", result2)
        assert result2["triggered"] is True

        # Test 3: Movement taking 90 minutes
        result3 = check_rapid_fund_movement(90, rule)
        print("Test 3 — 90 minutes:", result3)
        assert result3["triggered"] is False

        print("All AML-004 tests passed!")

finally:
    db.close()