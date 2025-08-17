from pydantic import BaseSettings, Field, AnyUrl
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "sat-tracker-backend"
    API_V1_PREFIX: str = "/api/v1"

    # External API
    N2YO_API_KEY: str = Field(..., env="N2YO_API_KEY")
    N2YO_BASE_URL: AnyUrl = Field("https://api.n2yo.com/rest/v1/satellite", env="N2YO_BASE_URL")

    # Mongo
    MONGO_URI: str = Field("mongodb://mongo:27017", env="MONGO_URI")
    MONGO_DB: str = Field("satellite_db", env="MONGO_DB")

    # Cache/Rates
    INMEMORY_CACHE_TTL_SEC: int = Field(60, env="INMEMORY_CACHE_TTL_SEC")     # short TTL for hot endpoints
    TLE_CACHE_TTL_SEC: int = Field(3600, env="TLE_CACHE_TTL_SEC")              # TLE is stable ~hours
    MAX_OUTBOUND_RPS: float = Field(5.0, env="MAX_OUTBOUND_RPS")               # soft limiter per-process

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
