import random
import string

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi import status as http_status

from urllib.parse import urljoin

from app.shortener_url.crud import UrlCRUD, UserCRUD
from app.shortener_url.dependencies import get_url_crud, get_user_crud
from app.shortener_url.models import Url, UrlBase, UrlKey, UrlRead, User

router = APIRouter()


async def create_key():
    return "".join(random.choices(string.ascii_letters+string.digits, k=8))


@router.post("/shorten_url", response_model=UrlKey, status_code=http_status.HTTP_201_CREATED)
async def create_url(
    data: UrlBase,
    request: Request,
    urls: UrlCRUD = Depends(get_url_crud),
    users: UserCRUD = Depends(get_user_crud),
):
    app_url = urljoin(str(request.url), "/url")
    print(app_url)
    user_ip = request.client.host
    target_url = data.url
    url = await urls.is_exist_url(target_url=target_url)
    if url:
        key_url = url.key
        user = await users.is_exist_user(ip=user_ip, url_key=key_url)
        if not user:
            user = User(ip=user_ip, url_key=key_url)
            await users.create(user)
            await urls.update_count(key_url)
    else:
        key = await create_key()
        data = Url(url=target_url, key=key)
        url = await urls.create(data=data)
        user = User(ip=user_ip, url_key=key)
        await users.create(user)

    url = UrlKey(shortened_url=urljoin(app_url, url.key))
    return url


@router.get("/count", status_code=http_status.HTTP_200_OK)
async def get_count(urls: UrlCRUD = Depends(get_url_crud)):
    count = await urls.get_count()

    return {"Calls": count}


@router.get("/top_10", status_code=http_status.HTTP_200_OK)
async def get_top_10(urls: UrlCRUD = Depends(get_url_crud)):
    return await urls.top_10()


@router.get("/{key}", status_code=http_status.HTTP_301_MOVED_PERMANENTLY)
async def get_url(key: str, urls: UrlCRUD = Depends(get_url_crud)):
    url = await urls.get(key=key)

    return RedirectResponse(url.url, status_code=301)
