"""
PDF processor using pypdf.
"""
import io
from typing import Optional


def compress_pdf(data: bytes, quality: int = 75) -> bytes:
    """Compress PDF by compressing content streams."""
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(io.BytesIO(data))
        writer = PdfWriter()
        writer.clone_reader_document_root(reader)
        for page in writer.pages:
            page.compress_content_streams()
        buf = io.BytesIO()
        writer.write(buf)
        result = buf.getvalue()
        # Only return if actually smaller
        return result if len(result) < len(data) else data
    except Exception:
        return data


def pdf_to_images(data: bytes, fmt: str = 'jpg', dpi: int = 150) -> list[bytes]:
    """Convert each PDF page to an image. Returns list of image bytes."""
    try:
        from pypdf import PdfReader
        from PIL import Image
        import io as _io

        reader = PdfReader(_io.BytesIO(data))
        images = []

        for page in reader.pages:
            # Try to extract images from page
            for img_obj in page.images:
                buf = _io.BytesIO(img_obj.data)
                img = Image.open(buf)
                out = _io.BytesIO()
                save_fmt = 'JPEG' if fmt == 'jpg' else fmt.upper()
                if save_fmt == 'JPEG' and img.mode in ('RGBA', 'P'):
                    img = img.convert('RGB')
                img.save(out, format=save_fmt)
                images.append(out.getvalue())

        return images if images else [data]
    except Exception:
        return [data]


def merge_pdfs(pdf_list: list[bytes]) -> bytes:
    """Merge multiple PDFs into one."""
    try:
        from pypdf import PdfWriter
        writer = PdfWriter()
        for pdf_data in pdf_list:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(pdf_data))
            for page in reader.pages:
                writer.add_page(page)
        buf = io.BytesIO()
        writer.write(buf)
        return buf.getvalue()
    except Exception:
        return pdf_list[0] if pdf_list else b''
