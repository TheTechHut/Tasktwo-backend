from fastapi import APIRouter, HTTPException, Depends, Body
from uuid import uuid4, UUID
from typing import List

from app.models.ticket import TicketModel
from app.schemas.ticket import TicketCreate, TicketResponse
from app.auth.users import require_role, get_current_user, TokenData, fake_users_db



router = APIRouter()

# Dummy database to store tickets in memory
fake_db = {}

@router.post("/tickets/", response_model=TicketResponse)
def create_ticket(ticket: TicketCreate):
    ticket_id = uuid4()
    new_ticket = TicketModel(
        id=ticket_id,
        customer_id=ticket.customer_id,
        subject=ticket.subject,
        description=ticket.description
    )
    fake_db[str(ticket_id)] = new_ticket
    return new_ticket

@router.get("/tickets/{ticket_id}", response_model=TicketResponse)
def get_ticket(
    ticket_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    ticket = fake_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Access control logic
    if current_user.role == "customer" and str(ticket.customer_id) != current_user.username:
        raise HTTPException(status_code=403, detail="Customers can only view their own tickets")

    if current_user.role == "agent":
        # Look up agent's UUID from username
        agent = fake_users_db.get(current_user.username)
        if not agent or ticket.agent_id != agent["id"]:
            raise HTTPException(status_code=403, detail="Agents can only view tickets assigned to them")

    # Admins bypass checks
    return ticket

@router.get("/tickets/embed/{embed_token}")
def get_ticket_embed(embed_token: str):
    for ticket in fake_db.values():
        if ticket.embed_token == embed_token:
            return {
                "subject": ticket.subject,
                "status": ticket.status,
                "last_updated": ticket.last_updated,
                "link": f"/tickets/{ticket.id}"
            }
    raise HTTPException(status_code=404, detail="Ticket not found")


@router.get("/tickets/my", response_model=List[TicketResponse])
def get_my_tickets(current_user: TokenData = Depends(require_role("customer"))):
    results = [
        ticket for ticket in fake_db.values()
        if str(ticket.customer_id) == current_user.username
    ]
    return results
@router.get("/tickets/", response_model=List[TicketResponse])
def get_all_tickets(current_user: TokenData = Depends(get_current_user)):
    if current_user.role == "admin":
        # Admin sees all tickets
        return list(fake_db.values())
    elif current_user.role == "agent":
        agent = fake_users_db.get(current_user.username)
        if not agent:
            return []
        return [
            ticket for ticket in fake_db.values()
            if ticket.agent_id == agent["id"]
        ]
    else:
        raise HTTPException(status_code=403, detail="Access forbidden")

@router.patch("/tickets/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: str,
    status: str = Body(None),
    resolution_notes: str = Body(None),
    current_user: TokenData = Depends(require_role("agent"))
):
    ticket = fake_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    agent = fake_users_db.get(current_user.username)
    if not agent or ticket.agent_id != agent["id"]:
        raise HTTPException(status_code=403, detail="Agents can only update their assigned tickets")
    if status:
        ticket.status = status
    if resolution_notes:
        ticket.resolution_notes = resolution_notes
    fake_db[ticket_id] = ticket
    return ticket

@router.patch("/tickets/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: str,
    agent_id: str = Body(..., embed=True),
    current_user: TokenData = Depends(require_role("admin"))
):
    ticket = fake_db.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.agent_id = agent_id
    fake_db[ticket_id] = ticket
    return ticket







