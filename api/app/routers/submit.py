from fastapi import APIRouter, Depends
from app.models.json_models import ReceiptJ
from sqlalchemy.orm import Session
from app.services.get_db import get_db
from app.services.db_interaction import add_item_to_receipt, add_receipt

router = APIRouter()

#temp user ID, until auth is implemented
user_id = 1

@router.post("/save-receipt/")
async def save_receipt(receipt: ReceiptJ, db: Session = Depends(get_db)):
    merchant = receipt.merchant_name 
    date = receipt.date
    total = receipt.total
    items = receipt.items

    new_receipt = add_receipt(db, merchant, merchant, total, user_id)

    for item in items:
        description = item.description
        unitPrice = item.unitPrice
        qty = item.qty

        add_item_to_receipt(db, new_receipt.id, description, qty, unitPrice)

    return {"status": "success"} 