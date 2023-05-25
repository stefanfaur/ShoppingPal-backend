import requests
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File
from app.models import Receipt, Item, ReceiptJ, ItemJ
from app.services import engine, create_db_and_tables
from app.services import add_receipt, add_item_to_receipt
from app.services import SessionLocal, get_db
from datetime import date as dated

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
    
db = SessionLocal()

app = FastAPI()

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    image_contents = await file.read()
    
    response = requests.post('https://ocr.asprise.com/api/v1/receipt', files={'file': ('image.jpg', image_contents)})
    
    #extract stuff from the response
    receipts = response.json()['receipts']
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
async def save_receipt(receipt: Receipt):
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