from fastapi import APIRouter, UploadFile, File, Form, Request, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Optional
from middleware.security import validate_upload
from middleware.rate_limiter import check_rate_limit
from jobs.queue import create_job
from jobs.processor import process_job
from config import get_settings

router = APIRouter()

@router.post("/upload")
async def upload_file(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    operation: str = Form("compress"),
    quality: Optional[int] = Form(75),
    target_format: Optional[str] = Form(None),
    scale: Optional[float] = Form(2.0),
    max_width: Optional[int] = Form(None),
    max_height: Optional[int] = Form(None),
    bitrate: str = Form("128k"),
):
    settings = get_settings()
    
    # Rate limit
    check_rate_limit(request, max_requests=settings.ANON_FILES_PER_HOUR)
    
    # Read file
    data = await file.read()
    
    # Security validation
    clean_name = validate_upload(data, file.filename or "upload")
    
    # Build options
    options = {
        "quality": quality,
        "target_format": target_format,
        "scale": scale,
        "max_width": max_width,
        "max_height": max_height,
        "bitrate": bitrate,
    }
    
    # Create job
    job_id = create_job(clean_name, operation, options)
    
    # Process in background thread
    background_tasks.add_task(process_job, job_id, data, clean_name, operation, options)
    
    return JSONResponse({
        "job_id": job_id,
        "filename": clean_name,
        "original_size": len(data),
        "status": "queued"
    })
