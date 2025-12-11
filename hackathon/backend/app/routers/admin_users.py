# backend/app/routers/admin_users.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import require_admin
from app.schemas import CreateUserRequest, CreateUserResponse, CreditUpdateRequest, UserOut
from app.services.user_service import create_user, update_credits
from app.models import User

router = APIRouter(prefix="/admin/users", tags=["Admin - Users"])

@router.post("", response_model=CreateUserResponse)
def admin_create_user(
    req: CreateUserRequest,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    user, api = create_user(db, req.username, req.role, req.credits, admin.id)
    return {"username": user.username, "api_key": api}


@router.get("", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(User).all()


@router.post("/{user_id}/credits", response_model=UserOut)
def admin_update_credits(
    user_id: int,
    req: CreditUpdateRequest,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    user = update_credits(db, user_id, req.credits, admin.id)
    if not user:
        raise HTTPException(404, "User not found")
    return user
