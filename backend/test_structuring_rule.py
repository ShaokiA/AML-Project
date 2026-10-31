from decimal import Decimal

from database import SessionLocal
from models import AMLRule
from rule_engine import check_structuring


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-003"
    ).first()

    if rule is None:
        print("ERROR: AML-003 rule not found.")
    else:
        # Test 1: Total below the 90,000 threshold
        result1 = check_structuring(Decimal("50000"), 2, rule)
        print("Test 1 — Below threshold:", result1)
        assert result1["triggered"] is False

        # Test 2: Multiple transactions totaling 90,000
        result2 = check_structuring(Decimal("90000"), 3, rule)
        print("Test 2 — At threshold:", result2)
        assert result2["triggered"] is True

        # Test 3: A single transaction should not count as structuring
        result3 = check_structuring(Decimal("120000"), 1, rule)
        print("Test 3 — Single transaction:", result3)
        assert result3["triggered"] is False

        print("All AML-003 tests passed!")

finally:
    db.close()