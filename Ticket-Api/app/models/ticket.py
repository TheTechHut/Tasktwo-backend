from uuid import uuid4
from datetime import datetime

from app.constants.status import TicketStatus

# Create a Ticket "model"

# This is a simple class to represent a ticket in our system.

# It holds all the necessary information about a ticket.

# I Think of it like a form that captures everything we need to know about a support ticket.

# This is a blueprint for creating ticket objects.

class TicketModel:
    def __init__(self, id, customer_id, subject, description):
        self.id = id  # unique ticket ID
        self.customer_id = customer_id  # the customer who submitted it
        self.agent_id = None  # initially no agent is assigned
        self.subject = subject  # short title of the issue
        self.description = description  # full issue details
        self.status = TicketStatus.OPEN  # default status is "Open"
        self.resolution_notes = ""  # notes added by agent when resolving
        self.embed_token = str(uuid4())  # secure token for sharing with chatbot
        self.last_updated = datetime.utcnow()  # time the ticket was last touched
