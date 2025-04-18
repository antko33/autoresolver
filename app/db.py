from tortoise import Tortoise

from app.config import TORTOISE_ORM


async def db_init() -> None:
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def db_close() -> None:
    await Tortoise.close_connections()
