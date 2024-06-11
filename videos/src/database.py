from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

from .config import settings
from .constants import DB_NAMING_CONVENTION


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
    pass


if settings.MODE == "TEST":
    ASYNC_DATABASE_URL = settings.ASYNC_TEST_DATABASE_URL
    SYNC_DATABASE_URL = settings.SYNC_TEST_DATABASE_URL
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    ASYNC_DATABASE_URL = settings.ASYNC_DATABASE_URL
    SYNC_DATABASE_URL = settings.SYNC_DATABASE_URL
    DATABASE_PARAMS = {}

async_engine = create_async_engine(ASYNC_DATABASE_URL, **DATABASE_PARAMS)

async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)

sync_engine = create_engine(SYNC_DATABASE_URL, **DATABASE_PARAMS)

sync_session_maker = sessionmaker(sync_engine, expire_on_commit=False)
