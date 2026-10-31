from decimal import Decimal

from database import SessionLocal
from models import Transaction, AMLRule
from rule_engine import check_large_transaction


db = SessionLocal()

try:
    transaction = db.query(Transaction).first()
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-001"
    ).first()

    if transaction is None:
        print("ERROR: No transaction found.")
    elif rule is None:
        print("ERROR: AML-001 rule not found.")
    else:
        # Test 1: Amount below threshold
        transaction.amount = Decimal("5000")
        result1 = check_large_transaction(transaction, rule)
        print("Test 1 — Small transaction:", result1)
        assert result1["triggered"] is False

        # Test 2: Amount above threshold
        transaction.amount = Decimal("150000")
        result2 = check_large_transaction(transaction, rule)
        print("Test 2 — Large transaction:", result2)
        assert result2["triggered"] is True

        print("Both AML-001 tests passed!")

finally:
    db.close()