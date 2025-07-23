
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_and_view_ticket():
    # Login as alice (customer)
    login = client.post(
        "/auth/token", data={"username": "alice", "password": "alice123"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create ticket
    res = client.post(
        "/tickets/", json={"subject": "Test Issue", "description": "Details"}, headers=headers)
    assert res.status_code == 200
    ticket_id = res.json()["id"]

    # View ticket
    res = client.get(f"/tickets/{ticket_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["subject"] == "Test Issue"
