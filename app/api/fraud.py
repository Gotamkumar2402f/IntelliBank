from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.services import fraud_service
from app.schemas.transaction import TransactionOut

router = APIRouter(prefix="/fraud", tags=["Fraud Detection"])

@router.post("/analyze/{transaction_id}")
def analyze_single_transaction(transaction_id: int, db: Session = Depends(get_db)):
    result = fraud_service.analyze_transaction(db, transaction_id)
    if not result:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return result

@router.post("/analyze-all")
def analyze_all(db: Session = Depends(get_db)):
    results = fraud_service.analyze_all_transactions(db)
    return {
        "message": f"Analyzed {len(results)} transactions",
        "results": results
    }

@router.get("/flagged", response_model=List[TransactionOut])
def get_flagged_transactions(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    return fraud_service.get_fraud_transactions(db, skip, limit)

@router.get("/high-risk")
def get_high_risk(min_score: float = 0.5, limit: int = 20, db: Session = Depends(get_db)):
    transactions = fraud_service.get_high_risk_transactions(db, min_score, limit)
    return {
        "count": len(transactions),
        "transactions": transactions
    }