from app.core.database import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.ml.fraud_detector import FraudDetector
import uuid
from datetime import datetime, timedelta
import random

fraud_detector = FraudDetector()

def seed_more():
    db = SessionLocal()

    accounts = db.query(Account).all()
    if len(accounts) < 2:
        print("Please run seed_data.py first")
        db.close()
        return

    acc1 = accounts[0]
    acc2 = accounts[1]

    # Normal transactions
    normal_data = [
        {"type": "deposit", "amount": 5000, "desc": "Salary credit"},
        {"type": "withdrawal", "amount": 2000, "desc": "ATM withdrawal"},
        {"type": "transfer", "amount": 3000, "desc": "Friend transfer"},
        {"type": "deposit", "amount": 15000, "desc": "Business payment"},
    ]

    # High risk / suspicious transactions
    risky_data = [
        {"type": "withdrawal", "amount": 95000, "desc": "Large cash withdrawal"},
        {"type": "transfer", "amount": 110000, "desc": "Urgent international transfer"},
        {"type": "withdrawal", "amount": 78000, "desc": "Night withdrawal"},
        {"type": "transfer", "amount": 150000, "desc": "Suspicious large transfer"},
    ]

    all_data = normal_data + risky_data

    for i, item in enumerate(all_data):
        amount = item["amount"]
        t_type = item["type"]

        from_id = None
        to_id = None
        balance = None

        if t_type == "deposit":
            to_id = acc1.id
        elif t_type == "withdrawal":
            from_id = acc1.id
            balance = acc1.balance
            if acc1.balance >= amount:
                acc1.balance -= amount
        elif t_type == "transfer":
            from_id = acc1.id
            to_id = acc2.id
            balance = acc1.balance
            if acc1.balance >= amount:
                acc1.balance -= amount
                acc2.balance += amount

        # Random hour (some at night for higher risk)
        hour = random.choice([2, 3, 14, 15, 22, 1]) if i >= 4 else 14

        score = fraud_detector.calculate_fraud_score(
            amount=amount,
            transaction_type=t_type,
            account_balance=balance,
            hour=hour
        )
        is_fraud = fraud_detector.is_fraud(score)

        t = Transaction(
            transaction_id=str(uuid.uuid4())[:12].upper(),
            from_account_id=from_id,
            to_account_id=to_id,
            amount=amount,
            transaction_type=t_type,
            description=item["desc"],
            status="success",
            fraud_score=score,
            is_fraud=is_fraud,
            created_at=datetime.now() - timedelta(hours=random.randint(1, 48))
        )
        db.add(t)

    db.commit()
    print("Extra sample data (including high-risk transactions) added successfully!")
    db.close()

if __name__ == "__main__":
    seed_more()