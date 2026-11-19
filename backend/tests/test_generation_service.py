
from pathlib import Path
from unittest.mock import Mock

from backend.schemas.job import JobStatus
from backend.services.job_service import create_job, get_job
from backend.services.generation_service import run_generation


def test_generation_success():

    job = create_job("A futuristic sports car")

    fake_generator = Mock()
    fake_generator.generate.return_value = Path("generated/car.glb")

    run_generation(job.job_id, fake_generator)

    updated_job = get_job(job.job_id)

    assert updated_job.status == JobStatus.completed
    assert updated_job.asset_path == "generated/car.glb"


def test_generation_failure():

    job = create_job("A futuristic sports car")

    fake_generator = Mock()
    fake_generator.generate.side_effect = RuntimeError(
        "Mock generation failure"
    )

    run_generation(job.job_id, fake_generator)

    updated_job = get_job(job.job_id)

    assert updated_job.status == JobStatus.failed
    assert updated_job.asset_path is None


def test_invalid_job_id():

    fake_generator = Mock()

    run_generation("invalid-job-id", fake_generator)

    fake_generator.generate.assert_not_called()
