
import uuid

from backend.schemas.job import JobStatus
from backend.services.job_service import (
    create_job,
    get_job,
    list_jobs,
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


def test_list_jobs():
    job1 = create_job("A futuristic airplane")
    job2 = create_job("A 3D gaming character")

    jobs = list_jobs()

    job_ids = [job.job_id for job in jobs]

    assert job1.job_id in job_ids
    assert job2.job_id in job_ids


def test_list_jobs_latest_first():
    create_job("First 3D object")
    latest_job = create_job("Latest 3D object")

    jobs = list_jobs(limit=1)

    assert len(jobs) == 1
    assert jobs[0].job_id == latest_job.job_id


def test_list_jobs_pagination():
    create_job("3D object one")
    create_job("3D object two")
    create_job("3D object three")

    first_page = list_jobs(limit=2, offset=0)
    second_page = list_jobs(limit=2, offset=2)

    assert len(first_page) == 2
    assert len(second_page) == 2

    first_page_ids = {job.job_id for job in first_page}
    second_page_ids = {job.job_id for job in second_page}

    assert first_page_ids.isdisjoint(second_page_ids)
