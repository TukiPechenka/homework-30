from sqlalchemy.ext import asyncio
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite+aiosqlite:///./app.py.db"

engine = asyncio.create_async_engine(DATABASE_URL, echo=True)
# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = asyncio.async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=asyncio.AsyncSession,
)
session = async_session()
Base = declarative_base()
