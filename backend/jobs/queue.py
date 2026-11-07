import uuid
import time
import json
import io
import os
import tempfile
from typing import Optional

# In-memory job store (replace with Redis in production)
_jobs: dict = {}

class JobStatus:
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    ERROR = "error"

def create_job(filename: str, operation: str, options: dict) -> str:
    job_id = str(uuid.uuid4())
    _jobs[job_id] = {
        "id": job_id,
        "filename": filename,
        "operation": operation,
        "options": options,
        "status": JobStatus.QUEUED,
        "progress": 0,
        "created_at": time.time(),
        "result": None,          # bytes
        "result_filename": None,
        "original_size": 0,
        "result_size": 0,
        "error": None,
    }
    return job_id

def get_job(job_id: str) -> Optional[dict]:
    job = _jobs.get(job_id)
    if job is None:
        return None
    # Return without raw bytes (for status endpoint)
    return {k: v for k, v in job.items() if k != "result"}

def update_job(job_id: str, **kwargs):
    if job_id in _jobs:
        _jobs[job_id].update(kwargs)

def get_job_result(job_id: str) -> Optional[tuple[bytes, str]]:
    job = _jobs.get(job_id)
    if not job or job["result"] is None:
        return None
    return job["result"], job["result_filename"]

def cleanup_old_jobs(ttl: int = 3600):
    now = time.time()
    to_delete = [jid for jid, j in _jobs.items() if now - j["created_at"] > ttl]
    for jid in to_delete:
        del _jobs[jid]
