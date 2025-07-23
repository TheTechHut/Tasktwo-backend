from fastapi import FastAPI
from app.api import tickets

app = FastAPI(title="Ticket Management API")

app.include_router(tickets.router, prefix="/tickets", tags=["Tickets"])