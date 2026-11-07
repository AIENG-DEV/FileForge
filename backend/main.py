import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import compress, convert, upscale, upload, jobs, download, formats
from utils.ffmpeg_helper import get_ffmpeg_path

# Initialize portable bundled FFmpeg executable
ffmpeg_exe = get_ffmpeg_path()
if ffmpeg_exe:
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    if ffmpeg_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

app = FastAPI(title="FileForge API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Legacy sync endpoints (keep for backward compat)
app.include_router(compress.router, tags=["sync"])
app.include_router(convert.router, tags=["sync"])
app.include_router(upscale.router, tags=["sync"])

# New async job-based endpoints
app.include_router(upload.router, tags=["jobs"])
app.include_router(jobs.router, tags=["jobs"])
app.include_router(download.router, tags=["jobs"])
app.include_router(formats.router, tags=["formats"])

@app.get("/")
def root():
    return {"status": "ok", "app": "FileForge", "version": "2.0.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}
