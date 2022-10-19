import validators

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shortenter_url.models import Url, UrlCreate


class UrlCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UrlCreate):
        values = data.dict()

        if not validators.url(values["target_url"]):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid url."
            )

        url = Url(**values)
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url

    async def get(self, key: str):
        statement = select(Url).where(Url.key == key)
        result = await self.session.execute(statement=statement)
        url = result.scalar_one_or_none()

        if url is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, detail="Invalid short url."
            )
        return url
