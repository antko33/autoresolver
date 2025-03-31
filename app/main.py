import asyncio

import uvicorn
from fastapi import FastAPI

from app.config import API_PORT
from app.db import db_init
from app.routes import router

fastapi_app = FastAPI()
fastapi_app.include_router(router)


def main():
    asyncio.run(db_init())
    uvicorn.run(fastapi_app, host="0.0.0.0", port=API_PORT)


if __name__ == "__main__":
    main()
