from fastapi.testclient import TestClient
from main import app
import uuid

client = TestClient(app)

# Simulated test user (matches your get_current_user)
test_user = {
    "user_id": 1,
    "role": "customer"
}

def test_create_ticket():
    response = client.post(
        "/tickets/",
        json={
            "subject": "Login Issue",
            "description": "I can't access my account",
            "priority": 2
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "ticket_id" in data
    assert data["subject"] == "Login Issue"

def test_get_my_tickets():
    response = client.get("/tickets/my")
    assert response.status_code == 200
    assert isinstance(response.json(), list)