
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.ticket import Ticket, StatusEnum
from app.schemas.ticket import TicketCreate, TicketResponse
from app.dependencies import get_db, get_current_user, require_role
from app.schemas.user import Role, User
from fastapi import Query
from app.schemas.ticket import TicketUpdate, TicketAssign
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/", response_model=TicketResponse)
def create_ticket(
    ticket_data: TicketCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([Role.CUSTOMER]))
):
    ticket = Ticket(
        subject=ticket_data.subject,
        description=ticket_data.description,
        customer_id=user.username,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/my", response_model=list[TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    user: User = Depends(require_role([Role.CUSTOMER]))
):
    tickets = db.query(Ticket).filter(
        Ticket.customer_id == user.username).all()
    return tickets


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket_by_id(
    ticket_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if user.role == Role.CUSTOMER and ticket.customer_id != user.username:
        raise HTTPException(status_code=403, detail="Access denied")

    return ticket


@router.get("/", response_model=list[TicketResponse])
def view_all_tickets(
    status: StatusEnum = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(require_role([Role.ADMIN, Role.AGENT]))
):
    query = db.query(Ticket)
    if user.role == Role.AGENT:
        query = query.filter(Ticket.agent_id == user.username)
    if status:
        query = query.filter(Ticket.status == status)
    return query.all()


@router.patch("/{ticket_id}", response_model=TicketResponse)
def update_ticket(
    ticket_id: str,
    update_data: TicketUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([Role.AGENT]))
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.agent_id != user.username:
        raise HTTPException(
            status_code=403, detail="Ticket not assigned to you")
    if update_data.status:
        ticket.status = update_data.status
    db.commit()
    db.refresh(ticket)
    return ticket


@router.patch("/{ticket_id}/assign", response_model=TicketResponse)
def assign_ticket(
    ticket_id: str,
    assign_data: TicketAssign,
    db: Session = Depends(get_db),
    user: User = Depends(require_role([Role.ADMIN]))
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket.agent_id = assign_data.agent_id
    ticket.status = StatusEnum.IN_PROGRESS
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get("/embed/{embed_token}")
def get_embed_ticket(embed_token: str, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.embed_token == embed_token).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Invalid token")

    return JSONResponse(
        content={
            "subject": ticket.subject,
            "status": ticket.status,
            "last_updated": str(ticket.updated_at or ticket.created_at),
            "link": f"https://support.example.com/tickets/{ticket.id}"
        }
    )
