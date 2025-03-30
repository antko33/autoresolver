import asyncio

from app.db import db_init
from app.resolver import Resolver, load_dns, load_urls


async def main() -> None:
    await db_init()

    resolver = Resolver(await load_dns(), await load_urls())
    _ = await resolver.resolve_all()


if __name__ == "__main__":
    asyncio.run(main())
