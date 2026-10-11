from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.account import Account
from app.ml.fraud_detector import FraudDetector
from datetime import datetime

fraud_detector = FraudDetector()

def analyze_transaction(db: Session, transaction_id: int):
    """Analyze a single transaction and update fraud score"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        return None

    # Get account balance if possible
    account_balance = None
    if transaction.from_account_id:
        account = db.query(Account).filter(Account.id == transaction.from_account_id).first()
        if account:
            account_balance = account.balance

    hour = transaction.created_at.hour if transaction.created_at else datetime.now().hour

    score = fraud_detector.calculate_fraud_score(
        amount=transaction.amount,
        transaction_type=transaction.transaction_type,
        account_balance=account_balance,
        hour=hour
    )

    is_fraud = fraud_detector.is_fraud(score)

    # Update transaction
    transaction.fraud_score = score
    transaction.is_fraud = is_fraud
    db.commit()
    db.refresh(transaction)

    return {
        "transaction_id": transaction.transaction_id,
        "amount": transaction.amount,
        "fraud_score": score,
        "is_fraud": is_fraud,
        "message": "High Risk - Suspicious Transaction" if is_fraud else "Low Risk - Transaction looks safe"
    }

def get_fraud_transactions(db: Session, skip: int = 0, limit: int = 50):
    """Get all transactions marked as fraud"""
    return db.query(Transaction).filter(Transaction.is_fraud == True)\
             .order_by(Transaction.created_at.desc())\
             .offset(skip).limit(limit).all()

def get_high_risk_transactions(db: Session, min_score: float = 0.5, limit: int = 20):
    """Get transactions with high fraud score"""
    return db.query(Transaction).filter(Transaction.fraud_score >= min_score)\
             .order_by(Transaction.fraud_score.desc())\
             .limit(limit).all()

def analyze_all_transactions(db: Session):
    """Analyze all existing transactions"""
    transactions = db.query(Transaction).all()
    results = []
    for t in transactions:
        result = analyze_transaction(db, t.id)
        if result:
            results.append(result)
    return results