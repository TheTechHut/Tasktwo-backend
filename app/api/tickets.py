from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import ticket as schemas
from app.models import ticket as models
from app.database import SessionLocal
from app.core.auth import get_current_user, role_required, TokenData
import uuid

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.TicketOut)
def create_ticket(ticket: schemas.TicketCreate, user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    new_ticket = models.Ticket(subject=ticket.subject, description=ticket.description, customer_id=user.user_id)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

@router.get("/my", response_model=list[schemas.TicketOut])
def get_my_tickets(user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Ticket).filter(models.Ticket.customer_id == user.user_id).all()

@router.get("/", response_model=list[schemas.TicketOut])
def get_all_tickets(user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role not in ["agent", "admin"]:
        raise HTTPException(403, "Forbidden")
    return db.query(models.Ticket).all()

@router.get("/{id}", response_model=schemas.TicketOut)
def get_ticket(id: str, user: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).get(id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    if user.role == "customer" and ticket.customer_id != user.user_id:
        raise HTTPException(403, "Forbidden")
    if user.role == "agent" and ticket.agent_id != user.user_id:
        raise HTTPException(403, "Forbidden")
    return ticket

@router.patch("/{id}", response_model=schemas.TicketOut)
def update_ticket(id: str, update: schemas.TicketUpdate, user: TokenData = Depends(role_required("agent")), db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).get(id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    if ticket.agent_id != user.user_id:
        raise HTTPException(403, "Forbidden")
    for field, value in update.dict(exclude_unset=True).items():
        setattr(ticket, field, value)
    db.commit()
    return ticket

@router.patch("/{id}/assign", response_model=schemas.TicketOut)
def assign_ticket(id: str, assign: schemas.TicketAssign, user: TokenData = Depends(role_required("admin")), db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).get(id)
    if not ticket:
        raise HTTPException(404, "Ticket not found")
    ticket.agent_id = assign.agent_id
    db.commit()
    return ticket

@router.get("/embed/{embed_token}", response_model=schemas.TicketEmbed)
def get_ticket_embed(embed_token: str, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.embed_token == embed_token).first()
    if not ticket:
        raise HTTPException(404, "Invalid token")
    return schemas.TicketEmbed(
        subject=ticket.subject,
        status=ticket.status,
        last_updated=ticket.last_updated,
        link=f"https://example.com/tickets/{ticket.id}"
    )