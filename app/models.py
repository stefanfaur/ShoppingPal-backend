from sqlmodel import SQLModel, Field
from datetime import datetime


class Receipt(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    shop_name: str
    total: float
    date: datetime = Field(default=datetime.now())
    user_id: str
    class Config:
        orm_mode = True
    
class Item(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    receipt_id: int = Field(default=None, foreign_key="receipt.id")
    name: str
    count: int
    price: float