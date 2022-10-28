from fastapi import APIRouter

from app.shortener_url.api import router as url_app_router

api_router = APIRouter()

include_api = api_router.include_router

include_api(url_app_router)
