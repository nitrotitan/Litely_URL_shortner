import logging

import uvicorn

from manage import migrate, upgrade
from .controller.api import app
from .database import init_db


@app.on_event("startup")
async def on_startup():
    migrate()
    upgrade()
    await init_db()


@app.on_event("shutdown")
async def shutdown():
    logging.info(msg='Server Shutting down')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)