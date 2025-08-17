import asyncio, time, hashlib, json
from typing import Any, Optional

class TTLCache:
    def __init__(self, default_ttl: int = 60):
        self.default_ttl = default_ttl
        self._store: dict[str, tuple[float, Any]] = {}
        self._lock = asyncio.Lock()

    def _now(self) -> float:
        return time.monotonic()

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            item = self._store.get(key)
            if not item:
                return None
            expires_at, value = item
            if self._now() > expires_at:
                self._store.pop(key, None)
                return None
            return value

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        ttl = ttl if ttl is not None else self.default_ttl
        async with self._lock:
            self._store[key] = (self._now() + ttl, value)

    @staticmethod
    def hash_key(prefix: str, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return f"{prefix}:{hashlib.sha256(raw.encode()).hexdigest()}"

# Token-bucket-ish soft limiter (per-process)
class SoftRateLimiter:
    def __init__(self, rps: float):
        self.period = 1.0 / max(0.001, rps)
        self._lock = asyncio.Lock()
        self._last = 0.0

    async def throttle(self):
        async with self._lock:
            now = time.monotonic()
            wait = self.period - (now - self._last)
            if wait > 0:
                await asyncio.sleep(wait)
            self._last = time.monotonic()
