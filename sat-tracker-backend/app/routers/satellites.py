from fastapi import APIRouter, Query
from app.models.schemas import TLEResponse, GenericN2YOResponse
from app.services import satellite_service as svc

router = APIRouter(prefix="/satellites", tags=["satellites"])

@router.get("/{norad_id}/tle", response_model=GenericN2YOResponse)
async def tle(norad_id: int):
    data = await svc.get_tle(norad_id)
    return data

@router.get("/{norad_id}/positions", response_model=GenericN2YOResponse)
async def positions(
    norad_id: int,
    lat: float = Query(..., description="Observer latitude"),
    lng: float = Query(..., description="Observer longitude"),
    alt: float = Query(..., description="Observer altitude (meters)"),
    seconds: int = Query(..., gt=0, le=3600, description="Number of seconds of prediction")
):
    return await svc.get_positions(norad_id, lat, lng, alt, seconds)

@router.get("/{norad_id}/visualpasses", response_model=GenericN2YOResponse)
async def visual_passes(
    norad_id: int,
    lat: float,
    lng: float,
    alt: float,
    days: int = Query(..., gt=0, le=10),
    min_visibility: int = Query(0, ge=0, le=3600)
):
    return await svc.get_visual_passes(norad_id, lat, lng, alt, days, min_visibility)

@router.get("/{norad_id}/radiopasses", response_model=GenericN2YOResponse)
async def radio_passes(
    norad_id: int,
    lat: float,
    lng: float,
    alt: float,
    days: int = Query(..., gt=0, le=10),
):
    return await svc.get_radio_passes(norad_id, lat, lng, alt, days)

@router.get("/above", response_model=GenericN2YOResponse)
async def above(
    lat: float,
    lng: float,
    alt: float,
    radius: int = Query(..., gt=0, le=90),
    category_id: int = Query(0, ge=0)
):
    return await svc.get_above(lat, lng, alt, radius, category_id)
