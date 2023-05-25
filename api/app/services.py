from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime
from app.models import Receipt, Item
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
