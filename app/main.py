import asyncio
import logging
import time

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from app.database import init_db
from app.routers import urls
from app.service.middleware import batch_processing_task, rate_limiter

fast = FastAPI()

origins = ["*"]

fast.add_middleware(CORSMiddleware,
                    allow_origins=origins,
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"]
                    )


# @fast.middleware("http")
# async def rate_limiter_middleware(request: Request, call_next):
#     return await rate_limiter(request, call_next)


@fast.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@fast.on_event("startup")
async def on_startup():
    await init_db()
    logging.info(msg='Initialized Databases')
    # asyncio.create_task(batch_processing_task())
    # print("Batch Processing Initialized")


@fast.on_event("shutdown")
def shutdown():
    logging.info(msg='Server Shutting down')


def openapi():
    if fast.openapi_schema:
        return fast.openapi_schema
    openapi_schema = get_openapi(
        title="Litely: URL shortener!",
        version="1.2.1",
        description="This is an API docs for URL shortner",
        routes=fast.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://verloop.io/wp-content/themes/verloop/images/VerloopLogo.svg"
    }
    fast.openapi_schema = openapi_schema
    return fast.openapi_schema


fast.openapi = openapi
from app.routers import users, redirection

fast.include_router(urls.router)
fast.include_router(users.router)
fast.include_router(redirection.router)
