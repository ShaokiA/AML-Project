from database import SessionLocal
from models import AMLRule
from rule_engine import check_circular_transfers


db = SessionLocal()

try:
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-005"
    ).first()

    if rule is None:
        print("ERROR: AML-005 rule not found.")
    else:
        # Test 1: Cycle length below threshold
        result1 = check_circular_transfers(2, rule)
        print("Test 1 — Cycle length 2:", result1)
        assert result1["triggered"] is False

        # Test 2: Cycle length at threshold
        result2 = check_circular_transfers(3, rule)
        print("Test 2 — Cycle length 3:", result2)
        assert result2["triggered"] is True

        # Test 3: Cycle length above threshold
        result3 = check_circular_transfers(4, rule)
        print("Test 3 — Cycle length 4:", result3)
        assert result3["triggered"] is True

        print("All AML-005 tests passed!")

finally:
    db.close()