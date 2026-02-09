import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

def test_signup_and_unregister():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "pytestuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code in (200, 400)  # 400 if already signed up
    # Duplicate signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    # Unregister
    response3 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response3.status_code == 200
    # Unregister again should fail
    response4 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response4.status_code == 400
