"""
Synchronous job processor. Runs in a background thread via FastAPI's threadpool.
"""
import io
import os
from jobs.queue import update_job, JobStatus
from utils.file_detector import detect_type
from processors import image, audio, pdf, archive, document, video

def process_job(job_id: str, data: bytes, filename: str, operation: str, options: dict):
    update_job(job_id, status=JobStatus.PROCESSING, progress=10)
    try:
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        file_type = detect_type(filename)
        result_bytes = None
        result_ext = ext

        if operation == "compress":
            if file_type == "image":
                quality = int(options.get("quality", 75))
                max_w = options.get("max_width")
                max_h = options.get("max_height")
                result_bytes, result_ext = image.compress_image(
                    data, filename, quality=quality,
                    max_width=int(max_w) if max_w else None,
                    max_height=int(max_h) if max_h else None
                )
            elif file_type == "audio":
                result_bytes = audio.compress_audio(data, ext, options.get("bitrate", "128k"))
            elif file_type == "video":
                crf = int(options.get("crf", 28))
                result_bytes = video.compress_video(data, ext, crf=crf)
                result_ext = "mp4"
            elif file_type == "pdf":
                result_bytes = pdf.compress_pdf(data)
            elif file_type in ("document", "code"):
                result_bytes = document.compress_document(data, ext)
            elif file_type == "archive":
                result_bytes = archive.compress_to_zip(data, filename)
            else:
                result_bytes = data  # pass through unsupported types

        elif operation == "convert":
            target = options.get("target_format", ext).lower()
            if file_type == "image":
                result_bytes = image.convert_image(data, ext, target)
                result_ext = target
            elif file_type == "audio":
                result_bytes = audio.convert_audio(data, ext, target)
                result_ext = target
            elif file_type == "video":
                result_bytes = video.convert_video(data, ext, target)
                result_ext = target
            elif file_type == "pdf" and target in ("jpg", "png"):
                images = pdf.pdf_to_images(data, fmt=target)
                result_bytes = images[0] if images else data
                result_ext = target
            elif file_type in ("document", "code"):
                result_bytes = document.convert_document(data, ext, target)
                result_ext = target
            elif file_type == "archive":
                result_bytes = archive.convert_archive(data, ext, target, filename)
                result_ext = target
            else:
                result_bytes = data

        elif operation == "upscale":
            if file_type == "image":
                scale = float(options.get("scale", 2.0))
                result_bytes, result_ext = image.upscale_image(data, filename, scale=scale)
            else:
                result_bytes = data

        update_job(job_id, progress=90)

        base = filename.rsplit('.', 1)[0] if '.' in filename else filename
        result_filename = f"{base}_fileforge.{result_ext}"

        update_job(
            job_id,
            status=JobStatus.DONE,
            progress=100,
            result=result_bytes,
            result_filename=result_filename,
            original_size=len(data),
            result_size=len(result_bytes),
        )

    except Exception as e:
        update_job(job_id, status=JobStatus.ERROR, error=str(e))
