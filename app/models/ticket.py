from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum
from datetime import datetime
from app.database import Base

class TicketStatus(str, enum.Enum):
    open = "Open"
    in_progress = "In Progress"
    resolved = "Resolved"
    closed = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject = Column(String, nullable=False)
    description = Column(String, nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    agent_id = Column(UUID(as_uuid=True), nullable=True)
    status = Column(Enum(TicketStatus), default=TicketStatus.open)
    embed_token = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)