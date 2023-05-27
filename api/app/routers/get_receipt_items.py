from fastapi import APIRouter, Depends, HTTPException
from app.services.db_interaction import get_receipt_with_items
from app.services.get_db import get_db
from app.models.sql_models import Receipt
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/receipts/{receipt_id}/items")
def read_receipt_with_items(receipt_id: int, db: Session = Depends(get_db)):
    items = get_receipt_with_items(db, receipt_id)
    if items is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return {"items": [item for item in items]}