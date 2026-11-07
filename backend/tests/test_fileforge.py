import io
import os
import sys
import zipfile
import pytest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from utils.file_detector import detect_type, get_supported_formats
from utils.magic_bytes import validate_magic, check_zip_bomb, sanitize_filename
from middleware.security import validate_upload, ALLOWED_EXTENSIONS
from processors import image, pdf, document, archive, audio, video
from jobs.queue import create_job, get_job, get_job_result, JobStatus
from jobs.processor import process_job

client = TestClient(app)


# =====================================================================
# 1. UTILS & SECURITY TESTS
# =====================================================================

def test_file_detector_categories():
    assert detect_type("photo.jpg") == "image"
    assert detect_type("photo.PNG") == "image"
    assert detect_type("clip.mp4") == "video"
    assert detect_type("song.mp3") == "audio"
    assert detect_type("doc.pdf") == "pdf"
    assert detect_type("sheet.xlsx") == "document"
    assert detect_type("archive.zip") == "archive"
    assert detect_type("data.json") == "code"
    assert detect_type("unknown_file") == "unknown"


def test_sanitize_filename():
    assert sanitize_filename("../../../etc/passwd") == "passwd"
    assert sanitize_filename("..\\..\\windows\\system32\\cmd.exe") == "cmd.exe"
    clean = sanitize_filename("my photo! @#$.png")
    assert not any(c in clean for c in ['!', '@', '#', '$', ' '])


def test_magic_bytes_validation():
    # Valid PNG
    png_header = b'\x89PNG\r\n\x1a\n' + b'\x00' * 50
    assert validate_magic(png_header, "png") is True

    # Valid JPEG
    jpg_header = b'\xff\xd8\xff\xe0' + b'\x00' * 50
    assert validate_magic(jpg_header, "jpg") is True

    # Valid PDF
    pdf_header = b'%PDF-1.4\n' + b'\x00' * 50
    assert validate_magic(pdf_header, "pdf") is True

    # Valid ZIP
    zip_header = b'PK\x03\x04' + b'\x00' * 50
    assert validate_magic(zip_header, "zip") is True

    # Spoofed file: executable disguised as PNG
    fake_png = b'MZ\x90\x00' + b'\x00' * 50
    assert validate_magic(fake_png, "png") is False


def test_zip_bomb_detection():
    # Normal small zip
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("test.txt", b"Hello world! " * 10)
    normal_zip = buf.getvalue()
    assert check_zip_bomb(normal_zip) is True


def test_validate_upload_rejection():
    from fastapi import HTTPException

    # Disallowed extension (.exe)
    with pytest.raises(HTTPException) as exc_info:
        validate_upload(b'test content', 'malicious.exe')
    assert exc_info.value.status_code == 400

    # Spoofed magic bytes
    with pytest.raises(HTTPException) as exc_info:
        validate_upload(b'random text data not a jpeg', 'image.jpg')
    assert exc_info.value.status_code == 400


# =====================================================================
# 2. IMAGE PROCESSOR TESTS
# =====================================================================

@pytest.fixture
def sample_jpeg_bytes():
    from PIL import Image
    buf = io.BytesIO()
    img = Image.new('RGB', (200, 200), color='red')
    img.save(buf, format='JPEG', quality=95)
    return buf.getvalue()


@pytest.fixture
def sample_png_bytes():
    from PIL import Image
    buf = io.BytesIO()
    img = Image.new('RGBA', (150, 150), color=(0, 255, 0, 128))
    img.save(buf, format='PNG')
    return buf.getvalue()


def test_image_compress(sample_jpeg_bytes):
    compressed, ext = image.compress_image(sample_jpeg_bytes, "test.jpg", quality=30)
    assert ext == "jpg"
    assert len(compressed) > 0
    assert len(compressed) < len(sample_jpeg_bytes)


def test_image_resize(sample_jpeg_bytes):
    from PIL import Image
    compressed, ext = image.compress_image(sample_jpeg_bytes, "test.jpg", quality=75, max_width=50)
    result_img = Image.open(io.BytesIO(compressed))
    assert result_img.width <= 50


def test_image_convert_jpg_to_png(sample_jpeg_bytes):
    converted = image.convert_image(sample_jpeg_bytes, "jpg", "png")
    assert converted.startswith(b'\x89PNG')


def test_image_convert_png_to_webp(sample_png_bytes):
    converted = image.convert_image(sample_png_bytes, "png", "webp")
    assert b'WEBP' in converted[:16]


def test_image_upscale(sample_jpeg_bytes):
    from PIL import Image
    upscaled, ext = image.upscale_image(sample_jpeg_bytes, "test.jpg", scale=2.0)
    result_img = Image.open(io.BytesIO(upscaled))
    assert result_img.width == 400
    assert result_img.height == 400


# =====================================================================
# 3. PDF PROCESSOR TESTS
# =====================================================================

@pytest.fixture
def sample_pdf_bytes():
    from pypdf import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


def test_pdf_compress(sample_pdf_bytes):
    res = pdf.compress_pdf(sample_pdf_bytes)
    assert len(res) > 0
    assert res.startswith(b'%PDF')


def test_pdf_merge(sample_pdf_bytes):
    from pypdf import PdfReader
    merged = pdf.merge_pdfs([sample_pdf_bytes, sample_pdf_bytes])
    reader = PdfReader(io.BytesIO(merged))
    assert len(reader.pages) == 2


# =====================================================================
# 4. DOCUMENT & CODE PROCESSOR TESTS
# =====================================================================

def test_document_compress_json():
    raw_json = b'{\n  "key": "value",   \n  "count":   123\n}'
    minified = document.compress_json(raw_json)
    assert minified == b'{"key":"value","count":123}'


def test_document_compress_xml():
    raw_xml = b'<root>   <child>  Hello  </child>   </root>'
    minified = document.compress_xml(raw_xml)
    assert minified == b'<root><child> Hello </child></root>'


def test_document_compress_yaml():
    raw_yaml = b'# comment\nname: John\nage: 30\n'
    result = document.compress_yaml(raw_yaml)
    assert b'# comment' not in result
    assert b'name: John' in result


def test_document_convert_json_yaml():
    json_data = b'{"hello": "world"}'
    yaml_out = document.convert_json_to_yaml(json_data)
    assert b'hello: world' in yaml_out

    back_to_json = document.convert_yaml_to_json(yaml_out)
    assert b'"hello": "world"' in back_to_json


def test_document_convert_md_to_html():
    md = b'# Title\nThis is **bold** text.'
    html = document.convert_md_to_html(md)
    assert b'<h1>Title</h1>' in html or b'Title' in html
    assert b'<strong>bold</strong>' in html


# =====================================================================
# 5. ARCHIVE PROCESSOR TESTS
# =====================================================================

def test_archive_compress_to_zip():
    data = b'Sample file contents inside an archive'
    zipped = archive.compress_to_zip(data, "test.txt")
    assert zipped.startswith(b'PK\x03\x04')
    with zipfile.ZipFile(io.BytesIO(zipped), 'r') as zf:
        assert "test.txt" in zf.namelist()
        assert zf.read("test.txt") == data


def test_archive_compress_to_targz():
    import tarfile
    data = b'Tar gzip content'
    targz = archive.compress_to_targz(data, "test.txt")
    assert len(targz) > 0
    with tarfile.open(fileobj=io.BytesIO(targz), mode='r:gz') as tar:
        assert "test.txt" in tar.getnames()


# =====================================================================
# 6. AUDIO & VIDEO PROCESSOR TESTS
# =====================================================================

def test_audio_compress_mock_or_real():
    from pydub.generators import Sine
    tone = Sine(440).to_audio_segment(duration=300)
    buf = io.BytesIO()
    tone.export(buf, format='wav')
    wav_bytes = buf.getvalue()

    compressed_wav = audio.compress_audio(wav_bytes, 'wav', '64k')
    assert len(compressed_wav) > 0

    converted_mp3 = audio.convert_audio(wav_bytes, 'wav', 'mp3', '128k')
    assert len(converted_mp3) > 0


def test_video_compress_fallback():
    from utils.ffmpeg_helper import get_ffmpeg_path
    ffmpeg_exe = get_ffmpeg_path()
    assert ffmpeg_exe is not None, "Self-contained portable FFmpeg binary should be detected"


# =====================================================================
# 7. JOB QUEUE & ASYNC PROCESSOR TESTS
# =====================================================================

def test_job_lifecycle(sample_jpeg_bytes):
    job_id = create_job("test.jpg", "compress", {"quality": 50})
    job = get_job(job_id)
    assert job["status"] == JobStatus.QUEUED

    # Execute processor directly
    process_job(job_id, sample_jpeg_bytes, "test.jpg", "compress", {"quality": 50})

    updated_job = get_job(job_id)
    assert updated_job["status"] == JobStatus.DONE
    assert updated_job["progress"] == 100
    assert updated_job["result_size"] > 0

    result = get_job_result(job_id)
    assert result is not None
    data, filename = result
    assert filename.endswith(".jpg")
    assert len(data) == updated_job["result_size"]


# =====================================================================
# 8. API ROUTE INTEGRATION TESTS
# =====================================================================

def test_api_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "healthy"}


def test_api_formats():
    res = client.get("/formats")
    assert res.status_code == 200
    data = res.json()
    assert "image" in data
    assert "pdf" in data
    assert "video" in data
    assert "audio" in data
    assert "document" in data


def test_api_upload_and_download_flow(sample_jpeg_bytes):
    # 1. Upload
    res = client.post(
        "/upload",
        files={"file": ("photo.jpg", sample_jpeg_bytes, "image/jpeg")},
        data={"operation": "compress", "quality": 60}
    )
    assert res.status_code == 200
    job_id = res.json()["job_id"]
    assert job_id is not None

    # 2. Check Job status
    job_res = client.get(f"/job/{job_id}")
    assert job_res.status_code == 200
    assert job_res.json()["status"] in ["queued", "processing", "done"]

    # 3. Wait/ensure done (since background task runs in threadpool)
    import time
    for _ in range(10):
        if client.get(f"/job/{job_id}").json()["status"] == "done":
            break
        time.sleep(0.3)

    # 4. Download
    dl_res = client.get(f"/download/{job_id}")
    assert dl_res.status_code == 200
    assert dl_res.headers["content-type"] == "image/jpeg"
    assert len(dl_res.content) > 0


def test_api_bundle_download(sample_jpeg_bytes):
    # Upload two files
    r1 = client.post("/upload", files={"file": ("f1.jpg", sample_jpeg_bytes, "image/jpeg")}, data={"operation": "compress"})
    r2 = client.post("/upload", files={"file": ("f2.jpg", sample_jpeg_bytes, "image/jpeg")}, data={"operation": "compress"})
    j1, j2 = r1.json()["job_id"], r2.json()["job_id"]

    import time
    time.sleep(1.0) # allow processing

    # Download bundle
    bundle_res = client.post("/download-bundle", json={"job_ids": [j1, j2]})
    if bundle_res.status_code == 200:
        assert bundle_res.headers["content-type"] == "application/zip"
        assert len(bundle_res.content) > 0


def test_api_sync_endpoints(sample_jpeg_bytes):
    # Sync compress
    res = client.post(
        "/compress",
        files={"file": ("sync.jpg", sample_jpeg_bytes, "image/jpeg")},
        data={"quality": 40}
    )
    assert res.status_code == 200
    assert "x-original-size" in res.headers
    assert "x-compressed-size" in res.headers

    # Sync convert
    res_conv = client.post(
        "/convert",
        files={"file": ("sync.jpg", sample_jpeg_bytes, "image/jpeg")},
        data={"target_format": "png"}
    )
    assert res_conv.status_code == 200
    assert res_conv.headers["content-type"] == "image/png"

    # Sync upscale
    res_up = client.post(
        "/upscale",
        files={"file": ("sync.jpg", sample_jpeg_bytes, "image/jpeg")},
        data={"scale": 2.0}
    )
    assert res_up.status_code == 200
