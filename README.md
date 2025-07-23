
# Ticket Management API

A secure, role-based support ticketing system built with **FastAPI**.  
Customers can submit issues, admins assign them to agents, and agents resolve them.  
Includes a public chatbot-friendly endpoint using a secure embed token.

---

# Features

- JWT-based authentication
- Role-based access control (Customer, Agent, Admin)
- RESTful API for ticket operations
- Secure embed endpoint for chatbot integration
- FastAPI OpenAPI docs
- Basic test coverage with `pytest`

---

# Project Structure

```
ticket_api/
├── app/
│   ├── main.py                # App entry point
│   ├── api/                   # Routers
│   │   ├── auth.py            # Login route
│   │   └── tickets.py         # Ticket operations
│   ├── models/                # ORM models
│   │   ├── user.py            # Mock user DB
│   │   └── ticket.py          # Ticket model
│   ├── schemas/               # Pydantic validation schemas
│   ├── database.py            # SQLAlchemy DB session
│   └── dependencies.py        # Shared auth/dependency logic
├── tests/
│   └── test_tickets.py        # Test cases
├── create_db.py               # One-time script to init the DB
├── requirements.txt
└── README.md
```

---

# Authentication & Roles

- Users log in via `/auth/token` using a username/password.
- A **JWT token** is returned and must be sent in the `Authorization` header.

# Roles:

| Role     | Permissions                                                  |
|----------|--------------------------------------------------------------|
| Customer | Submit ticket, view their own tickets                        |
| Agent    | View and update assigned tickets                             |
| Admin    | View all tickets, assign tickets to agents                   |

---

# API Endpoints Overview

# Auth
| Method | Path         | Description     |
|--------|--------------|-----------------|
| POST   | `/auth/token`| Login (JWT)     |

---

# Ticket Operations

| Method | Path                     | Role(s)         | Description                        |
|--------|--------------------------|-----------------|------------------------------------|
| POST   | `/tickets/`              | Customer        | Create a new ticket                |
| GET    | `/tickets/my`           | Customer        | View your submitted tickets        |
| GET    | `/tickets/{id}`         | All             | View a specific ticket (access-controlled) |
| GET    | `/tickets/`              | Agent, Admin    | View all or assigned tickets       |
| PATCH  | `/tickets/{id}`         | Agent           | Update ticket status               |
| PATCH  | `/tickets/{id}/assign`  | Admin           | Assign a ticket to an agent        |
| GET    | `/tickets/embed/{token}`| Public          | Chatbot-friendly view via token    |

---

# Example Usage

# Login
```
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=alice
password=alice123
```

# JWT Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Use the token:
```
Authorization: Bearer <access_token>
```

---
# Chatbot-Friendly Embed Response

```http
GET /tickets/embed/9f40cb91-...
```

# Example JSON:
```json
{
  "subject": "App Crash",
  "status": "In Progress",
  "last_updated": "2025-07-23T12:30:00",
  "link": "https://support.example.com/tickets/9f40cb91-..."
}
```

---

# Testing

Run all tests with:

```bash
pytest
```

Test cases include:
- Ticket creation
- Access control
- Embed token security

---

# Running the App

# 1. Install requirements:
```bash
pip install -r requirements.txt
```

# 2. Create the database:
```bash
python create_db.py
```

# 3. Run the server:
```bash
uvicorn app.main:app --reload
```

Access API docs at:
> 📘 http://localhost:8000/docs

---

# Security Notes

- All tokens use JWT with `HS256` algorithm.
- `embed_token` is a UUID, unguessable and unique.
- Passwords are hashed with `bcrypt` (via `passlib`).

---

# Fake Users (for testing)

| Username | Password   | Role     |
|----------|------------|----------|
| alice    | alice123   | Customer |
| bob      | bob123     | Agent    |
| carol    | carol123   | Admin    |

---
