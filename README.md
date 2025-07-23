# Ticket Management API

This FastAPI backend enables role-based ticket management with chatbot-friendly ticket summaries.

## Features
- JWT authentication with Customer, Agent, Admin roles
- Role-aware endpoints to submit, view, assign, and update tickets
- Secure `/embed/{token}` endpoint for read-only public access

## Roles & Permissions
- **Customer**: Submit/view own tickets
- **Agent**: View/update assigned tickets
- **Admin**: Full access, assign tickets

## Embed Endpoint Example
```json
{
  "subject": "Login error",
  "status": "Open",
  "last_updated": "2025-07-23T09:30:00Z",
  "link": "https://example.com/tickets/abc123"
}
```

## Setup
```bash
uvicorn main:app --reload
```

## Testing
```bash
pytest tests/
```