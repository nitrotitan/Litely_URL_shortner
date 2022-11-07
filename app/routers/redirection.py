from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.database import get_session
from app.service.crud import db_get_url_by_key
from app.exceptions import raise_url_not_found

router = APIRouter(tags=['Redirection'])


@router.get("/{url_key}", status_code=status.HTTP_302_FOUND, response_class=RedirectResponse,
            summary='Redirects to url')
async def forward_to_destination(url_key, request: Request, session: AsyncSession = Depends(get_session)):
    result = await db_get_url_by_key(url_key, session)
    print(result)
    if result is not None:
        if not result.is_active:
            raise raise_url_not_found(request)
        else:

            return result.target_url
    raise raise_url_not_found(request)
