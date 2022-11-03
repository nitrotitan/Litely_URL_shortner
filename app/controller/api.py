import json
import logging

import validators
from fastapi import Depends, HTTPException, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse, HTMLResponse

from app import models
from app.database import get_session
from app.models import URLBase
from app.service.crud import db_create_url, db_get_url_by_key, db_deactivate_url
from exceptions import raise_bad_request

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )


@app.get("/", status_code=status.HTTP_401_UNAUTHORIZED, response_class=HTMLResponse)
def read_root():
    html = """<!DOCTYPE html>
<html>
<body>
<h1>Unauthorized 401</h1>
<p>Why don't you take a coffee break?</p>
</body>
</html>"""
    return html


@app.post("/create-url/", status_code=status.HTTP_201_CREATED)
async def create_url(url: models.URLTarget, session: AsyncSession = Depends(get_session)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    try:
        await db_create_url(url=url, session=session)
    except:
        logging.error("ran into error  ", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    resp = {"status": "Created Successfully"}
    return json.dumps(resp, indent=1)


@app.get("/peek-url/{url_key}", status_code=status.HTTP_200_OK, response_model=URLBase)
async def peek(url_key, session: AsyncSession = Depends(get_session)):
    result = await db_get_url_by_key(url_key, session)
    if not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return result


@app.get("/{url_key}", status_code=status.HTTP_302_FOUND, response_class=RedirectResponse)
async def forward_to_destination(url_key, session: AsyncSession = Depends(get_session)):
    result = await db_get_url_by_key(url_key, session)
    if not result.is_active or not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return result.target_url


@app.delete("/delete_url/{url_key}", status_code=status.HTTP_200_OK)
async def delete_url_key_binding(url_key, session: AsyncSession = Depends(get_session)):
    url_key = url_key[::-1]
    result = await db_deactivate_url(url_key, session)
    if not result:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        resp = {"status": "Deactivated Successfully"}
        return json.dumps(resp, indent=1)
