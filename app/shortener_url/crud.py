from requests import session
import validators

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.shortener_url.models import Url, UrlCreate, UrlRead, User, UserCreate


class UrlCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UrlCreate):
        values = data.dict()
        url = values["url"]
        if not validators.url(url):
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
        statement = select(Url).where(Url.url == target_url)
        result = await self.session.execute(statement=statement)
        url = result.scalar_one_or_none()

        return url

    async def update_count(self, key: str):
        url = await self.get(key=key)
        url.count += 1
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url

    async def top_10(self):
        statement = select(Url).order_by(Url.count.desc()).limit(10)
        result = await self.session.execute(statement=statement)
        urls = result.all()
        return urls

    async def get_count(self):
        statement = select(Url.count)
        result = await self.session.execute(statement=statement)
        count = [el[0] for el in result.all()]
        return sum(count)


class UserCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate):
        values = data.dict()
        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def is_exist_user(self, ip, url_key):
        statement = select(User).where(User.url_key == url_key).where(User.ip == ip)
        result = await self.session.execute(statement=statement)
        user = result.scalar_one_or_none()

        return user
