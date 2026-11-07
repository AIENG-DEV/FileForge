"""
Video processor using self-contained or system FFmpeg.
"""
import io
import os
import tempfile
import subprocess
from typing import Optional
from utils.ffmpeg_helper import get_ffmpeg_path, is_ffmpeg_available


def compress_video(data: bytes, source_ext: str, crf: int = 28, preset: str = "fast") -> bytes:
    """
    Compress video using H.264 with CRF (higher = smaller, default 28).
    Returns compressed bytes in mp4 format.
    """
    ffmpeg_exe = get_ffmpeg_path()
    if not ffmpeg_exe:
        raise RuntimeError("No working FFmpeg binary found. Please check imageio-ffmpeg installation.")

    with tempfile.NamedTemporaryFile(suffix=f'.{source_ext}', delete=False) as fin:
        fin.write(data)
        fin_path = fin.name

    out_path = fin_path + '_out.mp4'
    try:
        subprocess.run([
            ffmpeg_exe, '-y', '-i', fin_path,
            '-vcodec', 'libx264', '-crf', str(crf),
            '-preset', preset, '-acodec', 'aac',
            '-movflags', '+faststart',
            out_path
        ], capture_output=True, timeout=300, check=True)

        with open(out_path, 'rb') as f:
            return f.read()
    except subprocess.CalledProcessError:
        return data
    finally:
        for p in [fin_path, out_path]:
            try: os.unlink(p)
            except: pass


def convert_video(data: bytes, source_ext: str, target_ext: str) -> bytes:
    """Convert video to target format."""
    ffmpeg_exe = get_ffmpeg_path()
    if not ffmpeg_exe:
        raise RuntimeError("No working FFmpeg binary found. Please check imageio-ffmpeg installation.")

    codec_map = {
        'mp4': ['-vcodec', 'libx264', '-acodec', 'aac'],
        'webm': ['-vcodec', 'libvpx-vp9', '-acodec', 'libopus'],
        'avi': ['-vcodec', 'mpeg4', '-acodec', 'mp3'],
        'mkv': ['-vcodec', 'libx264', '-acodec', 'aac'],
        'mov': ['-vcodec', 'libx264', '-acodec', 'aac'],
        'mp3': ['-vn', '-acodec', 'libmp3lame', '-ab', '192k'],  # audio-only extract
    }

    with tempfile.NamedTemporaryFile(suffix=f'.{source_ext}', delete=False) as fin:
        fin.write(data)
        fin_path = fin.name

    out_path = fin_path + f'_out.{target_ext}'
    try:
        codec_args = codec_map.get(target_ext, ['-c', 'copy'])
        subprocess.run(
            [ffmpeg_exe, '-y', '-i', fin_path] + codec_args + [out_path],
            capture_output=True, timeout=300, check=True
        )
        with open(out_path, 'rb') as f:
            return f.read()
    except subprocess.CalledProcessError:
        return data
    finally:
        for p in [fin_path, out_path]:
            try: os.unlink(p)
            except: pass
