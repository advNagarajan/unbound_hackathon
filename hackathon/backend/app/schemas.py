from pydantic import BaseModel
from datetime import datetime


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    credits: int
    created_at: datetime

    class Config:
        orm_mode = True

class RuleOut(BaseModel):
    id: int
    pattern: str
    action: str
    priority: int

    class Config:
        orm_mode = True


class CommandOut(BaseModel):
    id: int
    command_text: str
    status: str
    credits_charged: int
    result_log: str | None
    timestamp: datetime
    rule: RuleOut | None

    class Config:
        orm_mode = True

class CreateUserRequest(BaseModel):
    username: str
    role: str
    credits: int = 100

class CreateUserResponse(BaseModel):
    username: str
    api_key: str

class CreditUpdateRequest(BaseModel):
    credits: int

class CreateRuleRequest(BaseModel):
    pattern: str
    action: str
    priority: int

class AuditLogOut(BaseModel):
    id: int
    action: str
    details: str | None
    timestamp: datetime
    actor_user_id: int

    class Config:
        orm_mode = True

