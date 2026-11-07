"""Compression router."""

from typing import Optional
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from utils.file_detector import detect_type
from processors import image as img_proc
from processors import audio as aud_proc
from processors import pdf as pdf_proc
from processors import archive as arc_proc

router = APIRouter()

CONTENT_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg",
    "png": "image/png", "webp": "image/webp",
    "gif": "image/gif", "bmp": "image/bmp",
    "tiff": "image/tiff", "avif": "image/avif",
    "mp3": "audio/mpeg", "wav": "audio/wav",
    "flac": "audio/flac", "ogg": "audio/ogg",
    "aac": "audio/aac", "m4a": "audio/mp4",
    "pdf": "application/pdf",
    "zip": "application/zip",
}


def _ext(filename: str) -> str:
    return filename.lower().rsplit(".", 1)[-1] if "." in filename else ""


@router.post("/compress")
async def compress(
    file: UploadFile = File(...),
    quality: int = Form(75),
    max_width: Optional[int] = Form(None),
    max_height: Optional[int] = Form(None),
    bitrate: str = Form("128k"),
):
    data = await file.read()
    original_size = len(data)
    filename = file.filename or "file"
    file_type = detect_type(filename)
    ext = _ext(filename)

    try:
        if file_type == "image":
            compressed, out_ext = img_proc.compress_image(
                data, filename, quality=quality,
                max_width=max_width, max_height=max_height,
            )
        elif file_type == "audio":
            compressed = aud_proc.compress_audio(data, ext, bitrate=bitrate)
            out_ext = ext
        elif file_type == "pdf":
            compressed = pdf_proc.compress_pdf(data, quality=quality)
            out_ext = "pdf"
        elif file_type == "archive":
            compressed = arc_proc.compress_to_zip(data, filename)
            out_ext = "zip"
        else:
            raise HTTPException(status_code=415, detail=f"Unsupported file type: {file_type}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    content_type = CONTENT_TYPES.get(out_ext, "application/octet-stream")
    out_filename = f"{filename.rsplit('.', 1)[0]}_compressed.{out_ext}"

    return Response(
        content=compressed,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{out_filename}"',
            "X-Original-Size": str(original_size),
            "X-Compressed-Size": str(len(compressed)),
        },
    )
