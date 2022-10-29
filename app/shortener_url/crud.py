import validators

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional

from app.shortener_url.models import Url, UrlCreate, User, UserCreate


class UrlCRUD:
    """Fuctionality class for the "urls" table in database."""

    def __init__(self, session: AsyncSession):
        """Initialize the session and use it to connect to the database."""
        self.session = session

    async def create(self, data: UrlCreate) -> Url:
        """Create a new record in "urls" table.

        Parameters:
        -----------
        data: UrlCreate
            URL model for creation record in the "urls" table.
            Contains URL from a target website, random key
            and count of calls from different users.
        Return:
        -------
        url : Url
            returns created record from the "urls" table.
        """

        values = data.dict()
        url = values["url"]
        # if URL don't pass validation throws an error
        if not validators.url(url):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST, detail="Invalid url."
            )
        # Unpacking data from the model adding to the table, committing
        # and refreshing
        url = Url(**values)
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url

    async def get(self, key: str) -> Url:
        """Get URL record from the "url" table.

        Parameters:
        ----------
        key: str
            a string of 8 chars in length. The primary key for the table.
        Return:
        -------
        url: Url
            record from the "urls" table.
        """
        statement = select(Url).where(Url.key == key)
        result = await self.session.execute(statement=statement)
        url = result.scalar_one_or_none()

        # if no record in the table throw error
        if url is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND, detail="Invalid short url."
            )

        return url

    async def is_exist_url(self, target_url: str) -> Optional[Url]:
        """Search in the table "urls" is there a saved URL.

        Parameters:
        -----------
        target_url: str
            URL from another website.
        Return:
        -------
        url: Url or None
            If there is a record in the table the method returns this record,
            else returns None.
        """

        statement = select(Url).where(Url.url == target_url)
        result = await self.session.execute(statement=statement)
        url = result.scalar_one_or_none()

        return url

    async def update_count(self, key: str) -> Url:
        """Update calls count from different users.

        Parameters:
        -----------
        key: str
            a string of 8 chars in length. The primary key for the table.
        Return:
        -------
        url: Url
            record from the "urls" table.
        """
        url = await self.get(key=key)
        url.count += 1
        self.session.add(url)
        await self.session.commit()
        await self.session.refresh(url)

        return url

    async def top_10(self) -> List[Url]:
        """Return sorted list of 10 most shortered Url from the "urls" table.

        Parametrs:
        ----------
        None
        Return:
        -------
        url: List[Url]
            list of top 10 most shortered urls.
        """
        statement = select(Url).order_by(Url.count.desc()).limit(10)
        result = await self.session.execute(statement=statement)
        urls = result.all()
        return urls

    async def get_count(self) -> int:
        """Return count of shotered urls from unic users.

        Parameters:
        -----------
        None
        Return:
        -------
        count: int
            Sum of all count records in the "urls" table.
        """
        statement = select(Url.count)
        result = await self.session.execute(statement=statement)
        count = sum([el[0] for el in result.all()])
        return count


class UserCRUD:
    """Fuctionality class for the "users" in the database."""

    def __init__(self, session: AsyncSession):
        """Initialize the session and use it to connect to the database."""

        self.session = session

    async def create(self, data: UserCreate) -> User:
        """Create a new record in the "users" table.

        Parameters:
        -----------
        data: UserCreate
            contains user id, ip and key from the "urls" table.
        Return:
        -------
        user: User
            record from the "users" table.
        """
        values = data.dict()
        # Unpacking data from the model adding to the table, committing
        # and refreshing
        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def is_exist_user(self, ip: str, url_key: str) -> Optional[User]:
        """Cheking if there are a user in the "users" table.
        If user early created the shorten version of URL return user,
        else returns None.
        Parameters:
        -----------
        ip: str
            the user IP address.
        url_key: str
            the shortener version of URL.
        Retrun:
        -------
        user: Optional[User]
            return user record from the "users" table if there is a record,
            if not - return None.
        """
        statement = select(User).where(User.url_key == url_key).where(User.ip == ip)
        result = await self.session.execute(statement=statement)
        user = result.scalar_one_or_none()

        return user
