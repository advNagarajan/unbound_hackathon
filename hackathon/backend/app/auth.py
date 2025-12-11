from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User

API_KEY_HEADER = APIKeyHeader(name="Authorization")

def get_current_user(
    api_key_header: str = Depends(API_KEY_HEADER),
    db: Session = Depends(get_db)
):
    # Expect header: "ApiKey <key>"
    if not api_key_header.startswith("ApiKey "):
        raise HTTPException(status_code=401, detail="Invalid API Key format")

    raw_key = api_key_header.replace("ApiKey ", "").strip()

    user = db.query(User).filter(User.api_key == raw_key).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return current_user