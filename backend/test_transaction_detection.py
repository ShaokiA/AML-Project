
from uuid import uuid4

from database import SessionLocal
from models import Transaction, AMLRule, Alert
from rule_engine import check_large_transaction


def main():
    db = SessionLocal()

    try:
        rule = db.query(AMLRule).filter(
            AMLRule.rule_code == "AML-001",
            AMLRule.is_active == "YES"
        ).first()

        if rule is None:
            print("ERROR: Active AML-001 rule not found.")
            return

        transactions = (
            db.query(Transaction)
            .order_by(Transaction.id)
            .all()
        )

        print(f"Checking {len(transactions)} transaction(s)")
        detected = 0
        created = 0

        for transaction in transactions:
            result = check_large_transaction(transaction, rule)

            print(
                f"{transaction.transaction_reference} | "
                f"Amount: {transaction.amount} {transaction.currency} | "
                f"Triggered: {result['triggered']}"
            )

            if not result["triggered"]:
                continue

            detected += 1

            existing_alert = db.query(Alert).filter(
                Alert.transaction_id == transaction.id,
                Alert.rule_code == rule.rule_code
            ).first()

            if existing_alert:
                print("  Alert already exists; skipping duplicate.")
                continue

            alert = Alert(
                alert_reference=f"ALT-{uuid4().hex[:12].upper()}",
                transaction_id=transaction.id,
                rule_code=rule.rule_code,
                severity=result["severity"],
                message=result["message"],
                status="NEW"
            )

            db.add(alert)
            created += 1
            print("  New alert prepared.")

        db.commit()

        print("-" * 50)
        print(f"Transactions checked: {len(transactions)}")
        print(f"Transactions triggering AML-001: {detected}")
        print(f"New alerts saved: {created}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
