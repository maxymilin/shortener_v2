from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.shortener_url.crud import UrlCRUD, UserCRUD


async def get_url_crud(session: AsyncSession = Depends(get_async_session)):
    return UrlCRUD(session=session)


async def get_user_crud(session: AsyncSession = Depends(get_async_session)):
    return UserCRUD(session=session)
