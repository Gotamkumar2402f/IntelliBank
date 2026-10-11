from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from app.core.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    to_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String)  # deposit, withdrawal, transfer
    status = Column(String, default="success")  # success, failed, pending
    is_fraud = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())