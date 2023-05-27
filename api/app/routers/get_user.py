from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.get_db import get_db
from app.models.sql_models import Userd

router = APIRouter()

@router.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(Userd).filter(Userd.user_id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": db_user.user_id, "is_admin": db_user.is_admin}