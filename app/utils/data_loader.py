"""
Data Loader — Import real Kaggle Credit Card Fraud dataset
into IntelliBank SQLite database.

Kaggle dataset: mlg-ulb/creditcardfraud
- 284,807 transactions
- 492 frauds (Class=1)
- Columns: Time, V1-V28, Amount, Class
"""

import pandas as pd
import random
import uuid
from datetime import datetime, timedelta
from app.core.database import SessionLocal, Base, engine
from app.models.account import Account
from app.models.transaction import Transaction
from app.models.user import User


def load_real_data(csv_path: str = "data/real_data/creditcard.csv", sample_size: int = 5000):
    """Load real credit card fraud data into IntelliBank database."""

    print(f"📂 Loading CSV: {csv_path}")
    df = pd.read_csv(csv_path)
    print(f"✅ CSV loaded: {len(df):,} rows")

    # Take a manageable sample
    if sample_size and sample_size < len(df):
        df = df.sample(n=sample_size, random_state=42)
        print(f"📊 Sampled {sample_size:,} rows for database")

    df = df.reset_index(drop=True)

    # Create database tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.query(Transaction).count()
        if existing > 100:
            print(f"⚠️  Database already has {existing} transactions.")
            print("   Delete data/intellibank.db to re-import.")
            return

        # ===== 1. Create demo user =====
        user = User(
            full_name="Demo User",
            email="demo@intellibank.com",
            phone="03001234567",
            hashed_password="demo",
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"👤 Created user: {user.full_name}")

        # ===== 2. Create accounts =====
        NUM_ACCOUNTS = 20
        accounts = []
        for i in range(NUM_ACCOUNTS):
            acc = Account(
                user_id=user.id,
                account_number=f"ACC{10000 + i}",
                account_type=random.choice(["savings", "current", "business"]),
                balance=round(random.uniform(10000, 500000), 2),
                risk_score=round(random.uniform(0.0, 0.5), 2),
                is_blocked=False,
            )
            db.add(acc)
            accounts.append(acc)
        db.commit()
        for acc in accounts:
            db.refresh(acc)
        print(f"🏦 Created {NUM_ACCOUNTS} accounts")

        # ===== 3. Convert rows to transactions =====
        base_time = datetime.utcnow() - timedelta(days=30)
        inserted = 0

        for idx, row in df.iterrows():
            is_fraud = bool(row["Class"] == 1)
            fraud_score = round(random.uniform(0.7, 0.99), 3) if is_fraud else round(random.uniform(0.0, 0.4), 3)

            seconds = int(row["Time"])
            txn_time = base_time + timedelta(seconds=seconds)

            acc = random.choice(accounts)
            txn_type = random.choice(["transfer", "withdrawal", "payment", "deposit"])
            description = f"Real data — V1={row['V1']:.2f}, V2={row['V2']:.2f}" if is_fraud else "Regular transaction"

                        # For transfer: use two accounts. Otherwise use from_account_id only.
            if txn_type == "transfer":
                other_acc = random.choice([a for a in accounts if a.id != acc.id])
                from_id = acc.id
                to_id = other_acc.id
            else:
                from_id = acc.id
                to_id = None

            txn = Transaction(
                transaction_id=f"TXN{uuid.uuid4().hex[:10].upper()}",
                from_account_id=from_id,
                to_account_id=to_id,
                transaction_type=txn_type,
                amount=round(float(row["Amount"]), 2),
                description=description,
                fraud_score=fraud_score,
                is_fraud=is_fraud,
                status="flagged" if is_fraud else "success",
                created_at=txn_time,
            )
            db.add(txn)
            inserted += 1

            if inserted % 500 == 0:
                db.commit()
                print(f"   ⏳ Inserted {inserted:,} transactions...")

        db.commit()
        print(f"✅ Inserted {inserted:,} transactions")

        # ===== 4. Summary =====
        total = db.query(Transaction).count()
        fraud_count = db.query(Transaction).filter(Transaction.is_fraud == True).count()
        print(f"\n📊 Summary:")
        print(f"   Total transactions: {total:,}")
        print(f"   Frauds: {fraud_count:,}")
        print(f"   Accounts: {db.query(Account).count()}")

    finally:
        db.close()


if __name__ == "__main__":
    load_real_data()