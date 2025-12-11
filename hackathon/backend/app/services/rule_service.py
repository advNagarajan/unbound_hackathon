# backend/app/services/rule_service.py

import re
from sqlalchemy.orm import Session
from app.models import Rule
from app.services.audit_service import write_audit_log

def create_rule(db: Session, pattern: str, action: str, priority: int, admin_id: int):
    # Validate regex
    try:
        re.compile(pattern)
    except:
        return None, "Invalid regex pattern"

    rule = Rule(
        pattern=pattern,
        action=action,
        priority=priority,
        created_by=admin_id
    )

    db.add(rule)
    db.commit()

    write_audit_log(db, admin_id, "create_rule", f"Pattern: {pattern}")
    return rule, None


def delete_rule(db: Session, rule_id: int, admin_id: int):
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        return False

    db.delete(rule)
    db.commit()

    write_audit_log(db, admin_id, "delete_rule", f"Rule ID: {rule_id}")
    return True
