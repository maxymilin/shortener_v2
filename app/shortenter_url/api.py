from fastapi import APIRouter, Depends
from fastapi import status as http_status

from app.shortenter_url.crud import UrlCRUD
from app.shortenter_url.dependencies import get_url_crud
from app.shortenter_url.models import UrlCreate, UrlRead


router = APIRouter()


@router.post("", response_model=UrlRead, status_code=http_status.HTTP_201_CREATED)
async def create_url(data: UrlCreate, urls: UrlCRUD = Depends(get_url_crud)):
    url = await urls.create(data=data)

    return url.key


@router.get("/{key}", response_model=UrlRead, status_code=http_status.HTTP_200_OK)
async def get_url(key: str, urls: UrlCRUD = Depends(get_url_crud)):
    url = await urls.get(key=key)

    return url
