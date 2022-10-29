import random
import string

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi import status as http_status
from typing import List

from urllib.parse import urljoin

from app.shortener_url.crud import UrlCRUD, UserCRUD
from app.shortener_url.dependencies import get_url_crud, get_user_crud
from app.shortener_url.models import Url, UrlBase, UrlKey, UrlRead, User

router = APIRouter()


async def create_key() -> str:
    """Creating a random string from ASCII letters and digits 8 characters long.

    Parameters:
    -----------
    None
    Return:
    -------
    key: str
        random string.
    """

    key = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    return key

@router.post(
    "/shorten_url", response_model=UrlKey, status_code=http_status.HTTP_201_CREATED
)
async def create_url(
    data: UrlBase,
    request: Request,
    urls: UrlCRUD = Depends(get_url_crud),
    users: UserCRUD = Depends(get_user_crud),
) -> UrlKey:
    """Create a shortener version of the URL. Check if is there data
    in the database. If not create a new record.
    Returns response with shortener URL.

    Parameters:
    -----------
    data: UrlBase
        contains the URL that needed to be shortened.
    request: Request
        request from the user. Used to get user IP address.
    urls: UrlCRUD
        organizes the connection between the session and the "urls" table.
    users: UserCRUD
        organizes the connection between the session and the "users" table.
    Return:
    -------
    url: UrlKey
        respond contains a link to the shortener URL.
    """

    # Get URL from application
    app_url = str(request.url)
    # Get user IP from request
    user_ip = request.client.host
    target_url = data.url
    # Check if there URL in the "urls" table
    url = await urls.is_exist_url(target_url=target_url)
    if url:
        key_url = url.key
        # Check if user shorted the URL erlier
        user = await users.is_exist_user(ip=user_ip, url_key=key_url)
        if not user:
            # If new user create new user and update count of shortener URL
            user = User(ip=user_ip, url_key=key_url)
            await users.create(user)
            await urls.update_count(key_url)
    else:
        key = await create_key()
        data = Url(url=target_url, key=key)
        url = await urls.create(data=data)
        user = User(ip=user_ip, url_key=key)
        await users.create(user)

    # Create a nice respose
    url = UrlKey(shortened_url=urljoin(app_url, url.key))
    return url


@router.get("/count", status_code=http_status.HTTP_200_OK)
async def get_count(urls: UrlCRUD = Depends(get_url_crud)) -> dict:
    """Get a number of calls for all shortener URLs.

    Parameters:
    -----------
    urls: UrlCRUD
        organizes the connection between the session and the "urls" table.
    Return:
    -------
    response: dict
        dict with count calls.
    """
    count = await urls.get_count()
    response = {"calls": count}
    return response


@router.get("/top_10", status_code=http_status.HTTP_200_OK)
async def get_top_10(urls: UrlCRUD = Depends(get_url_crud)) -> List[Url]:
    """ Return the list of the 10 most shortened urls.

    Parameters:
    -----------
    urls: UrlCRUD
        organizes the connection between the session and the "urls" table.
    Return:
    -------
    response: List
        list of the 10 most shortened urls.
    """
    response = await urls.top_10()
    return response


@router.get("/{key}", status_code=http_status.HTTP_301_MOVED_PERMANENTLY)
async def get_url(
    key: str,
    urls: UrlCRUD = Depends(get_url_crud)
) -> RedirectResponse:
    """ Redirect to the target URL.

    Parameters:
    -----------
    urls: UrlCRUD
        organizes the connection between the session and the "urls" table.
    """
    url = await urls.get(key=key)

    return RedirectResponse(url.url, status_code=301)
