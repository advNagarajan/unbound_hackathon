from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    api_key = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    credits = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)

    audit_logs = relationship("AuditLog", back_populates="actor")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String, nullable=False)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    actor = relationship("User", back_populates="audit_logs")

class Rule(Base):
    __tablename__ = "rules"

    id = Column(Integer, primary_key=True)
    pattern = Column(String, nullable=False)
    action = Column(String, nullable=False)  # AUTO_ACCEPT or AUTO_REJECT
    priority = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    creator = relationship("User")


class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    command_text = Column(String, nullable=False)
    status = Column(String, nullable=False)  # executed / rejected
    rule_id = Column(Integer, ForeignKey("rules.id"))
    credits_charged = Column(Integer, default=0)
    result_log = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
    rule = relationship("Rule")

