
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

    data = response.json()

    assert data["status"] == "pending"
    assert data["prompt"] == "A futuristic sports car"
    assert "job_id" in data


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


def test_get_job_status():
    create_response = client.post(
        "/api/prompt/generate",
        json={"prompt": "A futuristic sports car"}
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["job_id"]

    status_response = client.get(
        f"/api/prompt/status/{job_id}"
    )

    assert status_response.status_code == 200
    assert status_response.json()["job_id"] == job_id
    assert status_response.json()["status"] == "pending"


def test_invalid_job_status():
    response = client.get(
        "/api/prompt/status/invalid-job-id"
    )

    assert response.status_code == 404


def test_update_job_status():
    create_response = client.post(
        "/api/prompt/generate",
        json={"prompt": "A futuristic robot"}
    )

    assert create_response.status_code == 200

    job_id = create_response.json()["job_id"]

    update_response = client.patch(
        f"/api/prompt/status/{job_id}",
        json={"status": "processing"}
    )

    assert update_response.status_code == 200
    assert update_response.json()["job_id"] == job_id
    assert update_response.json()["status"] == "processing"


def test_update_invalid_job():
    response = client.patch(
        "/api/prompt/status/invalid-job-id",
        json={"status": "completed"}
    )

    assert response.status_code == 404


def test_invalid_status_value():
    create_response = client.post(
        "/api/prompt/generate",
        json={"prompt": "A futuristic robot"}
    )

    job_id = create_response.json()["job_id"]

    response = client.patch(
        f"/api/prompt/status/{job_id}",
        json={"status": "unknown"}
    )

    assert response.status_code == 422
