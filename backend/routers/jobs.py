from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from jobs.queue import get_job, get_job_result
import asyncio
import json

router = APIRouter()

@router.get("/job/{job_id}")
async def job_status(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    return job

@router.websocket("/ws/job/{job_id}")
async def ws_job_status(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        while True:
            job = get_job(job_id)
            if not job:
                await websocket.send_json({"error": "Job not found"})
                break
            await websocket.send_json({
                "status": job["status"],
                "progress": job["progress"],
                "original_size": job.get("original_size", 0),
                "result_size": job.get("result_size", 0),
                "result_filename": job.get("result_filename"),
                "error": job.get("error"),
            })
            if job["status"] in ("done", "error"):
                break
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        pass
