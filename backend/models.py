from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(30), nullable=True)
    country = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(30), unique=True, nullable=False)
    account_type = Column(String(30), nullable=False)
    currency = Column(String(10), nullable=False, default="USD")
    balance = Column(Numeric(15, 2), nullable=False, default=0)
    status = Column(String(20), nullable=False, default="ACTIVE")

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    transaction_reference = Column(
        String(50),
        unique=True,
        nullable=False
    )

    sender_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    receiver_account_id = Column(
        Integer,
        ForeignKey("accounts.id"),
        nullable=False
    )

    amount = Column(
        Numeric(15, 2),
        nullable=False
    )

    currency = Column(
        String(10),
        nullable=False,
        default="USD"
    )

    transaction_type = Column(
        String(30),
        nullable=False
    )

    transaction_status = Column(
        String(20),
        nullable=False,
        default="COMPLETED"
    )

    description = Column(
        String(255),
        nullable=True
    )

    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class AMLRule(Base):
    __tablename__ = "aml_rules"

    id = Column(Integer, primary_key=True, index=True)

    rule_code = Column(
        String(30),
        unique=True,
        nullable=False
    )

    rule_name = Column(
        String(150),
        nullable=False
    )

    description = Column(
        String(500),
        nullable=True
    )

    threshold = Column(
        Numeric(15, 2),
        nullable=True
    )

    severity = Column(
        String(20),
        nullable=False
    )

    is_active = Column(
        String(10),
        nullable=False,
        default="YES"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    alert_reference = Column(
        String(50),
        unique=True,
        nullable=False
    )

    transaction_id = Column(
        Integer,
        ForeignKey("transactions.id"),
        nullable=False
    )

    rule_code = Column(
        String(30),
        ForeignKey("aml_rules.rule_code"),
        nullable=False
    )

    severity = Column(
        String(20),
        nullable=False
    )

    message = Column(
        String(1000),
        nullable=False
    )

    status = Column(
        String(30),
        nullable=False,
        default="NEW"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
