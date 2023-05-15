import logging
from typing import List

import validators
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app import models
from app.database import get_session
from app.exceptions import raise_bad_request, raise_url_not_found, raise_key_not_found
from app.models import URLBase, URLKey
from app.service.crud import (
    db_create_url,
    db_get_url_by_key,
    db_deactivate_url,
    db_reactivate_url,
    db_get_all_url,
)

router = APIRouter(prefix="/0", tags=['URLInfo'])


@router.get("/", status_code=status.HTTP_401_UNAUTHORIZED, response_class=HTMLResponse,
            summary='Ping this to see if it\'s hosted')
def read_root():
    html = """
        <!DOCTYPE html>
        <html>
        <body>
        <h1>Unauthorized 401</h1>
        <p>You seem lost. Why don't you take a coffee break?</p>
        </body>
        </html>
    """
    return HTMLResponse(content=html, status_code=status.HTTP_401_UNAUTHORIZED)


@router.post("/create-url/", status_code=status.HTTP_201_CREATED, summary='Create new key',
             response_model=URLKey)
async def create_url(url: models.URLTarget, session: AsyncSession = Depends(get_session)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")

    try:
        url_key = await db_create_url(url=url, session=session)
    except Exception as e:
        logging.error("Error occurred during URL creation: {}".format(e), exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return URLKey(key=url_key)


@router.get("/peek-url/{url_key}", response_model=URLBase, summary='See description of Keys')
async def peek(url_key, request: Request, session: AsyncSession = Depends(get_session)):
    result = await db_get_url_by_key(url_key, session)
    if not result:
        return raise_url_not_found(request)
    return URLBase(
        target_url=result.target_url,
        created_on=result.created_on,
        is_active=result.is_active,
        key=result.key,
    )


@router.get("/get-all-records/", response_model=List[URLBase], summary='Shows all the key in DB')
async def get_all_url(session: AsyncSession = Depends(get_session)):
    results = await db_get_all_url(session=session)
    return [
        URLBase(
            target_url=result.target_url,
            key=result.key,
            created_on=result.created_on,
            is_active=result.is_active,
        )
        for result in results
    ]


@router.delete("/delete_url/{url_key}", status_code=status.HTTP_200_OK, summary='Deactivates URL key')
async def delete_url_key_binding(url_key, session: AsyncSession = Depends(get_session)):
    result = await db_deactivate_url(url_key, session)
    if not result:
        return raise_key_not_found(key=url_key)
    if result == 'Already Deactivated':
        resp = {"status": {"key": url_key, "msg": "Already Deactivated!"}}
    else:
        resp = {"status": {"key": url_key, "msg": "Deactivated successfully!"}}
    return resp


@router.put('/reactivate_url/{url_key}', status_code=status.HTTP_200_OK, summary='Deactivates URL key',
            )
async def react_url_key_binding(url_key, session: AsyncSession = Depends(get_session)):
    # url_key = url_key[::-1]
    result = await db_reactivate_url(url_key, session)
    if not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if result == 'Already Activated':
        resp = {"status": {"key": "{}".format(url_key), "msg": "Already Activated!"}}
        return resp
    else:
        resp = {"status": {"key": "{}".format(url_key), "msg": "Activated successfully!"}}
        return resp
