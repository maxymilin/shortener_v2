from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel
from tomlkit import table


class UrlBase(SQLModel):
    target_url: str

class Url(SQLModel, table=True):
    __tablename__ = "urls"

    target_url: str
    key: str = Field(primary_key=True)

class UrlCreate(Url):
    ...


class UrlRead(Url):
    ...


class UrlKey(SQLModel):
    key: str


class UrlRedirerect(SQLModel):
    url: str
