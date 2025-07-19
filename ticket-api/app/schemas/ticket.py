from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    open = "Open"
    in_progress = "In Progress"
    resolved = "Resolved"
    closed = "Closed"

class TicketCreate(BaseModel):
    subject: str
    description: Optional[str]

class TicketUpdate(BaseModel):
    status: Optional[StatusEnum]
    resolution_notes: Optional[str]

class TicketAssign(BaseModel):
    agent_id: str

class TicketOut(BaseModel):
    id: str
    subject: str
    description: Optional[str]
    customer_id: str
    agent_id: Optional[str]
    status: StatusEnum
    resolution_notes: Optional[str]
    last_updated: datetime
    embed_token: str  # ✅ ADD THIS

    class Config:
        orm_mode = True


class TicketEmbedOut(BaseModel):
    subject: str
    status: StatusEnum
    last_updated: datetime
    link: str
