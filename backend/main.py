from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from rule_engine import check_large_transaction, check_high_frequency

from database import SessionLocal
from models import Alert, Customer, Account, Transaction, AMLRule
from schemas import (
    AlertResponse,
    AlertStatusUpdate,
    CustomerResponse,
    CustomerCreate,
    AccountCreate,
    AccountResponse,
    TransactionCreate,
    TransactionResponse
)


app = FastAPI(
    title="AML Transaction Monitoring System",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "AML System is running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }

@app.get(
    "/api/v1/alerts",
    response_model=list[AlertResponse]
)
def get_alerts(
    severity: str = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Alert)

    if severity:
        query = query.filter(Alert.severity == severity.upper())

    if status:
        query = query.filter(Alert.status == status.upper())

    alerts = (
        query
        .order_by(Alert.created_at.desc())
        .all()
    )

    return alerts
@app.get(
    "/api/v1/alerts/{alert_id}",
    response_model=AlertResponse
)
def get_alert_by_id(
    alert_id: int,
    db: Session = Depends(get_db)
):
    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if alert is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert

@app.patch(
    "/api/v1/alerts/{alert_id}/status",
    response_model=AlertResponse
)
def update_alert_status(
    alert_id: int,
    status_update: AlertStatusUpdate,
    db: Session = Depends(get_db)
):
    allowed_statuses = [
        "NEW",
        "UNDER_INVESTIGATION",
        "CLOSED",
        "ESCALATED"
    ]

    if status_update.status not in allowed_statuses:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Invalid alert status"
        )

    alert = db.query(Alert).filter(
        Alert.id == alert_id
    ).first()

    if alert is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    alert.status = status_update.status
    db.commit()
    db.refresh(alert)

    return alert

@app.get(
    "/api/v1/customers",
    response_model=list[CustomerResponse]
)
def get_customers(db: Session = Depends(get_db)):
    customers = (
        db.query(Customer)
        .order_by(Customer.id)
        .all()
    )

    return customers

@app.get(
    "/api/v1/customers/{customer_id}",
    response_model=CustomerResponse
)
def get_customer_by_id(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = db.query(Customer).filter(
        Customer.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer

@app.post(
    "/api/v1/customers",
    response_model=CustomerResponse,
    status_code=201
)
def create_customer(
    customer_data: CustomerCreate,
    db: Session = Depends(get_db)
):
    existing_customer = db.query(Customer).filter(
        Customer.email == customer_data.email
    ).first()

    if existing_customer:
        raise HTTPException(
            status_code=409,
            detail="A customer with this email already exists"
        )
    new_customer = Customer(
        full_name=customer_data.full_name,
        email=customer_data.email,
        phone=customer_data.phone,
        country=customer_data.country
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer

@app.post(
    "/api/v1/accounts",
    response_model=AccountResponse,
    status_code=201
)
def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_db)
):
    existing_account = db.query(Account).filter(
        Account.account_number == account_data.account_number
    ).first()

    if existing_account:
        raise HTTPException(
            status_code=409,
            detail="An account with this account number already exists"
        )

    customer = db.query(Customer).filter(
        Customer.id == account_data.customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    new_account = Account(
        account_number=account_data.account_number,
        account_type=account_data.account_type,
        currency=account_data.currency,
        balance=account_data.balance,
        status=account_data.status,
        customer_id=account_data.customer_id
    )

    db.add(new_account)
    db.commit()
    db.refresh(new_account)

    return new_account

@app.get(
    "/api/v1/accounts",
    response_model=list[AccountResponse]
)
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(Account).order_by(Account.id).all()
    return accounts

@app.get(
    "/api/v1/accounts/{account_id}",
    response_model=AccountResponse
)
def get_account_by_id(
    account_id: int,
    db: Session = Depends(get_db)
):
    account = db.query(Account).filter(
        Account.id == account_id
    ).first()

    if account is None:
        raise HTTPException(
            status_code=404,
            detail="Account not found"
        )

    return account


@app.post(
    "/api/v1/transactions",
    response_model=TransactionResponse,
    status_code=201
)
def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    existing_transaction = db.query(Transaction).filter(
        Transaction.transaction_reference ==
        transaction_data.transaction_reference
    ).first()

    if existing_transaction:
        raise HTTPException(
            status_code=409,
            detail="A transaction with this reference already exists"
        )

    sender = db.query(Account).filter(
        Account.id == transaction_data.sender_account_id
    ).first()

    if sender is None:
        raise HTTPException(
            status_code=404,
            detail="Sender account not found"
        )

    receiver = db.query(Account).filter(
        Account.id == transaction_data.receiver_account_id
    ).first()

    if receiver is None:
        raise HTTPException(
            status_code=404,
            detail="Receiver account not found"
        )

    new_transaction = Transaction(
        transaction_reference=transaction_data.transaction_reference,
        sender_account_id=transaction_data.sender_account_id,
        receiver_account_id=transaction_data.receiver_account_id,
        amount=transaction_data.amount,
        currency=transaction_data.currency,
        transaction_type=transaction_data.transaction_type,
        transaction_status=transaction_data.transaction_status,
        description=transaction_data.description
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    # Run AML-001 detection
    rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-001",
        AMLRule.is_active == "YES"
    ).first()

    if rule:
        result = check_large_transaction(new_transaction, rule)

        if result["triggered"]:
            alert = Alert(
                alert_reference=f"ALT-{uuid4().hex[:12].upper()}",
                transaction_id=new_transaction.id,
                rule_code=rule.rule_code,
                severity=result["severity"],
                message=result["message"],
                status="NEW"
            )
            db.add(alert)

    # Run AML-002 detection
    frequency_rule = db.query(AMLRule).filter(
        AMLRule.rule_code == "AML-002",
        AMLRule.is_active == "YES"
    ).first()

    if frequency_rule:
        from datetime import timedelta

        time_limit = new_transaction.timestamp - timedelta(hours=24)

        transaction_count = db.query(Transaction).filter(
            Transaction.sender_account_id == new_transaction.sender_account_id,
            Transaction.timestamp >= time_limit,
            Transaction.timestamp <= new_transaction.timestamp,
            Transaction.transaction_status == "COMPLETED"
        ).count()

        result = check_high_frequency(transaction_count, frequency_rule)

        if result["triggered"]:
            alert = Alert(
                alert_reference=f"ALT-{uuid4().hex[:12].upper()}",
                transaction_id=new_transaction.id,
                rule_code=frequency_rule.rule_code,
                severity=result["severity"],
                message=result["message"],
                status="NEW"
            )
            db.add(alert)

    db.commit()

    return new_transaction

@app.get(
    "/api/v1/transactions",
    response_model=list[TransactionResponse]
)
def get_transactions(db: Session = Depends(get_db)):
    transactions = (
        db.query(Transaction)
        .order_by(Transaction.timestamp.desc())
        .all()
    )

    return transactions

@app.get(
    "/api/v1/transactions/{transaction_id}",
    response_model=TransactionResponse
)
def get_transaction_by_id(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    transaction = db.query(Transaction).filter(
        Transaction.id == transaction_id
    ).first()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction

