import logging

from manage import migrate
from .controller.api import app
from .database import init_db

@app.on_event("startup")
async def on_startup():
    await init_db()
    migrate()


@app.on_event("shutdown")
async def shutdown():
    logging.info(msg='Server Shutting down')

