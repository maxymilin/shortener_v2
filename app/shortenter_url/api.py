import random
import string

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi import status as http_status

from app.shortenter_url.crud import UrlCRUD
from app.shortenter_url.dependencies import get_url_crud
from app.shortenter_url.models import Url, UrlBase, UrlKey, UrlRedirerect


router = APIRouter()


def create_key():
    return "".join(random.choices(string.ascii_letters, k=5))


@router.post("", response_model=UrlKey, status_code=http_status.HTTP_201_CREATED)
async def create_url(data: UrlBase, urls: UrlCRUD = Depends(get_url_crud)):
    data = Url(
        target_url = data.target_url,
        key = create_key()
    )
    url = await urls.create(data=data)
    key_url = UrlKey(key=url.key)

    return key_url


@router.get("/{key}", status_code=http_status.HTTP_301_MOVED_PERMANENTLY)
async def get_url(key: str, urls: UrlCRUD = Depends(get_url_crud)):
    url = await urls.get(key=key)

    return RedirectResponse(url.target_url, status_code=301)
