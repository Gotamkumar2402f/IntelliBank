from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    from_account_id: Optional[int] = None
    to_account_id: Optional[int] = None
    amount: float
    transaction_type: str  # deposit, withdrawal, transfer
    description: Optional[str] = None

class TransactionOut(BaseModel):
    id: int
    transaction_id: str
    from_account_id: Optional[int]
    to_account_id: Optional[int]
    amount: float
    transaction_type: str
    status: str
    is_fraud: bool
    fraud_score: float
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True