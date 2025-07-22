# FastAPI routing and dependencies
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Ticketing_System.database import get_db  # SQLAlchemy DB session
from Ticketing_System.models import Ticket  # SQLAlchemy Ticket model
from Ticketing_System.schemas import TicketCreate, TicketResponse, TicketEmbedResponse
from uuid import UUID
from Ticketing_System.testauth import get_current_user  # Auth dependency
import uuid
from typing import List

# Initialize FastAPI router
router = APIRouter(
    prefix="/tickets",
    tags=["Tickets"]  # Group under "Tickets" in Swagger UI
)

# ------------------------------------------
# 1. GET /tickets/ — Admins & Agents only
# ------------------------------------------
@router.get("/", response_model=List[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Retrieve all tickets from the system.
    Only accessible by users with 'admin' or 'agent' roles.
    """
    if user["role"] not in ["admin", "agent"]:
        raise HTTPException(status_code=403, detail="Not authorized")
    return db.query(Ticket).all()

# ------------------------------------------
# 2. GET /tickets/{ticket_id} — Restricted
# ------------------------------------------
@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: UUID, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Retrieve a specific ticket by ID.
    Admins/Agents can access any ticket.
    Customers can only view their own tickets.
    """
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id.bytes).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Only the creator can view their own ticket if they are a customer
    if user["role"] == "customer" and ticket.user_id != user["user_id"]:
        raise HTTPException(status_code=403, detail="Not allowed")
    return ticket

# ------------------------------------------
# 3. PATCH /tickets/{ticket_id} — Agent only
# ------------------------------------------
@router.patch("/{ticket_id}")
def update_ticket_status(
    ticket_id: UUID,
    status: int,
    resolution: str,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Allows agents to update the status and resolution notes of a ticket.
    """
    if user["role"] != "agent":
        raise HTTPException(status_code=403, detail="Only agents can update ticket status")

    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id.bytes).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Update ticket fields
    ticket.status = status
    ticket.description += f"\n\n[Agent Resolution Note]: {resolution}"
    db.commit()
    return {"message": "Ticket updated"}

# ------------------------------------------
# 4. PATCH /tickets/{ticket_id}/asPsAiTgCnH — Admin only
# ------------------------------------------
@router.patch("/{ticket_id}/asPsAiTgCnH")
def assign_ticket(
    ticket_id: UUID,
    agent_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    """
    Allows admins to assign a ticket to an agent.
    Also updates the ticket status to 'Assigned'.
    """
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Only admins can assign tickets")

    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id.bytes).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = 1  # Set status to 'Assigned' (integer value)
    ticket.description += f"\n\n[Assigned to agent ID {agent_id}]"
    db.commit()
    return {"message": f"Ticket assigned to agent {agent_id}"}

# ------------------------------------------
# 5. GET /tickets/embed/{token} — Public chatbot view
# ------------------------------------------

# Simulated in-memory map for embed tokens → ticket IDs
token_map = {}

@router.get("/embed/{token}", response_model=TicketResponse)
def get_embedded_ticket(token: str, db: Session = Depends(get_db)):
    """
    Public access to ticket data via token.
    Useful for chatbot integrations or sharing without login.
    """
    if token not in token_map:
        raise HTTPException(status_code=404, detail="Invalid token")

    ticket_id = token_map[token]
    ticket = db.query(Ticket).filter(Ticket.ticket_id == ticket_id.bytes).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

# ------------------------------------------
# Generate embed token — for testing
# ------------------------------------------
@router.get("/generate_embed_token/{ticket_id}")
def generate_token(ticket_id: UUID):
    """
    Utility route for generating a test embed token for a ticket.
    """
    token = str(uuid.uuid4()).replace("-", "")
    token_map[token] = ticket_id
    return {"embed_token": token}

# ------------------------------------------
# 6. GET /tickets/embed/{embed_token}
# ------------------------------------------
@router.get("/embed_simple/{embed_token}", response_model=TicketEmbedResponse)
def get_ticket_embed(embed_token: str, db: Session = Depends(get_db)):
    """
    Returns a minimal public view of the ticket with subject, status, and link.
    """
    ticket = db.query(Ticket).filter(Ticket.embed_token == embed_token).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    base_url = "http://localhost/NA"
    return {
        "subject": ticket.subject,
        "status": ticket.status,
        "last_updated": ticket.updated_at,
        "link": f"{base_url}{ticket.ticket_id}"
    }