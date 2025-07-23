from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.models.ticket import TicketStatus

class TicketCreate(BaseModel):
    subject: str
    description: str

class TicketUpdate(BaseModel):
    status: Optional[TicketStatus]
    resolution_notes: Optional[str] = None

class TicketAssign(BaseModel):
    agent_id: UUID

class TicketOut(BaseModel):
    id: UUID
    subject: str
    description: str
    status: TicketStatus
    agent_id: Optional[UUID]
    embed_token: UUID
    last_updated: datetime

    class Config:
        orm_mode = True

class TicketEmbed(BaseModel):
    subject: str
    status: TicketStatus
    last_updated: datetime
    link: str