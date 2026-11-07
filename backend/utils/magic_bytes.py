MAGIC_SIGNATURES = {
    "jpg":  [(0, b'\xff\xd8\xff')],
    "jpeg": [(0, b'\xff\xd8\xff')],
    "png":  [(0, b'\x89PNG\r\n\x1a\n')],
    "gif":  [(0, b'GIF8')],
    "webp": [(0, b'RIFF'), (8, b'WEBP')],
    "bmp":  [(0, b'BM')],
    "pdf":  [(0, b'%PDF')],
    "zip":  [(0, b'PK\x03\x04'), (0, b'PK\x05\x06'), (0, b'PK\x07\x08')],
    "gz":   [(0, b'\x1f\x8b')],
    "mp3":  [(0, b'ID3'), (0, b'\xff\xfb'), (0, b'\xff\xf3'), (0, b'\xff\xf2')],
    "wav":  [(0, b'RIFF')],
    "flac": [(0, b'fLaC')],
    "ogg":  [(0, b'OggS')],
    "mp4":  [(4, b'ftyp')],
    "mov":  [(4, b'ftyp'), (4, b'moov'), (4, b'free')],
    "avi":  [(0, b'RIFF'), (8, b'AVI ')],
    "mkv":  [(0, b'\x1a\x45\xdf\xa3')],
    "docx": [(0, b'PK\x03\x04')],
    "xlsx": [(0, b'PK\x03\x04')],
    "pptx": [(0, b'PK\x03\x04')],
    "svg":  [],  # XML-based, text check
    "txt":  [],  # no magic, allow
    "csv":  [],  # no magic, allow
    "json": [],  # no magic, allow
    "xml":  [],  # no magic, allow
    "yaml": [],  # no magic, allow
    "ico":  [(0, b'\x00\x00\x01\x00')],
    "tiff": [(0, b'II*\x00'), (0, b'MM\x00*')],
    "heic": [(4, b'ftyp')],
    "heif": [(4, b'ftyp')],
    "avif": [(4, b'ftyp')],
    "bz2":  [(0, b'BZh')],
    "7z":   [(0, b"7z\xbc\xaf'\x1c")],
}

def validate_magic(data: bytes, ext: str) -> bool:
    """Returns True if file data matches expected magic bytes for the extension.
    Returns True if extension has no magic (text files, etc.)."""
    ext = ext.lower().lstrip('.')
    sigs = MAGIC_SIGNATURES.get(ext)
    if sigs is None:
        return True  # unknown ext, pass through (allowlist handles rejection)
    if len(sigs) == 0:
        return True  # no magic defined, trust extension
    for offset, magic in sigs:
        if data[offset:offset + len(magic)] == magic:
            return True
    return False

def check_zip_bomb(data: bytes, max_ratio: float = 100.0) -> bool:
    """Returns True if archive is safe. False if compression ratio is suspiciously high."""
    import zipfile, io
    if not data[:4] == b'PK\x03\x04':
        return True  # not a zip
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            compressed = sum(i.compress_size for i in zf.infolist())
            uncompressed = sum(i.file_size for i in zf.infolist())
            if compressed == 0:
                return True
            ratio = uncompressed / compressed
            return ratio <= max_ratio
    except Exception:
        return False  # treat corrupt zip as unsafe

def sanitize_filename(name: str) -> str:
    """Remove path traversal and dangerous characters."""
    import os, re
    name = os.path.basename(name)
    name = re.sub(r'[^\w\.\-]', '_', name)
    name = name.lstrip('.')
    return name[:255] or "file"
