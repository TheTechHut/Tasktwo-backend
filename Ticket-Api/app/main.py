from fastapi import FastAPI
from app.api import tickets, auth

app = FastAPI(
    title="Ticket Management API",
    description="A backend system for managing support tickets",
    version="1.0.0"
)

# Register the ticket routes under the main app
app.include_router(tickets.router, tags=["Tickets"])
app.include_router(auth.router, tags=["Auth"]) # Authentication routes