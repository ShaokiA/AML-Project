from database import SessionLocal
from models import AMLRule


def main():
    db = SessionLocal()

    try:
        rules = (
            db.query(AMLRule)
            .filter(AMLRule.is_active == "YES")
            .order_by(AMLRule.rule_code)
            .all()
        )

        print(f"Active AML rules found: {len(rules)}")
        print("-" * 50)

        for rule in rules:
            print(
                f"{rule.rule_code} | "
                f"{rule.rule_name} | "
                f"Threshold: {rule.threshold} | "
                f"Severity: {rule.severity}"
            )

        if len(rules) != 8:
            print("WARNING: Expected 8 active rules.")
        else:
            print("-" * 50)
            print("All 8 active AML rules loaded successfully.")

    finally:
        db.close()


if __name__ == "__main__":
    main()