from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker, joinedload
from typing import List
from datetime import datetime
from app.models.sql_models import Receipt, Item, Userd
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def add_receipt(db: Session, name: str, shop_name: str, total: float, user_id: str):
    new_receipt = Receipt(name=name, shop_name=shop_name, total=total, date=datetime.now(), user_id=user_id)
    db.add(new_receipt)
    db.commit()
    db.refresh(new_receipt)
    return new_receipt

def add_item_to_receipt(db: Session, receipt_id: int, name: str, count: int, price: float):
    new_item = Item(receipt_id=receipt_id, name=name, count=count, price=price)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def get_user_receipts(db: Session, user_id: str) -> List[Receipt]:
    result = db.execute(select(Receipt).where(Receipt.user_id == user_id))
    return result.scalars().all()

def get_receipt_with_items(db: Session, receipt_id: int) -> List[Item]:
    result = db.execute(select(Item).where(Item.receipt_id == receipt_id))
    receipt_query = db.execute(select(Receipt).where(Receipt.id == receipt_id))
    if result is None:
        return None
    receipt = result.scalars().all()
    receipt_res = receipt_query.scalars().first()
    print(receipt)
    return receipt
    '''
    return {
        "id": receipt_id,
        "name": receipt_res.name,
        "shop_name": receipt_res.shop_name,
        "total": receipt_res.total,
        "date": receipt_res.date,
        "items": [item.dict() for item in receipt]}
        '''
    
