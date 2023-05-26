import requests
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from app.models.json_models import ReceiptJ
from app.models.sql_models import Receipt
from app.services.db_interaction import engine, create_db_and_tables
from app.services.db_interaction import add_receipt, add_item_to_receipt
from app.services.db_interaction import get_user_receipts, get_receipt_with_items
from app.services.db_interaction import SessionLocal
from app.services.get_db import get_db
from datetime import date as dated
from typing import List
from app.routers import upload, submit, get_receipt_items, get_user_receipts

#fixing this when login is implemented
user_id = "1"

app = FastAPI()

#include routes
app.include_router(submit.router)
app.include_router(upload.router)
app.include_router(get_receipt_items.router)
app.include_router(get_user_receipts.router)

#create db and schema if it doesn't exist on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#define authorizations for middleware components
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

