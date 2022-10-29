from typing import Optional

from sqlmodel import Field, SQLModel


class UrlBase(SQLModel):
    """Base URL model for getting data from user."""

    url: str


class Url(UrlBase, table=True):
    """URL model for creating a record in table "urls".

    Parameters:
    -----------
    url: str
        url from other webstie;
    key: str, primary key
        shorter version URL, generated randomly from ASCII
        letters and digits with length 8 characters. Primary key;
    count: int
        show the number of calls from a user with a unique
        IP address.

    Return:
    -------
    None
    """

    __tablename__ = "urls"

    key: str = Field(primary_key=True)
    count: int = Field(default=1)

    class Config:
        orm_mode = True


class UrlCreate(Url):
    """URL model for creating."""

    ...


class UrlRead(Url):
    """Url model for reading."""

    ...


class UrlKey(SQLModel):
    """URL model that used to make a nice return shortened URL to the user.

    Parameters:
    -----------
    shortened_url: str
        link what redirect to the full version of web page.

    Retrun:
    -------
    None
    """

    shortened_url: str


class User(SQLModel, table=True):
    """User model for creating a record in table "users".

    Parameters:
    -----------
    id: int, primary key
        user id;
    ip: str
        user IP address;
    url_key: str, foreign key
        link from "urls" table.

    Return:
    -------
    None
    """

    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    ip: str

    url_key: Optional[str] = Field(default=None, foreign_key="urls.key")

    class Config:
        orm_mode = True


class UserCreate(User):
    """User create model."""

    ...
