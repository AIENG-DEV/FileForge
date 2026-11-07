"""
Helper to locate, alias, and initialize a self-contained FFmpeg executable.
Uses imageio-ffmpeg which auto-bundles FFmpeg for Windows, macOS, and Linux without system installs.
"""
import os
import shutil
from typing import Optional

_ffmpeg_exe: Optional[str] = None


def init_ffmpeg():
    """Initializes portable FFmpeg, creates local alias, and adds directory to PATH."""
    global _ffmpeg_exe
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            bin_dir = os.path.dirname(exe)
            alias = os.path.join(bin_dir, "ffmpeg.exe" if os.name == "nt" else "ffmpeg")
            if not os.path.exists(alias):
                try:
                    os.link(exe, alias)
                except Exception:
                    try:
                        shutil.copy2(exe, alias)
                    except Exception:
                        pass

            # Prepend to PATH so pydub and subprocesses find it as 'ffmpeg'
            if bin_dir not in os.environ.get("PATH", ""):
                os.environ["PATH"] = bin_dir + os.pathsep + os.environ.get("PATH", "")

            target_exe = alias if os.path.exists(alias) else exe
            _ffmpeg_exe = target_exe

            # Configure pydub
            try:
                from pydub import AudioSegment
                AudioSegment.converter = target_exe
                AudioSegment.ffmpeg = target_exe
            except Exception:
                pass

            return _ffmpeg_exe
    except Exception:
        pass

    # Fallback to system PATH
    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        _ffmpeg_exe = sys_ffmpeg
        return _ffmpeg_exe

    return None


def get_ffmpeg_path() -> Optional[str]:
    if not _ffmpeg_exe or not os.path.exists(_ffmpeg_exe):
        return init_ffmpeg()
    return _ffmpeg_exe


def is_ffmpeg_available() -> bool:
    return get_ffmpeg_path() is not None


# Auto-initialize on module load
init_ffmpeg()
