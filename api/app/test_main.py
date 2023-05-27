from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from sqlmodel import SQLModel
import pytest
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_app():
    return TestClient(app)

@pytest.fixture
def db_cleanup():
    db = SessionLocal()
    yield db
    # Clean up the database after each test
    #for table in reversed(SQLModel.metadata.sorted_tables):
    #    db.execute(table.delete())
    db.commit()
    
def test_upload_image(test_app, db_cleanup: Session):
    file_name = 'app/test_image.jpg'
    with open(file_name, 'rb') as file:
        response = test_app.post("/upload-image/", files={"file": (file_name, file, "image/jpeg")})
    assert response.status_code == 200
    
def test_create_user(test_app, db_cleanup: Session):
    response = test_app.post("/users/", json={"user_id": "new_user_id", "user_email": "new_user_email"})
    assert response.status_code == 200
    assert response.json()["user_id"] == "new_user_id"

def test_save_receipt(test_app, db_cleanup: Session):
    response = test_app.post("/save-receipt/", json={"merchant_name": "test_merchant", "date": "2023-01-01", "total": 123.45, "items": [{"description": "item1", "qty": 1, "unitPrice": 123.45}]})
    assert response.status_code == 200
    assert response.json()["status"] == "success"

def test_read_receipt_with_items(test_app, db_cleanup: Session):
    response = test_app.get("/receipts/1/items")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_get_user(test_app, db_cleanup: Session):
    response = test_app.get("/users/new_user_id")
    assert response.status_code == 200
    assert response.json()["user_id"] == "new_user_id"

def test_read_user_receipts(test_app, db_cleanup: Session):
    response = test_app.get("/receipts/new_user_id")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


