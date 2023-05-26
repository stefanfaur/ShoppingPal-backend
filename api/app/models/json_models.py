from pydantic import BaseModel
from typing import List

class ItemJ(BaseModel):
    description: str
    qty: int
    unitPrice: float

class ReceiptJ(BaseModel):
    merchant_name: str 
    date: str
    total: float
    items: List[ItemJ]
