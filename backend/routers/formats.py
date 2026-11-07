from fastapi import APIRouter
from utils.file_detector import get_supported_formats

router = APIRouter()

@router.get("/formats")
async def get_formats():
    return get_supported_formats()
