from pydantic import BaseModel
from sqlalchemy import  Enum as SQLEnum
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, BigInteger, CheckConstraint
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID # SQLAlchemy base for model definitions
from sqlalchemy.orm import relationship
from Ticketing_System.database import Base
from datetime import datetime
import uuid
import sqlalchemy.types as types
from sqlalchemy.types import UUID
from Ticketing_System.enums import TicketStatus

# UUID field that works across dialects
class GUID(types.TypeDecorator):
    impl = String  # Base type used for SQLite
    cache_ok = True

    # Use native PostgreSQL UUID if available, otherwise fallback to string
    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    # Convert UUID to string for SQLite, pass through for PostgreSQL
    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        if dialect.name == "postgresql":
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        return uuid.UUID(value) if value else None

# --------------------------
# User Model
# --------------------------
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, ForeignKey("roles.role_id"))

    # Ensure email format contains '@' and a domain using SQL check
    __table_args__ = (
        CheckConstraint("email LIKE '%@%.__%'", name="email_format_check"),  # SQLite version of email check
    )

    role_rel = relationship("Role", back_populates="users")
    tickets = relationship("Ticket", back_populates="creator")
    status_changes = relationship("TicketStatusHistory", back_populates="user")

# --------------------------
# Role Model
# --------------------------
class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True)
    role = Column(String, nullable=False)

    users = relationship("User", back_populates="role_rel")

# --------------------------
# Priority Model
# --------------------------
class Priority(Base):
    __tablename__ = "priorities"

    priority_id = Column(Integer, primary_key=True)
    priority = Column(String)
    color = Column(BigInteger)  # UI element for coloring priority levels

    tickets = relationship("Ticket", back_populates="priority_rel")  # Priority → Associated tickets

# --------------------------
# Ticket Model
# --------------------------
class Ticket(Base):
    __tablename__ = "ticket"

    ticket_id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    subject = Column(String)
    description = Column(Text)
    status = Column(SQLEnum(TicketStatus), default=TicketStatus.OPEN, nullable=False)
    priority = Column(Integer, ForeignKey("priorities.priority_id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #create an embeded_token
    embed_token = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    # relationships
    creator = relationship("User", back_populates="tickets")
    priority_rel = relationship("Priority", back_populates="tickets")
    status_history = relationship("TicketStatusHistory", back_populates="ticket")


# --------------------------
# TicketStatus History Model
# --------------------------

class TicketStatusHistory(Base):
    __tablename__ = "ticketstatushistory"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(GUID(), ForeignKey("ticket.ticket_id"))
    status = Column(Integer)
    changed_by = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=False)
    colour = Column(BigInteger)
    #Relationships
    ticket = relationship("Ticket", back_populates="status_history")
    user = relationship("User", back_populates="status_changes")











