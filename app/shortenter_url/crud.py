import validators

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shortenter_url.models import Url, UrlCreate, User, UserCreate


class UrlCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UrlCreate):
        values = data.dict()
        target_url = values["target_url"]
        if not validators.url(target_url):
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

    async def is_exist_url(self, target_url: str):
        statement = select(Url).where(Url.target_url == target_url)
        result = await self.session.execute(statement=statement)
        url = result.scalar_one_or_none()

        return url

    async def update_count(self, key: str):
        url = await self.get(key=key)
        url.key += 1
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url


class UserCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate):
        values = data.dict()
        user = User(**values)
        print(user)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def is_exist_user(self, ip, url_key):
        statement = (
            select(User).where(User.url_key == url_key).where(User.ip == ip)
        )
        result = await self.session.execute(statement=statement)
        user = result.scalar_one_or_none()

        return user