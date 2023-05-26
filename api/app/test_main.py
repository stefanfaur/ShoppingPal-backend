import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#####################################
#         ROUTES TESTING            #
#####################################

def test_upload_image():
    with open("app/test_image.jpg", "rb") as image_file:
        response = client.post("/upload-image/", files={"file": ("image.jpg", image_file, "image/jpg")})
    assert response.status_code == 200
    data = response.json()
    assert "merchant_name" in data
    assert "date" in data
    assert "total" in data
    assert "items" in data

def test_save_receipt():
    test_receipt = {
        "merchant_name": "PREMIER RESTAURANTS ROMANIA S.R.L",
        "date": "2023-05-24",
        "total": 148.8,
        "items": [
    {
      "description": "MAIONEZA =",
      "qty": 1,
      "unitPrice": 3.9
    },
    {
      "description": "XL CHEESYCHICKEN =",
      "qty": 1,
      "unitPrice": 34.3
    },
    {
      "description": "COLA MARE",
      "qty": 1,
      "unitPrice": 7.6
    },
    {
      "description": "CHEESY CHICKEN =",
      "qty": 2,
      "unitPrice": 29
    },
    {
      "description": "DUBLU CHEESE =",
      "qty": 3,
      "unitPrice": 15
    }
  ]
        }

    response = client.post("/save-receipt/", json=test_receipt)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
def test_read_user_receipts():
    user_id = '1' 
    response = client.get(f"/receipts/{user_id}")
    assert response.status_code == 200
    assert response.json()

def test_read_receipt_with_items():
    receipt_id = 1 
    response = client.get(f"/receipts/{receipt_id}/items")
    assert response.status_code == 200
    assert response.json()

#####################################
#         DATABASE TESTING          #
#####################################
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from datetime import datetime
from app.services.get_db import get_db
import uuid
import os
from app.services.db_interaction import add_receipt, add_item_to_receipt, get_user_receipts, get_receipt_with_items

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    return TestingSessionLocal()

def test_add_receipt(db):
    # create unique user_id for each test
    user_id = str(uuid.uuid4())

    # Add a receipt and verify
    receipt = add_receipt(db, "test_receipt", "test_shop", 50.0, user_id)
    retrieved_receipts = get_user_receipts(db, user_id)
    assert len(retrieved_receipts) == 1
    assert retrieved_receipts[0].id == receipt.id

    # clean up
    db.delete(receipt)
    db.commit()

def test_add_item_to_receipt(db):
    # create unique user_id for each test
    user_id = str(uuid.uuid4())

    # Add a receipt
    receipt = add_receipt(db, "test_receipt", "test_shop", 50.0, user_id)

    # Add an item and verify
    item = add_item_to_receipt(db, receipt.id, "test_item", 2, 25.0)
    retrieved_receipt = get_receipt_with_items(db, receipt.id)
    assert len(retrieved_receipt.items) == 1
    assert retrieved_receipt.items[0].id == item.id

    # clean up
    db.delete(item)
    db.delete(receipt)
    db.commit()
