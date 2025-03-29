import asyncio

from app.db import db_init


async def main() -> None:
    await db_init()


if __name__ == "__main__":
    asyncio.run(main())
