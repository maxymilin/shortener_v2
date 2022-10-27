from typing import Optional

from sqlmodel import Field, SQLModel


class UrlBase(SQLModel):
    target_url: str


class Url(SQLModel, table=True):
    __tablename__ = "urls"

    target_url: str
    key: str = Field(primary_key=True)
    count: int = Field(default=1)

    class Config:
        orm_mode = True


class UrlCreate(Url):
    ...


class UrlRead(Url):
    ...


class UrlKey(SQLModel):
    key: str


class UrlRedirerect(SQLModel):
    url: str


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    ip: str

    url_key: Optional[str] = Field(default=None, foreign_key="urls.key")

    class Config:
        orm_mode = True


class UserCreate(User):
    ...
