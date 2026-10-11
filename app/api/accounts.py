from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountOut
from app.services import account_service

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.post("/", response_model=AccountOut)
def create_new_account(account: AccountCreate, db: Session = Depends(get_db)):
    return account_service.create_account(db, account)

@router.get("/", response_model=List[AccountOut])
def list_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return account_service.get_all_accounts(db, skip, limit)

@router.get("/{account_id}", response_model=AccountOut)
def read_account(account_id: int, db: Session = Depends(get_db)):
    account = account_service.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.post("/{account_id}/block")
def block_account(account_id: int, reason: str = "Suspicious activity", db: Session = Depends(get_db)):
    account = account_service.block_account(db, account_id, reason)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account blocked successfully", "account": account}

@router.post("/{account_id}/unblock")
def unblock_account(account_id: int, db: Session = Depends(get_db)):
    account = account_service.unblock_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": "Account unblocked successfully", "account": account}