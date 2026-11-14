
import uuid

from backend.schemas.job import JobStatus
from backend.services.job_service import (
    create_job,
    get_job,
    update_job_status
)


def test_create_job():
    prompt = "A futuristic sports car"

    job = create_job(prompt)

    assert job.job_id is not None
    assert job.prompt == prompt
    assert job.status == JobStatus.pending


def test_get_existing_job():
    job = create_job("A red sports car")

    retrieved_job = get_job(job.job_id)

    assert retrieved_job is not None
    assert retrieved_job.job_id == job.job_id
    assert retrieved_job.prompt == "A red sports car"


def test_get_invalid_job():
    job = get_job(str(uuid.uuid4()))

    assert job is None


def test_update_job_status():
    job = create_job("A futuristic robot")

    updated_job = update_job_status(
        job.job_id,
        JobStatus.processing
    )

    assert updated_job is not None
    assert updated_job.status == JobStatus.processing


def test_update_invalid_job():
    result = update_job_status(
        str(uuid.uuid4()),
        JobStatus.completed
    )

    assert result is None


def test_database_persistence():
    job = create_job("A flying futuristic car")

    job_id = job.job_id

    retrieved_job = get_job(job_id)

    assert retrieved_job is not None
    assert retrieved_job.job_id == job_id
    assert retrieved_job.prompt == "A flying futuristic car"
