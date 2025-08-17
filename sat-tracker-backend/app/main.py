from fastapi import FastAPI
from app.core.config import settings
from app.db.mongo import get_db
from app.routers import satellites, health

app = FastAPI(title=settings.APP_NAME)

# Routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(satellites.router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup():
    # Init DB & indexes
    await get_db()

# Root
@app.get("/")
async def root():
    return {"name": settings.APP_NAME, "docs": "/docs", "openapi": "/openapi.json"}
