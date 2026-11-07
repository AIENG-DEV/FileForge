from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from utils.magic_bytes import validate_magic, check_zip_bomb, sanitize_filename
from utils.file_detector import detect_type
from config import get_settings
import re

ALLOWED_EXTENSIONS = {
    # images
    "jpg","jpeg","png","webp","gif","bmp","tiff","avif","heic","heif","ico","svg","psd","jfif","jpe","exr","hdr",
    # video
    "mp4","mov","avi","mkv","webm","flv","wmv","m4v","3gp","ogv","ts",
    # audio
    "mp3","wav","flac","ogg","aac","m4a","wma","opus","aiff","au",
    # docs
    "doc","docx","ppt","pptx","xls","xlsx","odt","odp","ods","rtf","txt","csv","md","epub","mobi",
    # pdf
    "pdf",
    # archives
    "zip","tar","gz","bz2","xz","7z","rar",
    # code/data
    "json","xml","yaml","html","css","js","ts",
}

SIZE_LIMITS = {
    "image": 50 * 1024 * 1024,
    "video": 500 * 1024 * 1024,
    "audio": 100 * 1024 * 1024,
    "document": 25 * 1024 * 1024,
    "pdf": 50 * 1024 * 1024,
    "archive": 200 * 1024 * 1024,
    "code": 5 * 1024 * 1024,
    "unknown": 20 * 1024 * 1024,
}

def validate_upload(data: bytes, filename: str) -> str:
    """
    Full security validation. Returns sanitized filename.
    Raises HTTPException on failure.
    """
    settings = get_settings()
    
    # 1. Sanitize filename
    clean_name = sanitize_filename(filename)
    
    # 2. Extension allowlist
    ext = clean_name.rsplit('.', 1)[-1].lower() if '.' in clean_name else ''
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"File type '.{ext}' is not supported")
    
    # 3. Size limit
    file_type = detect_type(clean_name)
    limit = SIZE_LIMITS.get(file_type, SIZE_LIMITS["unknown"])
    if len(data) > limit:
        mb = limit // (1024 * 1024)
        raise HTTPException(413, f"File exceeds {mb}MB limit for {file_type} files")
    
    # 4. Magic bytes
    if not validate_magic(data, ext):
        raise HTTPException(400, f"File content does not match extension '.{ext}'. Possible spoofing.")
    
    # 5. Zip bomb
    if ext == 'zip' and not check_zip_bomb(data):
        raise HTTPException(400, "Archive compression ratio is too high (possible zip bomb)")
    
    return clean_name
