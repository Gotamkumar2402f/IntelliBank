from sqlalchemy.orm import Session
from app.models.account import Account
from app.models.user import User
from app.schemas.account import AccountCreate
import random
import string

def generate_account_number():
    return "PK" + "".join(random.choices(string.digits, k=12))

def create_account(db: Session, account: AccountCreate):
    db_account = Account(
        account_number=generate_account_number(),
        user_id=account.user_id,
        account_type=account.account_type,
        balance=account.initial_balance
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()

def get_account_by_number(db: Session, account_number: str):
    return db.query(Account).filter(Account.account_number == account_number).first()

def get_all_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Account).offset(skip).limit(limit).all()

def block_account(db: Session, account_id: int, reason: str):
    account = get_account(db, account_id)
    if account:
        account.is_blocked = True
        account.block_reason = reason
        db.commit()
        db.refresh(account)
    return account

def unblock_account(db: Session, account_id: int):
    account = get_account(db, account_id)
    if account:
        account.is_blocked = False
        account.block_reason = None
        db.commit()
        db.refresh(account)
    return account