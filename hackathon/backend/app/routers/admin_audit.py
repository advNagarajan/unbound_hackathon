# backend/app/routers/admin_audit.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.db import get_db
from app.schemas import AuditLogOut
from app.models import AuditLog

router = APIRouter(prefix="/admin/audit", tags=["Admin - Audit Logs"])

@router.get("", response_model=list[AuditLogOut])
def list_audit_logs(db: Session = Depends(get_db), admin = Depends(require_admin)):
    return db.query(AuditLog).order_by(AuditLog.timestamp.desc()).all()
