from backend.schemas.job import GenerationJob, JobStatus
from backend.storage.database import get_connection


def create_job(prompt: str) -> GenerationJob:
    import uuid

    job_id = str(uuid.uuid4())

    job = GenerationJob(
        job_id=job_id,
        prompt=prompt,
        status=JobStatus.pending
    )

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO generation_jobs (job_id, prompt, status)
        VALUES (?, ?, ?)
        """,
        (job.job_id, job.prompt, job.status.value)
    )

    connection.commit()
    connection.close()

    return job


def get_job(job_id: str):
    connection = get_connection()

    row = connection.execute(
        """
        SELECT job_id, prompt, status
        FROM generation_jobs
        WHERE job_id = ?
        """,
        (job_id,)
    ).fetchone()

    connection.close()

    if not row:
        return None

    return GenerationJob(
        job_id=row["job_id"],
        prompt=row["prompt"],
        status=JobStatus(row["status"])
    )


def update_job_status(job_id: str, status: JobStatus):
    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE generation_jobs
        SET status = ?
        WHERE job_id = ?
        """,
        (status.value, job_id)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return None

    return get_job(job_id)