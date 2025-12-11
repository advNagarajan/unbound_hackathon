# backend/app/main.py

from fastapi import FastAPI
from app.db import Base, engine, SessionLocal
from app.seed import run_seed
from app.routers import users, commands
from app.routers import admin_users, admin_rules, admin_audit

def create_app():
    app = FastAPI(title="Command Gateway")

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    run_seed(db)
    db.close()

    # Public routes
    app.include_router(users.router)
    app.include_router(commands.router)

    # Admin routes
    app.include_router(admin_users.router)
    app.include_router(admin_rules.router)
    app.include_router(admin_audit.router)

    return app

app = create_app()
