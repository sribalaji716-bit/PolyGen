
from fastapi import APIRouter, HTTPException, BackgroundTasks

from backend.schemas.prompt import PromptRequest
from backend.schemas.job import GenerationJob, JobStatusUpdate
from backend.services.job_service import (
    create_job,
    get_job,
    update_job_status
)
from backend.services.generation_service import run_generation

router = APIRouter()


@router.post("/generate", response_model=GenerationJob)
def generate_asset(
    request: PromptRequest,
    background_tasks: BackgroundTasks
):
    job = create_job(request.prompt)

    background_tasks.add_task(
        run_generation,
        job.job_id
    )

    return job


@router.get("/status/{job_id}", response_model=GenerationJob)
def get_generation_status(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    return job


@router.patch("/status/{job_id}", response_model=GenerationJob)
def update_generation_status(job_id: str, request: JobStatusUpdate):
    job = update_job_status(job_id, request.status)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    return job
