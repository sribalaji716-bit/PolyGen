from pydantic import BaseModel
from enum import Enum


class JobStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"


class GenerationJob(BaseModel):
    job_id: str
    prompt: str
    status: JobStatus = JobStatus.pending


class JobStatusUpdate(BaseModel):
    status: JobStatus