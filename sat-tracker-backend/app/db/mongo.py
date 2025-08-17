import motor.motor_asyncio
from pymongo import ASCENDING
from app.core.config import settings

_client: motor.motor_asyncio.AsyncIOMotorClient | None = None
_db = None

async def get_client():
    global _client
    if _client is None:
        _client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
    return _client

async def get_db():
    global _db
    if _db is None:
        client = await get_client()
        _db = client[settings.MONGO_DB]
        # Create indexes (idempotent)
        await _db.tle_cache.create_index([("norad_id", ASCENDING)], unique=True)
        await _db.positions_history.create_index([("norad_id", ASCENDING), ("ts", ASCENDING)])
        await _db.api_cache.create_index([("key", ASCENDING)], unique=True)
    return _db
