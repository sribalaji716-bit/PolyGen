
import pytest

from fastapi.testclient import TestClient

from backend.main import app
from backend.api import prompt as prompt_api
from backend.schemas.job import GenerationJob, JobStatus


client = TestClient(app)


@pytest.fixture(autouse=True)
def disable_real_generation(monkeypatch):
    monkeypatch.setattr(
        prompt_api,
        "run_generation",
        lambda job_id: None
    )


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


def test_download_completed_glb(monkeypatch, tmp_path):
    output_dir = tmp_path / "storage" / "generated"
    output_dir.mkdir(parents=True)

    glb_file = output_dir / "test_model.glb"
    glb_file.write_bytes(b"fake-glb-content")

    fake_api_file = tmp_path / "api" / "prompt.py"

    monkeypatch.setattr(
        prompt_api,
        "__file__",
        str(fake_api_file)
    )

    job = GenerationJob(
        job_id="test-job-123",
        prompt="A futuristic robot",
        status=JobStatus.completed,
        asset_path=str(glb_file)
    )

    monkeypatch.setattr(
        prompt_api,
        "get_job",
        lambda job_id: job if job_id == job.job_id else None
    )

    response = client.get(
        "/api/prompt/download/test-job-123"
    )

    assert response.status_code == 200
    assert response.content == b"fake-glb-content"
    assert response.headers["content-type"] == "model/gltf-binary"


def test_download_invalid_job():
    response = client.get(
        "/api/prompt/download/invalid-job-id"
    )

    assert response.status_code == 404


def test_download_pending_job(monkeypatch):
    job = GenerationJob(
        job_id="pending-job",
        prompt="A futuristic car",
        status=JobStatus.pending
    )

    monkeypatch.setattr(
        prompt_api,
        "get_job",
        lambda job_id: job if job_id == job.job_id else None
    )

    response = client.get(
        "/api/prompt/download/pending-job"
    )

    assert response.status_code == 400


def test_download_missing_glb(monkeypatch, tmp_path):
    output_dir = tmp_path / "storage" / "generated"
    output_dir.mkdir(parents=True)

    fake_api_file = tmp_path / "api" / "prompt.py"

    monkeypatch.setattr(
        prompt_api,
        "__file__",
        str(fake_api_file)
    )

    missing_file = output_dir / "missing.glb"

    job = GenerationJob(
        job_id="missing-job",
        prompt="A futuristic car",
        status=JobStatus.completed,
        asset_path=str(missing_file)
    )

    monkeypatch.setattr(
        prompt_api,
        "get_job",
        lambda job_id: job if job_id == job.job_id else None
    )

    response = client.get(
        "/api/prompt/download/missing-job"
    )

    assert response.status_code == 404
