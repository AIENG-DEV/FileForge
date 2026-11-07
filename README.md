# FileForge — Universal File Compression & Conversion Platform

FileForge is a high-performance web application designed to compress, upscale, and convert virtually any file format with ease, safety, and scale.

---

## 🚀 Key Features

### 1. Universal Format Support (70+ Formats)
- **🖼️ Images**: JPG, JPEG, PNG, WEBP, GIF, BMP, TIFF, AVIF, HEIC, HEIF, ICO, SVG, PSD, RAW, EXR, HDR, JFIF
  - *Operations*: Downscale compression (quality & dimensions), upscale resolution (LANCZOS 1.5×–4×), cross-format conversion.
- **📄 Documents**: DOC, DOCX, PPT, PPTX, XLS, XLSX, ODT, ODP, ODS, RTF, TXT, CSV, MD, EPUB
  - *Operations*: Recompression, markdown-to-HTML, minification, formatting.
- **📕 PDF**: PDF
  - *Operations*: Stream compression, page extraction to JPG/PNG images, PDF merging.
- **🎵 Audio**: MP3, WAV, FLAC, OGG, AAC, M4A, WMA, OPUS, AIFF, AU
  - *Operations*: Bitrate downscaling (e.g. 128k, 64k), cross-codec conversion.
- **🎬 Video**: MP4, MOV, AVI, MKV, WEBM, FLV, WMV, M4V, 3GP, OGV, TS
  - *Operations*: H.264/CRF compression, web-optimized encoding, audio extraction to MP3.
- **📦 Archives**: ZIP, TAR, GZ, BZ2, XZ, 7Z, RAR
  - *Operations*: Max DEFLATE recompression, repacking.
- **🔣 Code & Data**: JSON, XML, YAML, HTML, CSS, JS, TS, CSV
  - *Operations*: Minification, whitespace compression, JSON↔YAML cross-conversion.

---

## 🔒 Enterprise-Grade Security

1. **Magic Bytes Validation**: Verifies actual binary signatures to prevent file spoofing and malicious masquerading.
2. **Strict Extension Allowlist**: Rejects unapproved or dangerous executable extensions.
3. **Zip-Bomb & Decompression Protection**: Analyzes compression ratios before unpacking archives to mitigate DoS vulnerabilities.
4. **Sanitized File Paths**: Blocks path traversal attempts (`../`) and enforces clean filename constraints.
5. **Dynamic Size Quotas**:
   - Images: 50MB
   - Videos: 500MB
   - Documents & PDFs: 50MB
   - Archives: 200MB
6. **Sliding-Window Rate Limiting**: Built-in sliding window rate limiter per client IP to safeguard against traffic spikes.

---

## ⚡ System-Level Scaling & Traffic Management

- **Asynchronous Task Architecture**: Non-blocking background worker pipeline prevents server bottlenecks during long encode jobs.
- **Real-Time Job Polling & WebSocket**: Live status tracking (`queued` → `processing` → `done` with % progress).
- **Production Nginx Gateway**:
  - `limit_req_zone` for connection throttling and burst handling.
  - WebSocket forwarding (`/ws/`).
  - Keepalive upstream connection pooling.
- **Containerized Multi-Worker Scaling**: `docker-compose.yml` pre-configured with Redis queue and multi-worker Uvicorn instances.

---

## 🛠️ Quick Start

### Option A: Local Development (Windows)
Double-click `start.bat` or run:
```powershell
.\run_dev.ps1
```

Or manually:
```powershell
# 1. Start Backend
cd backend
uvicorn main:app --reload --port 8000

# 2. Start Frontend
cd frontend
npm run dev
```
Open [http://localhost:5173](http://localhost:5173).

### Option B: Docker Production Stack
```bash
docker-compose up --build
```
Access the application on [http://localhost](http://localhost).

