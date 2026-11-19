
import logging
from pathlib import Path

from backend.generation.huggingface_generator import HuggingFaceGenerator
from backend.schemas.job import JobStatus
from backend.services.job_service import (
    get_job,
    update_job_status
)

logger = logging.getLogger(__name__)

OUTPUT_DIR = (
    Path(__file__).resolve().parents[1]
    / "storage"
    / "generated"
)


def run_generation(job_id: str, generator=None):
    job = get_job(job_id)

    if job is None:
        logger.error("Generation job not found: %s", job_id)
        return

    try:
        update_job_status(job_id, JobStatus.processing)

        if generator is None:
            generator = HuggingFaceGenerator()

        asset_path = generator.generate(job.prompt, OUTPUT_DIR)

        update_job_status(
            job_id,
            JobStatus.completed,
            Path(asset_path).as_posix()
        )

        logger.info("Generation completed: %s", job_id)

    except Exception:
        logger.exception("Generation failed: %s", job_id)
        update_job_status(job_id, JobStatus.failed)
