import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.auth import create_token

client = TestClient(app)

# Helper to create token for a role
def get_auth_headers(username):
    token = create_token(username)
    return {"Authorization": f"Bearer {token}"}

# 1. Test ticket creation by customer
def test_customer_can_create_ticket():
    headers = get_auth_headers("customer1")
    response = client.post("/api/tickets/", json={
        "subject": "Login issue",
        "description": "Login fails with error."
    }, headers=headers)
    assert response.status_code == 200
    assert response.json()["subject"] == "Login issue"

# 2. Test only admin can assign ticket
def test_only_admin_can_assign():
    # Create ticket as customer
    headers = get_auth_headers("customer1")
    ticket = client.post("/api/tickets/", json={
        "subject": "Assign test",
        "description": "Please assign"
    }, headers=headers).json()

    # Try assigning as agent (should fail)
    agent_headers = get_auth_headers("agent1")
    response = client.patch(f"/api/tickets/{ticket['id']}/assign", json={
        "agent_id": "user-agent"
    }, headers=agent_headers)
    assert response.status_code == 403

    # Assign as admin (should work)
    admin_headers = get_auth_headers("admin1")
    response = client.patch(f"/api/tickets/{ticket['id']}/assign", json={
        "agent_id": "user-agent"
    }, headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["agent_id"] == "user-agent"

# 3. Test agent can update status
def test_agent_can_update_ticket():
    # Customer creates a ticket
    customer_headers = get_auth_headers("customer1")
    ticket = client.post("/api/tickets/", json={
        "subject": "Update test",
        "description": "Agent should update this."
    }, headers=customer_headers).json()

    # Admin assigns it to agent
    admin_headers = get_auth_headers("admin1")
    client.patch(f"/api/tickets/{ticket['id']}/assign", json={
        "agent_id": "user-agent"
    }, headers=admin_headers)

    # Agent updates status
    agent_headers = get_auth_headers("agent1")
    response = client.patch(f"/api/tickets/{ticket['id']}", json={
        "status": "Resolved",
        "resolution_notes": "Issue fixed"
    }, headers=agent_headers)
    assert response.status_code == 200
    assert response.json()["status"] == "Resolved"

# 4. Test embed token works
def test_embed_token_view():
    headers = get_auth_headers("customer1")
    ticket = client.post("/api/tickets/", json={
        "subject": "Embed test",
        "description": "Bot should see this."
    }, headers=headers).json()

    token = ticket["embed_token"]
    response = client.get(f"/api/tickets/embed/{token}")
    assert response.status_code == 200
    assert response.json()["subject"] == "Embed test"
