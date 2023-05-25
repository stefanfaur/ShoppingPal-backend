import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

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

