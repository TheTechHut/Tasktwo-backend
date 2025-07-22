from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime
from Ticketing_System.enums import TicketStatus  # Enum for ticket status


# -------------------------------
# Ticket Embed Response Schema
# -------------------------------

class TicketEmbedResponse(BaseModel):
    """
        Schema for representing a lightweight, embedded view of a ticket.
        """

    subject: str
    status: TicketStatus
    last_updated: datetime
    link: str

# -------------------------------
# Base Ticket Schema
# -------------------------------
class TicketBase(BaseModel):
    """
        Shared fields used for creating or viewing tickets.
        """
    subject: str
    description: str
    priority: int

# -------------------------------
# Ticket Create Schema (empty for now)
# -------------------------------
class TicketCreate(BaseModel):
    """
       Placeholder for ticket creation.
       """
    pass # Fields may be inherited or added in the future

class TicketUpdate(BaseModel):
    """
        Fields that can be updated on a ticket.
        """
    status: Optional[TicketStatus]
    resolution_notes: Optional[str] = None

# -------------------------------
# Ticket Response Schema
# -------------------------------
class TicketResponse(BaseModel):
    """
        Full representation of a ticket as returned from the database or API.
        """
    ticket_id: UUID
    user_id: int
    agent_id: Optional[int]
    subject: str
    description: str
    status: TicketStatus
    priority: int
    created_at: datetime
    updated_at: datetime

model_config = {
    'from_attributes': True
}