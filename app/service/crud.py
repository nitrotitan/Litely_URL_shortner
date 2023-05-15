from datetime import datetime
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_session
from app.models import URLInfo
from app.service.keygen import generate_key

now = datetime.now()
current_date_time = now.strftime("%d/%m/%y %H:%M:%S")


async def db_create_url(url, session: AsyncSession = Depends(get_session)):
    deterministic_key = generate_key(url)
    query = await session.execute(select(URLInfo).where(URLInfo.key == deterministic_key))
    try:
        result = query.scalars().one()

    except SQLAlchemyError:
        return None

    if query:
        return result.key
    else:
        query = URLInfo(target_url=url.target_url, key=deterministic_key, created_on=current_date_time,
                        is_active=True)
    result = await save(query, session)
    if result:
        return result.key
    else:
        raise ConnectionError


async def db_get_url_by_key(url_key, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(URLInfo).where(URLInfo.key == url_key))
    try:
        result = query.scalars().one()
    except SQLAlchemyError:
        return None
    return result


async def db_get_all_url(session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(URLInfo))
    try:
        results = query.scalars().all()
    except SQLAlchemyError:
        return None
    return results


async def db_deactivate_url(url_key, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(URLInfo).where(URLInfo.key == url_key))
    try:
        result = query.scalars().one()
    except SQLAlchemyError:
        return None
    if not result.is_active:
        return 'Already Deactivated'
    result.is_active = False

    return await save(query=result, session=session)


async def db_reactivate_url(url_key, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(URLInfo).where(URLInfo.key == url_key))
    try:
        result = query.scalars().one()

    except SQLAlchemyError:
        return None
    if result.is_active:
        return 'Already Activated'
    result.is_active = True
    return await save(query=result, session=session)


async def save(query, session: AsyncSession = Depends(get_session)):
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query
