from sqlalchemy import Column, String, Enum, ForeignKey, DateTime
from sqlalchemy.dialects.sqlite import BLOB as UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4
from datetime import datetime
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    open = "Open"
    in_progress = "In Progress"
    resolved = "Resolved"
    closed = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    subject = Column(String, nullable=False)
    description = Column(String, nullable=True)
    customer_id = Column(String, nullable=False)
    agent_id = Column(String, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.open)
    resolution_notes = Column(String, nullable=True)
    last_updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    embed_token = Column(String, default=lambda: str(uuid4()), unique=True)
