from enum import Enum, IntEnum
# Using IntEnum because it's easier to store in the database as integers,
class TicketStatus(IntEnum):
    """
    Enum for representing the status of a support ticket.

    The integer values are stored in the database for efficiency,
    but the strings can be used in logic and APIs.
    """

    OPEN = 1              # Ticket has been created but not yet worked on
    IN_PROGRESS = 2       # Ticket is currently being worked on
    RESOLVED = 3          # The issue has been resolved but not yet closed
    CLOSED = 4            # Ticket is fully closed

    def __str__(self):
        """
        Return a human-readable version of the enum name.
        """
        return self.name.replace("_", " ").title()