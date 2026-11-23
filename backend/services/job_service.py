
from uuid import uuid4

from backend.schemas.job import GenerationJob, JobStatus
from backend.storage.database import get_connection


def create_job(prompt: str) -> GenerationJob:
    job = GenerationJob(
        job_id=str(uuid4()),
        prompt=prompt,
        status=JobStatus.pending
    )

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO generation_jobs (job_id, prompt, status, asset_path)
            VALUES (?, ?, ?, ?)
            """,
            (
                job.job_id,
                job.prompt,
                job.status.value,
                None
            )
        )

        connection.commit()

    finally:
        connection.close()

    return job


def get_job(job_id: str):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT job_id, prompt, status, asset_path
            FROM generation_jobs
            WHERE job_id = ?
            """,
            (job_id,)
        ).fetchone()

    finally:
        connection.close()

    if not row:
        return None

    return GenerationJob(
        job_id=row["job_id"],
        prompt=row["prompt"],
        status=JobStatus(row["status"]),
        asset_path=row["asset_path"]
    )


def list_jobs(limit: int = 10, offset: int = 0):
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT job_id, prompt, status, asset_path
            FROM generation_jobs
            ORDER BY rowid DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset)
        ).fetchall()

    finally:
        connection.close()

    return [
        GenerationJob(
            job_id=row["job_id"],
            prompt=row["prompt"],
            status=JobStatus(row["status"]),
            asset_path=row["asset_path"]
        )
        for row in rows
    ]


def update_job_status(
    job_id: str,
    status: JobStatus,
    asset_path: str | None = None
):
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE generation_jobs
            SET status = ?, asset_path = ?
            WHERE job_id = ?
            """,
            (status.value, asset_path, job_id)
        )

        connection.commit()

    finally:
        connection.close()

    if cursor.rowcount == 0:
        return None

    return get_job(job_id)
