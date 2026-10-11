from langchain.tools import tool
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        pass

@tool
def get_total_transactions() -> str:
    """Returns the total number of transactions in the system."""
    db = SessionLocal()
    count = db.query(Transaction).count()
    db.close()
    return f"Total transactions in the system: {count}"

@tool
def get_fraud_transactions() -> str:
    """Returns the count and details of fraud transactions."""
    db = SessionLocal()
    frauds = db.query(Transaction).filter(Transaction.is_fraud == True).all()
    db.close()
    if not frauds:
        return "Currently there are no fraud transactions detected."
    result = f"Total fraud transactions: {len(frauds)}\n\n"
    for t in frauds[:5]:
        result += f"- ID: {t.transaction_id} | Amount: Rs {t.amount:,.0f} | Score: {t.fraud_score} | {t.description or t.transaction_type}\n"
    return result

@tool
def get_high_risk_transactions() -> str:
    """Returns high risk transactions with fraud score >= 0.5"""
    db = SessionLocal()
    high_risk = db.query(Transaction).filter(Transaction.fraud_score >= 0.5).order_by(Transaction.fraud_score.desc()).limit(8).all()
    db.close()
    if not high_risk:
        return "No high-risk transactions found."
    result = f"High-risk transactions (score >= 0.5): {len(high_risk)}\n\n"
    for t in high_risk:
        result += f"- {t.transaction_id} | Rs {t.amount:,.0f} | Score: {t.fraud_score} | {t.transaction_type}\n"
    return result

@tool
def get_account_info(account_id: int) -> str:
    """Get details of a specific account by its ID. Example: account_id=1"""
    db = SessionLocal()
    account = db.query(Account).filter(Account.id == account_id).first()
    db.close()
    if not account:
        return f"Account with ID {account_id} not found."
    status = "Blocked" if account.is_blocked else "Active"
    return (f"Account Number: {account.account_number}\n"
            f"Type: {account.account_type}\n"
            f"Balance: Rs {account.balance:,.2f}\n"
            f"Status: {status}\n"
            f"Risk Score: {account.risk_score}\n"
            f"Block Reason: {account.block_reason or 'None'}")

@tool
def get_blocked_accounts() -> str:
    """Returns list of all blocked accounts."""
    db = SessionLocal()
    accounts = db.query(Account).filter(Account.is_blocked == True).all()
    db.close()
    if not accounts:
        return "No accounts are currently blocked."
    result = "Blocked Accounts:\n"
    for a in accounts:
        result += f"- {a.account_number} | Reason: {a.block_reason or 'N/A'}\n"
    return result

@tool
def get_recent_transactions(limit: int = 5) -> str:
    """Returns the most recent transactions. Default limit is 5."""
    db = SessionLocal()
    txns = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(limit).all()
    db.close()
    if not txns:
        return "No transactions found."
    result = f"Last {limit} transactions:\n\n"
    for t in txns:
        tag = "FRAUD" if t.is_fraud else "Safe"
        result += f"- {t.transaction_id} | Rs {t.amount:,.0f} | {t.transaction_type} | Score: {t.fraud_score} | {tag}\n"
    return result

@tool
def get_system_summary() -> str:
    """Returns overall system summary: accounts, transactions, fraud, balance etc."""
    db = SessionLocal()
    total_acc = db.query(Account).count()
    total_txn = db.query(Transaction).count()
    fraud = db.query(Transaction).filter(Transaction.is_fraud == True).count()
    blocked = db.query(Account).filter(Account.is_blocked == True).count()
    total_bal = sum(a.balance for a in db.query(Account).all())
    db.close()
    return (f"IntelliBank System Summary:\n"
            f"- Total Accounts: {total_acc}\n"
            f"- Total Transactions: {total_txn}\n"
            f"- Fraud Detected: {fraud}\n"
            f"- Blocked Accounts: {blocked}\n"
            f"- Total Balance: Rs {total_bal:,.2f}")

@tool
def get_total_balance() -> str:
    """Returns total balance across all accounts."""
    db = SessionLocal()
    total = sum(a.balance for a in db.query(Account).all())
    db.close()
    return f"Total balance across all accounts: Rs {total:,.2f}"