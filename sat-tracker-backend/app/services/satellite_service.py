from datetime import datetime, timezone
from typing import Dict, Any
from app.db.mongo import get_db
from app.utils.cache import TTLCache
from app.core.config import settings
from . import n2yo_client

# In-memory caches
hot_cache = TTLCache(default_ttl=settings.INMEMORY_CACHE_TTL_SEC)
tle_cache = TTLCache(default_ttl=settings.TLE_CACHE_TTL_SEC)

async def get_tle(norad_id: int) -> Dict[str, Any]:
    key = f"tle:{norad_id}"
    cached = await tle_cache.get(key)
    if cached:
        return {"payload": cached, "cached": True, "cached_at": datetime.now(timezone.utc)}

    # Check persistent cache
    db = await get_db()
    doc = await db.tle_cache.find_one({"norad_id": norad_id})
    if doc:
        age = (datetime.now(timezone.utc) - doc["fetched_at"]).total_seconds()
        if age < settings.TLE_CACHE_TTL_SEC:
            await tle_cache.set(key, doc["payload"])
            return {"payload": doc["payload"], "cached": True, "cached_at": doc["fetched_at"]}

    payload = await n2yo_client.fetch_tle(norad_id)
    now = datetime.now(timezone.utc)
    await tle_cache.set(key, payload)
    await db.tle_cache.update_one(
        {"norad_id": norad_id},
        {"$set": {"payload": payload, "fetched_at": now}},
        upsert=True
    )
    return {"payload": payload, "cached": False, "cached_at": now}

async def get_positions(norad_id: int, lat: float, lng: float, alt: float, seconds: int) -> Dict[str, Any]:
    cache_key = hot_cache.hash_key("positions", {
        "id": norad_id, "lat": lat, "lng": lng, "alt": alt, "seconds": seconds
    })
    cached = await hot_cache.get(cache_key)
    if cached:
        return {"payload": cached, "cached": True, "cached_at": datetime.now(timezone.utc)}

    payload = await n2yo_client.fetch_positions(norad_id, lat, lng, alt, seconds)
    await hot_cache.set(cache_key, payload)

    # Persist history (trimmed)
    db = await get_db()
    now = datetime.now(timezone.utc)
    await db.positions_history.insert_one({
        "norad_id": norad_id,
        "observer": {"lat": lat, "lng": lng, "alt": alt},
        "seconds": seconds,
        "ts": now,
        "payload": payload
    })
    return {"payload": payload, "cached": False, "cached_at": now}

async def get_visual_passes(norad_id: int, lat: float, lng: float, alt: float, days: int, min_visibility: int):
    cache_key = hot_cache.hash_key("visualpasses", {
        "id": norad_id, "lat": lat, "lng": lng, "alt": alt, "days": days, "min_visibility": min_visibility
    })
    cached = await hot_cache.get(cache_key)
    if cached:
        return {"payload": cached, "cached": True, "cached_at": datetime.now(timezone.utc)}

    payload = await n2yo_client.fetch_visual_passes(norad_id, lat, lng, alt, days, min_visibility)
    await hot_cache.set(cache_key, payload)
    return {"payload": payload, "cached": False, "cached_at": datetime.now(timezone.utc)}

async def get_radio_passes(norad_id: int, lat: float, lng: float, alt: float, days: int):
    cache_key = hot_cache.hash_key("radiopasses", {
        "id": norad_id, "lat": lat, "lng": lng, "alt": alt, "days": days
    })
    cached = await hot_cache.get(cache_key)
    if cached:
        return {"payload": cached, "cached": True, "cached_at": datetime.now(timezone.utc)}

    payload = await n2yo_client.fetch_radio_passes(norad_id, lat, lng, alt, days)
    await hot_cache.set(cache_key, payload)
    return {"payload": payload, "cached": False, "cached_at": datetime.now(timezone.utc)}

async def get_above(lat: float, lng: float, alt: float, radius: int, category_id: int):
    cache_key = hot_cache.hash_key("above", {
        "lat": lat, "lng": lng, "alt": alt, "radius": radius, "category": category_id
    })
    cached = await hot_cache.get(cache_key)
    if cached:
        return {"payload": cached, "cached": True, "cached_at": datetime.now(timezone.utc)}

    payload = await n2yo_client.fetch_above(lat, lng, alt, radius, category_id)
    await hot_cache.set(cache_key, payload)
    return {"payload": payload, "cached": False, "cached_at": datetime.now(timezone.utc)}
