import requests
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from app.models import ReceiptJ, Receipt
from app.services import engine, create_db_and_tables
from app.services import add_receipt, add_item_to_receipt
from app.services import get_user_receipts, get_receipt_with_items
from app.services import SessionLocal
from datetime import date as dated
from typing import List

#fixing this when login is implemented
user_id = "1"

app = FastAPI()

#define authorizations for middleware components
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#create db and schema if it doesn't exist on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    
#db = SessionLocal()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    image_contents = await file.read()
    
    response = requests.post('https://ocr.asprise.com/api/v1/receipt', files={'file': ('image.jpg', image_contents)})
    
    #extract stuff from the response
    receipts = response.json()['receipts']
    success = response.json()['success']
    
    if success == False:
        raise HTTPException(status_code=400, detail="OCR failed, check quota")
    
    merchant = receipts[0]['merchant_name']
    date = receipts[0]['date'] if receipts[0]['date'] is not None else dated.today()
    items = receipts[0]['items']
    total = receipts[0]['total']
    
    #format the items and 'handle errors'
    formatted_items = []
    for item in items:
        description = item['description']
        unitPrice = item["unitPrice"] if item['unitPrice'] is not None else item['amount']
        qty = item['qty'] if item['qty'] is not None else 1
        formatted_items.append({"description": description, "qty": qty, "unitPrice": unitPrice})

    #return the formatted receipt as a json to be checked by user in frontend
    return {
            "merchant_name": merchant,
            "date": date,
            "total": total,
            "items": formatted_items,
    }
    
@app.post("/save-receipt/")
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

@app.get("/receipts/{user_id}", response_model=List[Receipt])
def read_user_receipts(user_id: str, db: Session = Depends(get_db)):
    receipts = get_user_receipts(db, user_id)
    if receipts is None:
        raise HTTPException(status_code=404, detail="Receipts not found")
    return receipts

@app.get("/receipts/{receipt_id}/items", response_model=Receipt)
def read_receipt_with_items(receipt_id: int, db: Session = Depends(get_db)):
    receipt = get_receipt_with_items(db, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt