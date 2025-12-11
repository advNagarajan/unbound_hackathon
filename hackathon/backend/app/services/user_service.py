# backend/app/services/user_service.py

import secrets
from sqlalchemy.orm import Session
from app.models import User
from app.services.audit_service import write_audit_log

def create_user(db: Session, username: str, role: str, credits: int, admin_id: int):
    api_key = secrets.token_hex(20)

    user = User(
        username=username,
        role=role,
        credits=credits,
        api_key=api_key
    )

    db.add(user)
    db.commit()

    write_audit_log(db, actor_user_id=admin_id, action="create_user", details=f"Created {username}")

    return user, api_key


def update_credits(db: Session, user_id: int, credits: int, admin_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.credits = credits
    db.commit()

    write_audit_log(db, admin_id, "update_credits", f"Set credits for {user.username} to {credits}")
    return user
