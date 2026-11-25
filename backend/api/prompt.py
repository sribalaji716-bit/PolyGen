
from pathlib import Path

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse

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
def update_generation_status(
    job_id: str,
    request: JobStatusUpdate
):
    job = update_job_status(
        job_id,
        request.status
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    return job


@router.get("/download/{job_id}")
def download_generated_asset(job_id: str):

    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Generation job not found"
        )

    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="3D generation is not completed yet"
        )

    if not job.asset_path:
        raise HTTPException(
            status_code=404,
            detail="Generated asset path not found"
        )

    output_dir = (
        Path(__file__).resolve().parents[1]
        / "storage"
        / "generated"
    ).resolve()

    asset_path = Path(job.asset_path).resolve()

    if (
        asset_path.suffix.lower() != ".glb"
        or not asset_path.is_relative_to(output_dir)
        or not asset_path.is_file()
    ):
        raise HTTPException(
            status_code=404,
            detail="Valid GLB asset not found"
        )

    return FileResponse(
        path=asset_path,
        media_type="model/gltf-binary",
        filename=f"polygen_{job_id}.glb"
    )
