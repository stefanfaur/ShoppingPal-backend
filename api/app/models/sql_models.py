from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List

class Userd(SQLModel, table=True):
    user_id: str = Field(default="1", primary_key=True)
    is_admin: bool = Field(default=False)
    user_email: str
    receipts: List["Receipt"] = Relationship(back_populates="userd")


class Receipt(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str 
    shop_name: str
    total: float
    date: datetime 
    user_id: str = Field(default=None, foreign_key="userd.user_id")
    items: List["Item"] = Relationship(back_populates="receipt")
    userd: "Userd" = Relationship(back_populates="receipts")
    class Config:
        orm_mode = True

    
class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    receipt_id: int = Field(default=None, foreign_key="receipt.id")
    name: str 
    count: int 
    price: float 
    receipt: Receipt = Relationship(back_populates="items")