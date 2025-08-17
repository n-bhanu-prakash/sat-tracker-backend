import httpx
from datetime import datetime
from typing import Any, Dict
from app.core.config import settings
from app.utils.exceptions import UpstreamAuthError, UpstreamRateLimited, UpstreamError
from app.utils.cache import SoftRateLimiter

_client: httpx.AsyncClient | None = None
_limiter = SoftRateLimiter(settings.MAX_OUTBOUND_RPS)

async def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, read=20.0))
    return _client

def _build_url(path: str) -> str:
    # path already formatted, just append apiKey query param
    sep = "&" if "?" in path or "&" in path else ""
    return f"{settings.N2YO_BASE_URL}{path}{sep}&apiKey={settings.N2YO_API_KEY}"

async def _handle_response(resp: httpx.Response) -> Dict[str, Any]:
    # Basic normalization and error mapping
    if resp.status_code == 401 or resp.status_code == 403:
        raise UpstreamAuthError()
    if resp.status_code == 429:
        raise UpstreamRateLimited()
    if resp.status_code >= 500:
        raise UpstreamError(status_code=502, detail="N2YO server error")
    if resp.status_code >= 400:
        raise UpstreamError(status_code=resp.status_code, detail=resp.text)
    data = resp.json()
    return data

async def fetch_tle(norad_id: int) -> Dict[str, Any]:
    await _limiter.throttle()
    client = await get_http_client()
    url = _build_url(f"/tle/{norad_id}")
    return await _handle_response(await client.get(url))

async def fetch_positions(norad_id: int, lat: float, lng: float, alt: float, seconds: int) -> Dict[str, Any]:
    await _limiter.throttle()
    client = await get_http_client()
    # /positions/{id}/{observer_lat}/{observer_lng}/{observer_alt}/{seconds}
    url = _build_url(f"/positions/{norad_id}/{lat}/{lng}/{alt}/{seconds}")
    return await _handle_response(await client.get(url))

async def fetch_visual_passes(norad_id: int, lat: float, lng: float, alt: float, days: int, min_visibility: int) -> Dict[str, Any]:
    await _limiter.throttle()
    client = await get_http_client()
    url = _build_url(f"/visualpasses/{norad_id}/{lat}/{lng}/{alt}/{days}/{min_visibility}")
    return await _handle_response(await client.get(url))

async def fetch_radio_passes(norad_id: int, lat: float, lng: float, alt: float, days: int) -> Dict[str, Any]:
    await _limiter.throttle()
    client = await get_http_client()
    url = _build_url(f"/radiopasses/{norad_id}/{lat}/{lng}/{alt}/{days}/0")  # last param = min el (deg), 0 default
    return await _handle_response(await client.get(url))

async def fetch_above(lat: float, lng: float, alt: float, radius: int, category_id: int) -> Dict[str, Any]:
    await _limiter.throttle()
    client = await get_http_client()
    url = _build_url(f"/above/{lat}/{lng}/{alt}/{radius}/{category_id}")
    return await _handle_response(await client.get(url))
