import logging

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from .database import init_db
from .routers import urls
from .routers import users, redirection

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"]
                   )

app.include_router(urls.router)
app.include_router(users.router)
app.include_router(redirection.router)

@app.on_event("startup")
async def on_startup():
    await init_db()
    # redis = create_redis_pool()
    # await FastAPILimiter.init(redis)
    logging.info(msg='Initialized Databases')


@app.on_event("shutdown")
async def shutdown():
    logging.info(msg='Server Shutting down')


def openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Litely: URL shortener!",
        version="1.2.1",
        description="This is an API docs for URL shortner",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://verloop.io/wp-content/themes/verloop/images/VerloopLogo.svg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = openapi
