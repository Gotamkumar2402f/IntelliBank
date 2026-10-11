from app.core.database import SessionLocal
from app.models.user import User
from app.models.account import Account
from app.models.transaction import Transaction
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    db = SessionLocal()

    # Check if data already exists
    if db.query(User).first():
        print("Data already exists. Skipping...")
        db.close()
        return

    # Create Admin User
    admin = User(
        full_name="Admin User",
        email="admin@intellibank.com",
        phone="03001234567",
        hashed_password=pwd_context.hash("admin123"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)

    # Create Normal User
    user1 = User(
        full_name="Ali Khan",
        email="ali@example.com",
        phone="03009876543",
        hashed_password=pwd_context.hash("ali123")
    )
    db.add(user1)
    db.commit()
    db.refresh(user1)

    # Create Accounts
    acc1 = Account(
        account_number="PK100000000001",
        user_id=user1.id,
        account_type="savings",
        balance=50000.0
    )
    acc2 = Account(
        account_number="PK100000000002",
        user_id=user1.id,
        account_type="current",
        balance=120000.0
    )
    db.add(acc1)
    db.add(acc2)
    db.commit()
    db.refresh(acc1)
    db.refresh(acc2)

    # Create some Transactions
    t1 = Transaction(
        transaction_id=str(uuid.uuid4())[:12].upper(),
        to_account_id=acc1.id,
        amount=50000.0,
        transaction_type="deposit",
        status="success",
        description="Initial deposit"
    )
    t2 = Transaction(
        transaction_id=str(uuid.uuid4())[:12].upper(),
        from_account_id=acc1.id,
        to_account_id=acc2.id,
        amount=10000.0,
        transaction_type="transfer",
        status="success",
        description="Transfer to current account"
    )
    db.add(t1)
    db.add(t2)
    db.commit()

    print("Sample data created successfully!")
    print(f"User: Ali Khan | Accounts: {acc1.account_number} & {acc2.account_number}")
    db.close()

if __name__ == "__main__":
    seed()