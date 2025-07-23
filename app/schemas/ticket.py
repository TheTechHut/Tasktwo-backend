
from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from enum import Enum
from datetime import datetime


class StatusEnum(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class TicketCreate(BaseModel):
    subject: str
    description: str


class TicketUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    resolution_notes: Optional[str] = None


class TicketAssign(BaseModel):
    agent_id: str


class TicketResponse(BaseModel):
    id: UUID
    subject: str
    description: str
    customer_id: str
    agent_id: Optional[str]
    status: StatusEnum
    embed_token: UUID
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True
