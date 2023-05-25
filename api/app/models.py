from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel
from typing import List
from sqlmodel import Field, Relationship

class Receipt(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    shop_name: str
    total: float
    date: datetime = Field(default=datetime.now())
    user_id: str
    items: List["Item"] = Relationship(back_populates="receipt")
    class Config:
        orm_mode = True
    
class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    receipt_id: int = Field(default=None, foreign_key="receipt.id")
    name: str
    count: int
    price: float
    receipt: Receipt = Relationship(back_populates="items")

    
#define models to work with JSON
class ItemJ(BaseModel):
    description: str
    qty: int
    unitPrice: float

class ReceiptJ(BaseModel):
    merchant_name: str
    date: str
    total: float
    items: List[ItemJ]
