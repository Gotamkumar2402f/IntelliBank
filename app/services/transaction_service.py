from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction import TransactionCreate
from app.ml.fraud_detector import FraudDetector
import uuid
from datetime import datetime

fraud_detector = FraudDetector()

def create_transaction(db: Session, transaction: TransactionCreate):
    account_balance = None

    # Handle different transaction types
    if transaction.transaction_type == "transfer":
        from_acc = db.query(Account).filter(Account.id == transaction.from_account_id).first()
        to_acc = db.query(Account).filter(Account.id == transaction.to_account_id).first()

        if not from_acc or not to_acc:
            raise ValueError("Invalid account(s)")
        if from_acc.is_blocked or to_acc.is_blocked:
            raise ValueError("One of the accounts is blocked")
        if from_acc.balance < transaction.amount:
            raise ValueError("Insufficient balance")

        from_acc.balance -= transaction.amount
        to_acc.balance += transaction.amount
        account_balance = from_acc.balance + transaction.amount  # original balance

    elif transaction.transaction_type == "deposit":
        to_acc = db.query(Account).filter(Account.id == transaction.to_account_id).first()
        if not to_acc or to_acc.is_blocked:
            raise ValueError("Invalid or blocked account")
        to_acc.balance += transaction.amount

    elif transaction.transaction_type == "withdrawal":
        from_acc = db.query(Account).filter(Account.id == transaction.from_account_id).first()
        if not from_acc or from_acc.is_blocked:
            raise ValueError("Invalid or blocked account")
        if from_acc.balance < transaction.amount:
            raise ValueError("Insufficient balance")
        account_balance = from_acc.balance
        from_acc.balance -= transaction.amount

    else:
        raise ValueError("Invalid transaction type. Use: deposit, withdrawal, transfer")

    # Calculate Fraud Score automatically
    hour = datetime.now().hour
    fraud_score = fraud_detector.calculate_fraud_score(
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        account_balance=account_balance,
        hour=hour
    )
    is_fraud = fraud_detector.is_fraud(fraud_score)

    db_transaction = Transaction(
        transaction_id=str(uuid.uuid4())[:12].upper(),
        from_account_id=transaction.from_account_id,
        to_account_id=transaction.to_account_id,
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        description=transaction.description,
        status="success",
        fraud_score=fraud_score,
        is_fraud=is_fraud
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_all_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Transaction).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()

def get_transaction(db: Session, transaction_id: int):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()