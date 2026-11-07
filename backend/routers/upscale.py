"""Upscale router."""

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import Response

from utils.file_detector import detect_type
from processors import image as img_proc

router = APIRouter()

CONTENT_TYPES = {
    "jpg": "image/jpeg", "jpeg": "image/jpeg",
    "png": "image/png", "webp": "image/webp",
    "gif": "image/gif", "bmp": "image/bmp",
    "tiff": "image/tiff", "avif": "image/avif",
}


@router.post("/upscale")
async def upscale(
    file: UploadFile = File(...),
    scale: float = Form(2.0),
):
    data = await file.read()
    filename = file.filename or "file"
    file_type = detect_type(filename)

    if file_type != "image":
        raise HTTPException(status_code=415, detail="Upscaling is only supported for images.")

    try:
        upscaled, out_ext = img_proc.upscale_image(data, filename, scale=scale)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    content_type = CONTENT_TYPES.get(out_ext, "image/png")
    base_name = filename.rsplit(".", 1)[0]
    out_filename = f"{base_name}_upscaled_{scale}x.{out_ext}"

    return Response(
        content=upscaled,
        media_type=content_type,
        headers={
            "Content-Disposition": f'attachment; filename="{out_filename}"',
        },
    )
