# backend/app/routers/admin_rules.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import require_admin
from app.db import get_db
from app.schemas import CreateRuleRequest, RuleOut
from app.services.rule_service import create_rule, delete_rule
from app.models import Rule

router = APIRouter(prefix="/admin/rules", tags=["Admin - Rules"])

@router.post("", response_model=RuleOut)
def admin_create_rule(
    req: CreateRuleRequest,
    db: Session = Depends(get_db),
    admin = Depends(require_admin)
):
    rule, err = create_rule(db, req.pattern, req.action, req.priority, admin.id)
    if err:
        raise HTTPException(400, err)
    return rule


@router.get("", response_model=list[RuleOut])
def admin_list_rules(db: Session = Depends(get_db), admin=Depends(require_admin)):
    return db.query(Rule).order_by(Rule.priority.asc()).all()


@router.delete("/{rule_id}")
def admin_delete_rule(rule_id: int, db: Session = Depends(get_db), admin = Depends(require_admin)):
    ok = delete_rule(db, rule_id, admin.id)
    if not ok:
        raise HTTPException(404, "Rule not found")
    return {"status": "deleted"}
