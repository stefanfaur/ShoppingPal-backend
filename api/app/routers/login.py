from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.get_db import get_db
from app.models.sql_models import Userd
from app.models.json_models import UserJ

router = APIRouter()

@router.post("/users/", response_model=UserJ)
def create_user(user: UserJ, db: Session = Depends(get_db)):
    db_user = Userd(user_id=user.user_id, user_email=user.user_email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user