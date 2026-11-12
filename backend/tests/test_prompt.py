from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Backend is running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_valid_prompt():
    response = client.post(
        "/api/prompt/generate",
        json={"prompt": "A futuristic sports car"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_short_prompt():
    response = client.post(
        "/api/prompt/generate",
        json={"prompt": "Car"}
    )

    assert response.status_code == 422


def test_empty_prompt():
    response = client.post(
        "/api/prompt/generate",
        json={"prompt": ""}
    )

    assert response.status_code == 422