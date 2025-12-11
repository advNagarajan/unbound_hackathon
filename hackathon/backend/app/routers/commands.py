# backend/app/routers/commands.py

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.auth import get_current_user
from app.db import get_db
from app.models import Command, User
from app.schemas import CommandOut
from app.services.command_service import submit_command

router = APIRouter(prefix="/commands", tags=["Commands"])

class CommandRequest(BaseModel):
    command_text: str

@router.post("", response_model=dict)
def submit(cmd: CommandRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return submit_command(db, user, cmd.command_text)

@router.get("", response_model=list[CommandOut])
def history(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cmds = (
        db.query(Command)
        .filter(Command.user_id == user.id)
        .order_by(Command.timestamp.desc())
        .all()
    )
    return cmds
