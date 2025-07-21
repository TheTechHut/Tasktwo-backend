from enum import Enum


class TicketStatus(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"



# Here we define a ticket status options using an Enum

# This allows us to have a fixed set of statuses that a ticket can have.

# enums are useful for defining a set of named values that can be used throughout the application.