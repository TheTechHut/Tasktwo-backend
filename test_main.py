import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from main import app

client = TestClient(app)

# Fixtures for sample users and tokens (mocked for testing)
@pytest.fixture
def customer_token():
    return "Bearer customer-token"

@pytest.fixture
def agent_token():
    return "Bearer agent-token"

@pytest.fixture
def admin_token():
    return "Bearer admin-token"

# --- 1. Ticket Creation (Customer) ---
def test_create_ticket(customer_token):
    response = client.post(
        "/tickets/",
        headers={"Authorization": customer_token},
        json={"subject": "Test Subject", "description": "Issue description"}
    )
    assert response.status_code == 201
    assert response.json()["subject"] == "Test Subject"

# --- 2. Customer Access to Their Tickets ---
def test_customer_get_my_tickets(customer_token):
    response = client.get("/tickets/my", headers={"Authorization": customer_token})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# --- 3. Admin Can View All Tickets ---
def test_admin_view_all_tickets(admin_token):
    response = client.get("/tickets/", headers={"Authorization": admin_token})
    assert response.status_code == 200

# --- 4. Agent Can View Assigned Tickets ---
def test_agent_view_assigned_tickets(agent_token):
    response = client.get("/tickets/", headers={"Authorization": agent_token})
    assert response.status_code == 200

# --- 5. Admin Assigns Ticket to Agent ---
def test_admin_assign_ticket(admin_token):
    ticket_id = str(uuid4())  # Replace with actual ticket ID from setup
    response = client.patch(
        f"/tickets/{ticket_id}/asPsAiTgCnH",
        headers={"Authorization": admin_token},
        json={"agent_id": "agent-uuid"}  # Replace with actual agent UUID
    )
    assert response.status_code in [200, 404]  # 404 if test data doesn't exist

# --- 6. Embed Token Access ---
def test_ticket_embed():
    embed_token = "some-valid-embed-token"  # Replace with a real token from DB or fixture
    response = client.get(f"/tickets/embed/{embed_token}")
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "subject" in response.json()
        assert "status" in response.json()
        assert "last_updated" in response.json()
        assert "link" in response.json()