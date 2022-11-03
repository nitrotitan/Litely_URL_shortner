from datetime import datetime

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_session
from app.models import URLInfo
from app.service.keygen import create_random_key

now = datetime.now()
current_date_time = now.strftime("%d/%m/%y %H:%M:%S")


async def db_create_url(url, session: AsyncSession = Depends(get_session)):
    query = URLInfo(target_url=url.target_url, key=create_random_key(), created_on=current_date_time,
                    is_active=True)
    return await save(query, session)


async def db_get_url_by_key(url_key, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(URLInfo).where(URLInfo.key == url_key))
    one_val = result.scalars().one()
    return one_val


async def db_deactivate_url(url_key, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(URLInfo).where(URLInfo.key == url_key))
    print("wtf", result)
    query = result.scalars().one()
    print("this is sparta", query)
    query.is_active = False
    return await save(query=query, session=session)


async def save(query, session: AsyncSession = Depends(get_session)):
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return 'Done'
