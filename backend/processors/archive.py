"""
Archive processor: recompress zip, tar, etc.
"""
import io
import zipfile
import tarfile
import os
import tempfile


def compress_to_zip(data: bytes, filename: str) -> bytes:
    """
    If input is a zip, re-compress with max DEFLATE.
    Otherwise, wrap the file in a new zip.
    """
    if data[:4] == b'PK\x03\x04':
        # Recompress existing zip
        input_buf = io.BytesIO(data)
        output_buf = io.BytesIO()
        try:
            with zipfile.ZipFile(input_buf, 'r') as zin:
                with zipfile.ZipFile(output_buf, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
                    for item in zin.infolist():
                        zout.writestr(item, zin.read(item.filename))
            return output_buf.getvalue()
        except Exception:
            return data
    else:
        # Wrap single file in zip
        output_buf = io.BytesIO()
        with zipfile.ZipFile(output_buf, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
            zout.writestr(filename, data)
        return output_buf.getvalue()


def compress_to_targz(data: bytes, filename: str) -> bytes:
    """Recompress to tar.gz."""
    output_buf = io.BytesIO()
    with tarfile.open(fileobj=output_buf, mode='w:gz') as tar:
        info = tarfile.TarInfo(name=filename)
        info.size = len(data)
        tar.addfile(info, io.BytesIO(data))
    return output_buf.getvalue()


def convert_archive(data: bytes, source_ext: str, target_ext: str, filename: str) -> bytes:
    if target_ext == 'zip':
        return compress_to_zip(data, filename)
    elif target_ext in ('tar.gz', 'gz'):
        return compress_to_targz(data, filename)
    return data
