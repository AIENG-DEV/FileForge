from typing import Optional

EXTENSION_MAP = {
    # Images
    "jpg": "image", "jpeg": "image", "png": "image", "webp": "image",
    "gif": "image", "bmp": "image", "tiff": "image", "tif": "image",
    "avif": "image", "heic": "image", "heif": "image", "ico": "image",
    "svg": "image", "psd": "image", "jfif": "image", "jpe": "image",
    "exr": "image", "hdr": "image", "raw": "image", "cr2": "image",
    "nef": "image", "arw": "image",
    # Video
    "mp4": "video", "mov": "video", "avi": "video", "mkv": "video",
    "webm": "video", "flv": "video", "wmv": "video", "m4v": "video",
    "3gp": "video", "ogv": "video", "ts": "video", "mts": "video",
    "m2ts": "video", "vob": "video", "asf": "video", "rm": "video",
    # Audio
    "mp3": "audio", "wav": "audio", "flac": "audio", "ogg": "audio",
    "aac": "audio", "m4a": "audio", "wma": "audio", "opus": "audio",
    "aiff": "audio", "aif": "audio", "au": "audio", "ra": "audio",
    "amr": "audio", "mid": "audio", "midi": "audio",
    # PDF
    "pdf": "pdf",
    # Documents
    "doc": "document", "docx": "document", "ppt": "document",
    "pptx": "document", "xls": "document", "xlsx": "document",
    "odt": "document", "odp": "document", "ods": "document",
    "rtf": "document", "txt": "document", "csv": "document",
    "md": "document", "epub": "document", "mobi": "document",
    "pages": "document", "numbers": "document", "key": "document",
    # Archives
    "zip": "archive", "tar": "archive", "gz": "archive",
    "bz2": "archive", "xz": "archive", "7z": "archive",
    "rar": "archive", "cab": "archive", "iso": "archive",
    "dmg": "archive", "pkg": "archive", "deb": "archive",
    # Code/Data
    "json": "code", "xml": "code", "yaml": "code", "yml": "code",
    "html": "code", "htm": "code", "css": "code", "js": "code",
    "ts": "code", "jsx": "code", "tsx": "code", "toml": "code",
    "ini": "code", "cfg": "code", "conf": "code", "sql": "code",
}

SUPPORTED_FORMATS = {
    "image": {
        "input": ["jpg","jpeg","png","webp","gif","bmp","tiff","avif","heic","heif","ico","svg","jfif","jpe","psd","raw","exr","hdr"],
        "output": ["jpg","png","webp","gif","bmp","tiff","avif","ico"],
        "operations": ["compress","convert","upscale"]
    },
    "video": {
        "input": ["mp4","mov","avi","mkv","webm","flv","wmv","m4v","3gp","ogv","ts"],
        "output": ["mp4","webm","avi","mkv","mov","mp3"],
        "operations": ["compress","convert"]
    },
    "audio": {
        "input": ["mp3","wav","flac","ogg","aac","m4a","wma","opus","aiff","au"],
        "output": ["mp3","wav","flac","ogg","aac","opus","m4a"],
        "operations": ["compress","convert"]
    },
    "pdf": {
        "input": ["pdf"],
        "output": ["pdf","jpg","png"],
        "operations": ["compress","convert"]
    },
    "document": {
        "input": ["doc","docx","ppt","pptx","xls","xlsx","odt","odp","ods","rtf","txt","csv","md","epub"],
        "output": ["pdf","txt","csv","md","html","docx","xlsx"],
        "operations": ["compress","convert"]
    },
    "archive": {
        "input": ["zip","tar","gz","bz2","xz","7z"],
        "output": ["zip","tar.gz","tar.bz2"],
        "operations": ["compress","convert"]
    },
    "code": {
        "input": ["json","xml","yaml","yml","html","css","js","ts","csv","toml"],
        "output": ["json","xml","yaml","html","css","js","txt"],
        "operations": ["compress","convert"]
    },
}

def detect_type(filename: str) -> str:
    if not filename or '.' not in filename:
        return "unknown"
    ext = filename.rsplit('.', 1)[-1].lower()
    return EXTENSION_MAP.get(ext, "unknown")

def get_ext(filename: str) -> str:
    if '.' not in filename:
        return ''
    return filename.rsplit('.', 1)[-1].lower()

def get_supported_formats() -> dict:
    return SUPPORTED_FORMATS
