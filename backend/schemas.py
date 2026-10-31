from datetime import datetime
from pydantic import BaseModel, ConfigDict
from decimal import Decimal

class AlertResponse(BaseModel):
    id: int
    alert_reference: str
    transaction_id: int
    rule_code: str
    severity: str
    message: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AlertStatusUpdate(BaseModel):
    status: str

class CustomerResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str | None
    country: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CustomerCreate(BaseModel):
    full_name: str
    email: str
    phone: str | None = None
    country: str | None = None

class AccountCreate(BaseModel):
    account_number: str
    account_type: str
    currency: str
    balance: Decimal
    status: str = "ACTIVE"
    customer_id: int


class AccountResponse(BaseModel):
    id: int
    account_number: str
    account_type: str
    currency: str
    balance: Decimal
    status: str
    customer_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TransactionCreate(BaseModel):
    transaction_reference: str
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    currency: str
    transaction_type: str
    transaction_status: str = "COMPLETED"
    description: str | None = None


class TransactionResponse(BaseModel):
    id: int
    transaction_reference: str
    sender_account_id: int
    receiver_account_id: int
    amount: Decimal
    currency: str
    transaction_type: str
    transaction_status: str
    description: str | None
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)

