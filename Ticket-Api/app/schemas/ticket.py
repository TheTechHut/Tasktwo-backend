from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

# Personal Notes

#In FastAPI, schemas are used to validate and shape data coming into and going out of your API.

#For easy understanding, I think of schemas as smart data forms. When a user submits data, FastAPI checks it against the schema to ensure everything is correct. If something's wrong, it sends back an error message.

#In FastAPI, we often use Pydantic models to define the structure of our data.

# This file defines the schemas for the ticketing system.


# Import the TicketStatus enum to represent ticket status values
from app.constants.status import TicketStatus

# Schema used when a customer sends in data to create a ticket
class TicketCreate(BaseModel):
    customer_id: UUID
    subject: str
    description: str

# Schema used when sending data back to users
class TicketResponse(BaseModel):
    id: UUID
    customer_id: UUID
    agent_id: Optional[UUID]
    subject: str
    description: str
    status: TicketStatus
    resolution_notes: Optional[str]
    embed_token: str                 
    last_updated: datetime


