import time
import hashlib
from fastapi import Request, HTTPException

# In-memory fallback when Redis is not available
_counters: dict = {}

def _get_client_key(request: Request) -> str:
    ip = request.client.host if request.client else "unknown"
    return f"ratelimit:{ip}"

def check_rate_limit(request: Request, max_requests: int = 10, window_seconds: int = 3600):
    """
    Simple sliding window rate limiter using in-memory store.
    When Redis is available (jobs/queue.py), upgrade to Redis.
    """
    key = _get_client_key(request)
    now = time.time()
    window_start = now - window_seconds
    
    if key not in _counters:
        _counters[key] = []
    
    # Remove old timestamps outside window
    _counters[key] = [t for t in _counters[key] if t > window_start]
    
    if len(_counters[key]) >= max_requests:
        reset_in = int(window_seconds - (now - _counters[key][0]))
        raise HTTPException(
            429,
            detail=f"Rate limit exceeded. Try again in {reset_in}s",
            headers={"Retry-After": str(reset_in)}
        )
    
    _counters[key].append(now)
