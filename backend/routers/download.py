from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from jobs.queue import get_job_result, get_job
import mimetypes

router = APIRouter()

CONTENT_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png",
    "webp": "image/webp", "gif": "image/gif", "bmp": "image/bmp",
    "tiff": "image/tiff", "avif": "image/avif", "ico": "image/x-icon",
    "svg": "image/svg+xml", "pdf": "application/pdf",
    "mp3": "audio/mpeg", "wav": "audio/wav", "flac": "audio/flac",
    "ogg": "audio/ogg", "aac": "audio/aac", "opus": "audio/opus",
    "mp4": "video/mp4", "webm": "video/webm", "avi": "video/x-msvideo",
    "mkv": "video/x-matroska", "zip": "application/zip",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "txt": "text/plain", "csv": "text/csv", "json": "application/json",
    "xml": "application/xml", "html": "text/html",
}

@router.get("/download/{job_id}")
async def download_result(job_id: str):
    job = get_job(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    if job["status"] != "done":
        raise HTTPException(400, f"Job is not done yet (status: {job['status']})")
    
    result = get_job_result(job_id)
    if not result:
        raise HTTPException(404, "Result not available")
    
    data, filename = result
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
    content_type = CONTENT_TYPES.get(ext, "application/octet-stream")
    
    return Response(
        content=data,
        media_type=content_type,
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


@router.post("/download-bundle")
async def download_bundle(payload: dict):
    """
    Accepts {"job_ids": ["id1", "id2", ...]}
    Creates a ZIP archive containing all finished files and returns it.
    """
    job_ids = payload.get("job_ids", [])
    if not job_ids:
        raise HTTPException(400, "No job_ids provided")

    import io
    import zipfile

    zip_buf = io.BytesIO()
    count = 0
    with zipfile.ZipFile(zip_buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for jid in job_ids:
            job = get_job(jid)
            if job and job.get("status") == "done":
                res = get_job_result(jid)
                if res:
                    file_bytes, file_name = res
                    # Prevent duplicate names in zip
                    arcname = file_name
                    zf.writestr(arcname, file_bytes)
                    count += 1

    if count == 0:
        raise HTTPException(404, "No completed files found for provided job IDs")

    return Response(
        content=zip_buf.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": 'attachment; filename="fileforge_bundle.zip"'}
    )
