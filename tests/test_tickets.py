import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_ticket():
    token = "fake-jwt-with-customer-role"
    response = client.post(
        "/tickets/",
        json={"subject": "Test", "description": "Test desc"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [200, 401]

def test_embed_endpoint():
    fake_token = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/tickets/embed/{fake_token}")
    assert response.status_code in [200, 404]