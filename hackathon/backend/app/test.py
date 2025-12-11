from db import SessionLocal
from models import Rule

db = SessionLocal()

for rule in db.query(Rule).all():
    print(rule.id, rule.pattern, rule.action, rule.priority)
