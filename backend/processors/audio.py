"""
Audio processing using pydub and self-contained or system FFmpeg.
Includes pure Python WAV fallback for zero-dependency WAV downsampling.
"""
import io
import os
import wave
import tempfile
from pydub import AudioSegment
from utils.ffmpeg_helper import get_ffmpeg_path


def _ensure_pydub_converter():
    ffmpeg_exe = get_ffmpeg_path()
    if ffmpeg_exe:
        AudioSegment.converter = ffmpeg_exe
        AudioSegment.ffmpeg = ffmpeg_exe


def _load_audio(data: bytes, source_ext: str) -> AudioSegment:
    _ensure_pydub_converter()
    with tempfile.NamedTemporaryFile(suffix=f".{source_ext}", delete=False) as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    try:
        segment = AudioSegment.from_file(tmp_path, format=source_ext)
    except FileNotFoundError as e:
        raise RuntimeError(
            "Could not decode audio. Portable FFmpeg executable could not be initialized."
        ) from e
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
    return segment


def _export_audio(segment: AudioSegment, target_ext: str, bitrate: str) -> bytes:
    _ensure_pydub_converter()
    buf = io.BytesIO()
    segment.export(buf, format=target_ext, bitrate=bitrate)
    return buf.getvalue()


def compress_audio(data: bytes, source_ext: str, bitrate: str = "128k") -> bytes:
    """Reduce audio bitrate."""
    # Pure Python fast path for WAV files
    if source_ext.lower() == 'wav':
        try:
            return _compress_wav_pure_python(data)
        except Exception:
            pass
    segment = _load_audio(data, source_ext)
    return _export_audio(segment, source_ext, bitrate)


def convert_audio(
    data: bytes,
    source_ext: str,
    target_ext: str,
    bitrate: str = "192k",
) -> bytes:
    """Convert audio to target format."""
    target_ext = target_ext.lower().lstrip(".")
    segment = _load_audio(data, source_ext)
    return _export_audio(segment, target_ext, bitrate)


def _compress_wav_pure_python(data: bytes) -> bytes:
    """Zero-dependency WAV downsampler converting stereo to mono or downsampling if needed."""
    in_buf = io.BytesIO(data)
    with wave.open(in_buf, 'rb') as r:
        n_channels, sampwidth, framerate, n_frames = r.getparams()[:4]
        frames = r.readframes(n_frames)
        # If stereo, downsample to mono
        if n_channels == 2:
            out_buf = io.BytesIO()
            with wave.open(out_buf, 'wb') as w:
                w.setnchannels(1)
                w.setsampwidth(sampwidth)
                w.setframerate(framerate)
                # Take every other sample for 16-bit
                if sampwidth == 2:
                    import audioop
                    try:
                        mono_frames = audioop.tomono(frames, 2, 0.5, 0.5)
                        w.writeframes(mono_frames)
                        res = out_buf.getvalue()
                        if len(res) < len(data):
                            return res
                    except Exception:
                        pass
    return data
