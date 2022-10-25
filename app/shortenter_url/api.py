import random
import string

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi import status as http_status

from app.shortenter_url.crud import UrlCRUD, UserCRUD
from app.shortenter_url.dependencies import get_url_crud, get_user_crud
from app.shortenter_url.models import Url, UrlBase, UrlKey, User

router = APIRouter()


async def create_key():
    return "".join(random.choices(string.ascii_letters, k=5))


@router.post("", response_model=UrlKey, status_code=http_status.HTTP_201_CREATED)
async def create_url(
    data: UrlBase,
    request: Request,
    urls: UrlCRUD = Depends(get_url_crud),
    users: UserCRUD = Depends(get_user_crud)
):
    user_ip = request.client.host
    target_url = data.target_url
    url = await urls.is_exist_url(target_url=target_url)
    if url:
        print("find Url!!!")
        key_url = url.key
        user = await users.is_exist_user(ip=user_ip, url_key=key_url)
        if not user:
            user = User(ip=user_ip, url_key=key_url)
            await users.create(user)
            await urls.update_count(url)
            return key_url
    else:
        key = await create_key()
        data = Url(target_url=data.target_url, key=key)
        url = await urls.create(data=data)
        user = User(ip=user_ip, url_key=key)
        await users.create(user)

    key_url = UrlKey(key=url.key)

    return key_url


@router.get("/{key}", status_code=http_status.HTTP_301_MOVED_PERMANENTLY)
async def get_url(key: str, urls: UrlCRUD = Depends(get_url_crud)):
    url = await urls.get(key=key)

    return RedirectResponse(url.target_url, status_code=301)
