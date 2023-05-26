from fastapi import APIRouter, HTTPException, File, UploadFile
from datetime import date as dated
import requests

router = APIRouter()

@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    image_contents = await file.read()
    
    response = requests.post('https://ocr.asprise.com/api/v1/receipt', files={'file': ('image.jpg', image_contents)})
    
    #extract stuff from the response
    receipts = response.json()['receipts']
    success = response.json()['success']
    
    if success == False:
        raise HTTPException(status_code=400, detail="OCR failed, check quota")
    
    merchant = receipts[0]['merchant_name'] if receipts[0]['merchant_name'] is not None else "Unknown"
    date = receipts[0]['date'] if receipts[0]['date'] is not None else dated.today()
    items = receipts[0]['items'] if receipts[0]['items'] is not None else []
    total = receipts[0]['total'] if receipts[0]['total'] is not None else 0.0
    
    #format the items and 'handle errors'
    formatted_items = []
    for item in items:
        description = item['description'] if item['description'] is not None else "Unknown"
        unitPrice = item["unitPrice"] if item["unitPrice"] is not None else 0.0
        qty = item['qty'] if item['qty'] is not None else 1
        formatted_items.append({"description": description, "qty": qty, "unitPrice": unitPrice})

    #return the formatted receipt as a json to be checked by user in frontend
    return {
            "merchant_name": merchant,
            "date": date,
            "total": total,
            "items": formatted_items,
    }