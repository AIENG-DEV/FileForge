"""
Image processor using Pillow. Supports 18+ formats.
"""
import io
from typing import Optional
from PIL import Image, ImageFilter

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIF_SUPPORT = True
except ImportError:
    HEIF_SUPPORT = False

FORMAT_MAP = {
    'jpg': 'JPEG', 'jpeg': 'JPEG', 'png': 'PNG', 'webp': 'WEBP',
    'gif': 'GIF', 'bmp': 'BMP', 'tiff': 'TIFF', 'tif': 'TIFF',
    'avif': 'AVIF', 'ico': 'ICO', 'jfif': 'JPEG', 'jpe': 'JPEG',
}

def _open_image(data: bytes) -> Image.Image:
    return Image.open(io.BytesIO(data))

def _save_image(img: Image.Image, fmt: str, quality: int = 85) -> bytes:
    buf = io.BytesIO()
    pil_fmt = FORMAT_MAP.get(fmt.lower(), fmt.upper())

    # Handle transparency
    if pil_fmt == 'JPEG' and img.mode in ('RGBA', 'P', 'LA'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        if img.mode in ('RGBA', 'LA'):
            background.paste(img, mask=img.split()[-1])
        img = background

    if pil_fmt in ('JPEG',):
        img.save(buf, format=pil_fmt, quality=quality, optimize=True)
    elif pil_fmt == 'PNG':
        compress_level = max(0, min(9, 9 - (quality // 11)))
        img.save(buf, format='PNG', compress_level=compress_level, optimize=True)
    elif pil_fmt == 'WEBP':
        img.save(buf, format='WEBP', quality=quality, method=6)
    elif pil_fmt == 'GIF':
        img.save(buf, format='GIF', optimize=True)
    elif pil_fmt == 'AVIF':
        img.save(buf, format='AVIF', quality=quality)
    else:
        img.save(buf, format=pil_fmt)

    return buf.getvalue()


def compress_image(
    data: bytes,
    filename: str,
    quality: int = 75,
    max_width: Optional[int] = None,
    max_height: Optional[int] = None,
) -> tuple[bytes, str]:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    img = _open_image(data)

    # Resize if max dimensions given
    if max_width or max_height:
        w, h = img.size
        if max_width and w > max_width:
            ratio = max_width / w
            img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
        if max_height and img.size[1] > max_height:
            ratio = max_height / img.size[1]
            img = img.resize((int(img.size[0] * ratio), max_height), Image.LANCZOS)

    return _save_image(img, ext, quality), ext


def convert_image(data: bytes, source_ext: str, target_ext: str, quality: int = 85) -> bytes:
    img = _open_image(data)
    return _save_image(img, target_ext, quality)


def upscale_image(data: bytes, filename: str, scale: float = 2.0) -> tuple[bytes, str]:
    ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else 'jpg'
    img = _open_image(data)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    return _save_image(img, ext, 90), ext
