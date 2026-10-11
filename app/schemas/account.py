from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    account_type: str = "savings"

class AccountCreate(AccountBase):
    user_id: int
    initial_balance: float = 0.0

class AccountOut(BaseModel):
    id: int
    account_number: str
    user_id: int
    account_type: str
    balance: float
    is_blocked: bool
    block_reason: Optional[str] = None
    risk_score: float
    created_at: datetime

    class Config:
        from_attributes = True