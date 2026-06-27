from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_plan_rejects_empty_intent() -> None:
    response = client.post("/api/plan", json={"user_intent": "", "budget": 30})
    assert response.status_code == 422


def test_plan_rejects_invalid_budget() -> None:
    response = client.post("/api/plan", json={"user_intent": "dinner", "budget": -5})
    assert response.status_code == 422
