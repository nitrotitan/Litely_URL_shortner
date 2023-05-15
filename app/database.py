import logging

import sqlalchemy.engine.url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import get_settings


def create_db_url():
    return sqlalchemy.engine.url.URL.create(drivername=get_settings().db_driver,
                                            username=get_settings().db_user,
                                            password=get_settings().db_pass,
                                            host=get_settings().instance_host,
                                            port=get_settings().db_port,
                                            database=get_settings().db_name,
                                            query={})


engine = create_async_engine(create_db_url(), echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def async_session_generator():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception as e:
        await session.rollback()
        print("Error in Creating Async Session {}".format(e))
    finally:
        await session.close()
