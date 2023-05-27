from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.sql_models import Receipt
from sqlalchemy.orm import Session
from app.services.db_interaction import get_user_receipts
from app.services.get_db import get_db

router = APIRouter()

@router.get("/receipts/{user_id}")
def read_user_receipts(user_id: str, db: Session = Depends(get_db)):
    receipts = get_user_receipts(db, user_id)
    if receipts is None:
        raise HTTPException(status_code=404, detail="Receipts not found")
    return {"receipts": [receipt.dict() for receipt in receipts]}
