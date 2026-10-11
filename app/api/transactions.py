from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionOut
from app.services import transaction_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionOut)
def create_new_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    try:
        return transaction_service.create_transaction(db, transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[TransactionOut])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return transaction_service.get_all_transactions(db, skip, limit)

@router.get("/{transaction_id}", response_model=TransactionOut)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = transaction_service.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction