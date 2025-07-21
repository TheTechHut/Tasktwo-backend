import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4
from app.constants.status import TicketStatus

KEN_ID = "11111111-1111-1111-1111-111111111111"
BARBIE_ID = "22222222-2222-2222-2222-222222222222"
ADMIN_ID = "33333333-3333-3333-3333-333333333333"

client = TestClient(app)

# Helper to get auth token for a user
def get_token(username):
    response = client.post("/login", data={"username": username, "password": ""})
    assert response.status_code == 200
    return response.json()["access_token"]

# --- Ticket Creation ---
def test_ticket_creation():
    customer_id = str(uuid4())
    token = get_token("ken")
    payload = {
        "customer_id": customer_id,
        "subject": "Test Subject",
        "description": "Test Description"
    }
    response = client.post("/tickets/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == customer_id
    assert data["subject"] == "Test Subject"
    assert data["status"] == TicketStatus.OPEN
    assert "embed_token" in data

# --- Role-specific Access Control ---
def test_customer_can_only_see_own_ticket():
    customer_id = str(uuid4())
    token = get_token("ken")
    payload = {
        "customer_id": customer_id,
        "subject": "Customer Ticket",
        "description": "Customer's issue"
    }
    ticket_resp = client.post("/tickets/", json=payload)
    ticket_id = ticket_resp.json()["id"]
    # Try to access as another customer
    token2 = get_token("barbie")
    resp = client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {token2}"})
    assert resp.status_code == 403 or resp.status_code == 404


def test_agent_can_only_see_assigned_ticket():
    # Create ticket as customer
    customer_id = str(uuid4())
    payload = {
        "customer_id": customer_id,
        "subject": "Agent Ticket",
        "description": "Agent's issue"
    }
    ticket_resp = client.post("/tickets/", json=payload)
    ticket_id = ticket_resp.json()["id"]
    # Assign to agent as admin
    admin_token = get_token("admin")
    agent_id = BARBIE_ID
    assign_resp = client.patch(
        f"/tickets/{ticket_id}/assign",
        json={"agent_id": agent_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert assign_resp.status_code == 200
    # Agent can access
    agent_token = get_token("barbie")
    resp = client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {agent_token}"})
    assert resp.status_code == 200
    # Another agent/customer cannot access
    other_token = get_token("ken")
    resp2 = client.get(f"/tickets/{ticket_id}", headers={"Authorization": f"Bearer {other_token}"})
    assert resp2.status_code == 403 or resp2.status_code == 404

# --- Admin Assignment Flow ---
def test_admin_can_assign_ticket():
    customer_id = str(uuid4())
    payload = {
        "customer_id": customer_id,
        "subject": "Assign Test",
        "description": "Assignment flow"
    }
    ticket_resp = client.post("/tickets/", json=payload)
    ticket_id = ticket_resp.json()["id"]
    admin_token = get_token("admin")
    agent_id = BARBIE_ID
    assign_resp = client.patch(
        f"/tickets/{ticket_id}/assign",
        json={"agent_id": agent_id},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert assign_resp.status_code == 200
    data = assign_resp.json()
    assert data["agent_id"] == agent_id

# --- Embed Token Access ---
def test_embed_token_access():
    customer_id = str(uuid4())
    payload = {
        "customer_id": customer_id,
        "subject": "Embed Test",
        "description": "Embed token access"
    }
    ticket_resp = client.post("/tickets/", json=payload)
    ticket = ticket_resp.json()
    embed_token = ticket["embed_token"]
    resp = client.get(f"/tickets/embed/{embed_token}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["subject"] == "Embed Test"
    assert data["status"] == TicketStatus.OPEN
    assert "link" in data



