"""Conversion router."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from utils.file_detector import detect_type
from processors import image as img_proc
from processors import audio as aud_proc

router = APIRouter()

CONTENT_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg",
    "png": "image/png", "webp": "image/webp",
    "gif": "image/gif", "bmp": "image/bmp",
    "tiff": "image/tiff", "avif": "image/avif",
    "mp3": "audio/mpeg", "wav": "audio/wav",
    "flac": "audio/flac", "ogg": "audio/ogg",
    "aac": "audio/aac", "m4a": "audio/mp4",
}


def _ext(filename: str) -> str:
    return filename.lower().rsplit(".", 1)[-1] if "." in filename else ""


@router.post("/convert")
async def convert(
    file: UploadFile = File(...),
    target_format: str = Form(...),
):
    data = await file.read()
    filename = file.filename or "file"
    file_type = detect_type(filename)
    source_ext = _ext(filename)
    target_ext = target_format.lower().lstrip(".")

    try:
        if file_type == "image":
            converted = img_proc.convert_image(data, source_ext, target_ext)
        elif file_type == "audio":
            converted = aud_proc.convert_audio(data, source_ext, target_ext)
        else:
            raise HTTPException(
                status_code=415,
                detail=f"Conversion not supported for file type: {file_type}",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    content_type = CONTENT_TYPES.get(target_ext, "application/octet-stream")
    base_name = filename.rsplit(".", 1)[0]
    out_filename = f"{base_name}.{target_ext}"

    return Response(
        content=converted,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{out_filename}"',
        },
    )
