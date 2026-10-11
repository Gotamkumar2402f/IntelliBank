from app.core.database import SessionLocal
from app.models.account import Account
from app.models.transaction import Transaction
from app.jarvis.llm import ask_llm, summarize_pdf
import re


def get_db_context() -> str:
    """Build a summary of bank data for LLM context."""
    db = SessionLocal()
    try:
        total_accounts = db.query(Account).count()
        total_txns = db.query(Transaction).count()
        fraud_txns = db.query(Transaction).filter(Transaction.is_fraud == True).count()
        total_balance = sum(a.balance for a in db.query(Account).all())

        # Recent high-risk transactions
        recent_high = (
            db.query(Transaction)
            .filter(Transaction.fraud_score >= 0.5)
            .order_by(Transaction.created_at.desc())
            .limit(5)
            .all()
        )
        high_risk_str = "\n".join(
            f"  • {t.transaction_id}: Rs {t.amount:,.0f} (score {t.fraud_score})"
            for t in recent_high
        ) or "  (none)"

        return (
            f"📊 BANK SUMMARY:\n"
            f"- Total accounts: {total_accounts}\n"
            f"- Total transactions: {total_txns}\n"
            f"- Fraud detected: {fraud_txns}\n"
            f"- Total balance: Rs {total_balance:,.2f}\n"
            f"- Recent high-risk transactions:\n{high_risk_str}"
        )
    finally:
        db.close()


def process_query(query: str) -> str:
    """Main Jarvis brain — LLM with rule-based fast paths."""
    q = query.lower().strip()

    # Get PDF text from session (Streamlit)
    pdf_text = None
    try:
        import streamlit as st
        pdf_text = st.session_state.get("pdf_text", None)
    except Exception:
        pass

    # ============================================================
    # FAST RULE-BASED PATHS (offline, instant)
    # ============================================================

    # Fraud quick check
    if "fraud" in q and ("show" in q or "list" in q or "dikhao" in q):
        db = SessionLocal()
        try:
            frauds = db.query(Transaction).filter(Transaction.is_fraud == True).all()
            if not frauds:
                return "✅ No fraud transactions detected. All systems are secure."
            lines = [f"🚨 **{len(frauds)} fraud transactions found:**"]
            for t in frauds[:5]:
                lines.append(f"• `{t.transaction_id}` — Rs {t.amount:,.0f} (score: {t.fraud_score})")
            return "\n".join(lines)
        finally:
            db.close()

    # Account balance quick check
    m = re.search(r"account\s*(\d+)", q)
    if m and "balance" in q:
        db = SessionLocal()
        try:
            acc = db.query(Account).filter(Account.id == int(m.group(1))).first()
            if acc:
                return f"💳 Account **{acc.account_number}** has a balance of **Rs {acc.balance:,.2f}**."
            return "❌ Account not found."
        finally:
            db.close()

    # ============================================================
    # LLM-POWERED RESPONSE (Groq)
    # ============================================================
    try:
        db_context = get_db_context()
        return ask_llm(query, pdf_text=pdf_text, db_context=db_context)
    except Exception as e:
        # Fallback 1: PDF summary if relevant
        if pdf_text and any(kw in q for kw in ["pdf", "document", "summarize", "summary"]):
            return summarize_pdf(pdf_text)
        # Fallback 2: Error message
        return f"⚠️ AI service unavailable: {str(e)}"


def summarize_pdf_text(pdf_text: str) -> str:
    """Wrapper for PDF summarization."""
    return summarize_pdf(pdf_text)