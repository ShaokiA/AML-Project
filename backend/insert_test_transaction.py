from decimal import Decimal

from database import SessionLocal
from models import Transaction


db = SessionLocal()

try:
    existing = db.query(Transaction).filter(
        Transaction.transaction_reference == "TXN-AML-TEST-001"
    ).first()

    if existing:
        print("Test transaction already exists.")
    else:
        transaction = Transaction(
            transaction_reference="TXN-AML-TEST-001",
            sender_account_id=1,
            receiver_account_id=2,
            amount=Decimal("150000.00"),
            currency="BDT",
            transaction_type="TRANSFER",
            transaction_status="COMPLETED",
            description="Controlled AML detection test"
        )

        db.add(transaction)
        db.commit()

        print("Test transaction inserted successfully.")

finally:
    db.close()