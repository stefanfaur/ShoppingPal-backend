from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from app.models import Receipt, Item
from app.services import engine, create_db_and_tables

app = FastAPI()

#define authorizations for middleware components
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#create db and schema if it doesn't exist on startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()