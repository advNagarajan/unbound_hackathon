# backend/app/seed.py

import secrets
from sqlalchemy.orm import Session
from app.models import User, Rule
from app.services.audit_service import write_audit_log

def run_seed(db: Session):

    # 1️⃣ Check if admin exists → if yes, DO NOT seed again
    admin = db.query(User).filter(User.username == "admin").first()
    if admin:
        return  # already seeded, skip entirely

    # 2️⃣ Create admin user
    api_key = secrets.token_hex(20)

    admin = User(
        username="admin",
        api_key=api_key,
        role="admin",
        credits=9999
    )

    db.add(admin)
    db.commit()

    # 3️⃣ Seed default rules
    default_rules = [
        (r":\(\)\s*{ :\|:& };\:", "AUTO_REJECT"),
        (r"rm\s+-rf\s+/", "AUTO_REJECT"),
        (r"mkfs\.", "AUTO_REJECT"),
        (r"git\s+(status|log|diff)", "AUTO_ACCEPT"),
        (r"^(ls|cat|pwd|echo)", "AUTO_ACCEPT"),
    ]

    priority = 1
    for pat, act in default_rules:
        rule = Rule(
            pattern=pat,
            action=act,
            priority=priority,
            created_by=admin.id
        )
        db.add(rule)
        priority += 1

    db.commit()

    # 4️⃣ Log seeding
    write_audit_log(db, actor_user_id=admin.id, action="system_seed", details="Initial admin + rules created")

    # 5️⃣ Print admin key once
    print("\n==============================")
    print(" Default Admin Created ")
    print(" Username: admin")
    print(f" API Key: {api_key}")
    print("==============================\n")


# curl.exe -H "Authorization: ApiKey ba64e61f199129897d108693f683878273d30371" http://localhost:8000/me
'''
curl.exe -X POST http://localhost:8000/commands `
  -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" `
  -H "Content-Type: application/json" `
  -d "{\"command_text\": \"ls -la\"}"

curl -X POST http://localhost:8000/commands ^
   -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
   -H "Content-Type: application/json" ^
   -d "{\"command_text\": \"ls -la\"}"

curl -X POST http://localhost:8000/commands ^
   -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
   -H "Content-Type: application/json" ^
   -d "{\"command_text\": \"rm -rf /\"}"

curl -X POST http://localhost:8000/commands ^
   -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
   -H "Content-Type: application/json" ^
   -d "{\"command_text\": \"lol\"}"

curl -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" http://localhost:8000/commands

curl -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" http://localhost:8000/admin/users

curl -X POST http://localhost:8000/admin/users ^
  -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"johndoe\", \"role\": \"member\", \"credits\": 100}"


  
john thing: 2ba09f004da4a23205b3e35d2fee25c3d2b3c6c0"
curl -H "Authorization: ApiKey 2ba09f004da4a23205b3e35d2fee25c3d2b3c6c0" http://localhost:8000/admin/users

curl.exe -H "Authorization: ApiKey 2ba09f004da4a23205b3e35d2fee25c3d2b3c6c0" http://localhost:8000/me

curl.exe -X POST http://localhost:8000/admin/rules ^
  -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
  -H "Content-Type: application/json" ^
  -d "{\"pattern\": \"echo hello\", \"action\": \"AUTO_ACCEPT\", \"priority\": 10}"
this is rule add

curl.exe -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" http://localhost:8000/admin/rules

curl.exe -X POST http://localhost:8000/commands ^
  -H "Authorization: ApiKey 6c0548256bea4bc72239db0003622e729c580260" ^
  -H "Content-Type: application/json" ^
  -d "{\"command_text\": \"ls -la\"}"

python -m cli.app login 2ba09f004da4a23205b3e35d2fee25c3d2b3c6c0

python -m cli.app login 6c0548256bea4bc72239db0003622e729c580260
'''