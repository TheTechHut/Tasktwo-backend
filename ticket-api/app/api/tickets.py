from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import uuid4
from typing import List

from app.schemas.ticket import *
from app.models.ticket import Ticket, StatusEnum
from app.db.session import get_db
from app.core.auth import get_current_user, require_role

router = APIRouter(tags=["Tickets"])

# --- 1. CREATE TICKET (CUSTOMER) ---
@router.post("/tickets/", response_model=TicketOut, summary="Create a new ticket")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can create tickets")

    new_ticket = Ticket(
        subject=ticket.subject,
        description=ticket.description,
        customer_id=user["id"]
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

# --- 2. GET MY TICKETS (CUSTOMER) ---
@router.get("/tickets/my", response_model=List[TicketOut], summary="Get customer's tickets")
def get_my_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "customer":
        raise HTTPException(status_code=403, detail="Only customers can view their tickets")
    return db.query(Ticket).filter(Ticket.customer_id == user["id"]).all()

# --- 3. GET ALL TICKETS (AGENT & ADMIN) ---
@router.get("/tickets/", response_model=List[TicketOut], summary="Get all tickets (filtered)")
def get_all_tickets(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] not in ["agent", "admin"]:
        raise HTTPException(status_code=403, detail="Only agents or admins can view all tickets")
    if user["role"] == "agent":
        return db.query(Ticket).filter(Ticket.agent_id == user["id"]).all()
    return db.query(Ticket).all()

# --- 4. GET TICKET BY ID (ALL ROLES, ROLE-BASED ACCESS) ---
@router.get("/tickets/{id}", response_model=TicketOut, summary="Get specific ticket by ID")
def get_ticket_by_id(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if user["role"] == "customer" and ticket.customer_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not your ticket")
    if user["role"] == "agent" and ticket.agent_id != user["id"]:
        raise HTTPException(status_code=403, detail="Not assigned to you")

    return ticket

# --- 5. UPDATE TICKET STATUS/NOTES (AGENT) ---
@router.patch("/tickets/{id}", response_model=TicketOut, summary="Update ticket status or notes")
def update_ticket(id: str, update: TicketUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if user["role"] != "agent":
        raise HTTPException(status_code=403, detail="Only agents can update tickets")

    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.agent_id != user["id"]:
        raise HTTPException(status_code=403, detail="You are not assigned to this ticket")

    if update.status:
        ticket.status = update.status
    if update.resolution_notes:
        ticket.resolution_notes = update.resolution_notes

    db.commit()
    db.refresh(ticket)
    return ticket

# --- 6. ASSIGN TICKET TO AGENT (ADMIN) ---
@router.patch("/tickets/{id}/assign", response_model=TicketOut, summary="Assign ticket to agent")
def assign_ticket(id: str, data: TicketAssign, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    ticket = db.query(Ticket).filter(Ticket.id == id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.agent_id = data.agent_id
    ticket.status = StatusEnum.in_progress
    db.commit()
    db.refresh(ticket)
    return ticket

# --- 7. EMBED TOKEN ENDPOINT (PUBLIC) ---
@router.get("/tickets/embed/{embed_token}", response_model=TicketEmbedOut, summary="Chatbot embed view")
def get_embed(embed_token: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.embed_token == embed_token).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return TicketEmbedOut(
        subject=ticket.subject,
        status=ticket.status,
        last_updated=ticket.last_updated,
        link=f"https://support.example.com/tickets/{ticket.id}"
    )
