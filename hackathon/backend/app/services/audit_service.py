from sqlalchemy.orm import Session
from app.models import AuditLog

def write_audit_log(db: Session, actor_user_id: int, action: str, details: str = ""):
    log = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        details=details
    )
    db.add(log)
    db.commit()
