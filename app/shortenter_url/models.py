import random
import string

from typing import Optional

from sqlalchemy import Column
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel
from tomlkit import table


class UrlBase(SQLModel):
    key: Optional[str] = Field(
        default="".join(random.choices(string.ascii_letters, k=5)),
        primary_key=True
    )
    target_url: str



class Url(UrlBase, table=True):
    __tablename__ = "urls"


class UrlCreate(UrlBase):
    ...


class UrlRead(UrlBase):
    ...
