from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.shortenter_url.crud import UrlCRUD


async def get_url_crud(session: AsyncSession = Depends(get_async_session)):
    return UrlCRUD(session=session)
