# backend/app/services/command_service.py

from sqlalchemy.orm import Session
from app.models import Command, User
from app.services.rule_engine import match_rule
from app.services.audit_service import write_audit_log

EXECUTION_COST = 1  # credits per execution

def submit_command(db: Session, user: User, command_text: str):

    # 1. Check credits
    if user.credits <= 0:
        return {"status": "rejected", "reason": "Insufficient credits"}

    # 2. Match rule
    rule = match_rule(db, command_text)

    # If no rule → reject by default (safe behavior)
    if rule is None:
        cmd = Command(
            user_id=user.id,
            command_text=command_text,
            status="rejected",
            rule_id=None,
            credits_charged=0,
            result_log="No matching rule. Command rejected."
        )
        db.add(cmd)
        db.commit()

        write_audit_log(db, user.id, "command_rejected", command_text)
        return {"status": "rejected", "reason": "No matching rule"}

    # 3. AUTO_REJECT path
    if rule.action == "AUTO_REJECT":
        cmd = Command(
            user_id=user.id,
            command_text=command_text,
            status="rejected",
            rule_id=rule.id,
            credits_charged=0,
            result_log="Rejected by rule."
        )
        db.add(cmd)
        db.commit()

        write_audit_log(db, user.id, "command_rejected", f"Rule {rule.pattern}")
        return {"status": "rejected", "reason": "Rejected by rule"}

    # 4. AUTO_ACCEPT path → simulate execution
    if rule.action == "AUTO_ACCEPT":
        result_log = f"[SIMULATED] Executed: {command_text}"

        user.credits -= EXECUTION_COST

        cmd = Command(
            user_id=user.id,
            command_text=command_text,
            status="executed",
            rule_id=rule.id,
            credits_charged=EXECUTION_COST,
            result_log=result_log
        )

        db.add(cmd)
        db.commit()

        write_audit_log(db, user.id, "command_executed", f"Rule {rule.pattern}")
        return {
            "status": "executed",
            "result": result_log,
            "remaining_credits": user.credits
        }
