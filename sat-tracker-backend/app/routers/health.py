from fastapi import APIRouter
from app.models.schemas import APIMessage

router = APIRouter()

@router.get("/health", response_model=APIMessage)
async def health():
    return APIMessage(message="ok")
