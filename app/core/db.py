from sys import modules

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from app import settings


db_connection_str = settings.db_async_connection_str
if "pytest" in modules:
    db_connection_str = settings.db_async_test_connection_str


# Create a SQLAlchemy engine to be able to connect to the database.
async_engine = create_async_engine(
    db_connection_str, echo=True, future=True, pool_size=40
)


async def get_async_session() -> AsyncSession:
    """Use the asyncpg driver to pass a database session to a handler.
    In future you can use the Depends approach for Sharing of database
    connections.
    """
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
