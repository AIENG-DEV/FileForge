"""
Document processor: compress and convert documents.
Requires python-docx, openpyxl. PDF conversion requires LibreOffice (optional).
"""
import io
import zipfile
import os
import tempfile
from typing import Optional


def compress_docx(data: bytes) -> bytes:
    """Re-zip a docx with maximum compression."""
    input_buf = io.BytesIO(data)
    output_buf = io.BytesIO()
    with zipfile.ZipFile(input_buf, 'r') as zin:
        with zipfile.ZipFile(output_buf, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zout:
            for item in zin.infolist():
                zout.writestr(item, zin.read(item.filename))
    return output_buf.getvalue()


def compress_xlsx(data: bytes) -> bytes:
    """Re-zip an xlsx with maximum compression."""
    return compress_docx(data)  # xlsx is also a zip


def compress_text(data: bytes, encoding: str = 'utf-8') -> bytes:
    """Strip extra whitespace from plain text."""
    try:
        text = data.decode(encoding, errors='replace')
        lines = [line.rstrip() for line in text.splitlines()]
        # Remove consecutive blank lines
        result = []
        blank = False
        for line in lines:
            if line.strip() == '':
                if not blank:
                    result.append('')
                blank = True
            else:
                result.append(line)
                blank = False
        return '\n'.join(result).encode(encoding)
    except Exception:
        return data


def compress_csv(data: bytes) -> bytes:
    """Strip whitespace from CSV cells."""
    try:
        import csv
        text = data.decode('utf-8', errors='replace')
        reader = csv.reader(io.StringIO(text))
        output = io.StringIO()
        writer = csv.writer(output)
        for row in reader:
            writer.writerow([cell.strip() for cell in row])
        return output.getvalue().encode('utf-8')
    except Exception:
        return data


def compress_json(data: bytes) -> bytes:
    """Minify JSON."""
    import json
    try:
        obj = json.loads(data)
        return json.dumps(obj, separators=(',', ':')).encode('utf-8')
    except Exception:
        return data


def compress_xml(data: bytes) -> bytes:
    """Minify XML by removing whitespace between tags."""
    import re
    try:
        text = data.decode('utf-8', errors='replace')
        text = re.sub(r'>\s+<', '><', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip().encode('utf-8')
    except Exception:
        return data


def compress_yaml(data: bytes) -> bytes:
    """Round-trip YAML to strip comments and normalize."""
    try:
        import yaml
        obj = yaml.safe_load(data)
        return yaml.dump(obj, default_flow_style=False).encode('utf-8')
    except Exception:
        return data


def convert_md_to_html(data: bytes) -> bytes:
    """Convert Markdown to HTML."""
    try:
        import markdown
        text = data.decode('utf-8', errors='replace')
        return markdown.markdown(text).encode('utf-8')
    except ImportError:
        # Basic fallback
        import re
        text = data.decode('utf-8', errors='replace')
        text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        return f"<html><body>{text}</body></html>".encode('utf-8')


def convert_json_to_yaml(data: bytes) -> bytes:
    try:
        import json, yaml
        obj = json.loads(data)
        return yaml.dump(obj, default_flow_style=False).encode('utf-8')
    except Exception:
        return data


def convert_yaml_to_json(data: bytes) -> bytes:
    try:
        import json, yaml
        obj = yaml.safe_load(data)
        return json.dumps(obj, indent=2).encode('utf-8')
    except Exception:
        return data


def compress_document(data: bytes, ext: str) -> bytes:
    ext = ext.lower()
    if ext in ('docx', 'pptx', 'xlsx', 'odt', 'odp', 'ods', 'epub'):
        return compress_docx(data)
    elif ext in ('txt', 'md', 'rtf'):
        return compress_text(data)
    elif ext == 'csv':
        return compress_csv(data)
    elif ext == 'json':
        return compress_json(data)
    elif ext == 'xml':
        return compress_xml(data)
    elif ext in ('yaml', 'yml'):
        return compress_yaml(data)
    return data


def convert_document(data: bytes, source_ext: str, target_ext: str) -> bytes:
    source_ext = source_ext.lower()
    target_ext = target_ext.lower()

    if source_ext == 'md' and target_ext == 'html':
        return convert_md_to_html(data)
    if source_ext == 'json' and target_ext in ('yaml', 'yml'):
        return convert_json_to_yaml(data)
    if source_ext in ('yaml', 'yml') and target_ext == 'json':
        return convert_yaml_to_json(data)
    if source_ext in ('txt', 'md') and target_ext == 'txt':
        return data
    # For docx/pdf conversions requiring LibreOffice, return data with note
    return data
