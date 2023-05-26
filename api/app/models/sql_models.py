from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List

class Receipt(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str 
    shop_name: str
    total: float
    date: datetime 
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