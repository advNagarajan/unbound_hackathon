# backend/app/services/rule_engine.py

import re
from sqlalchemy.orm import Session
from app.models import Rule

def match_rule(db: Session, command_text: str):
    rules = db.query(Rule).order_by(Rule.priority.asc()).all()

    for rule in rules:
        try:
            if re.search(rule.pattern, command_text):
                return rule
        except:
            continue

    return None  # no match found
