from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.schemas import UserOut
from app.db import get_db
from app.models import User

router = APIRouter(prefix="/me", tags=["Users"])

@router.get("", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
