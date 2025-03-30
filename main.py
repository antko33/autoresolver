import asyncio

from app.db import db_close, db_init
from app.resolver import Resolver, load_dns, load_urls, save_to_file


async def main() -> None:
    await db_init()

    resolver = Resolver(await load_dns(), await load_urls())
    ips = await resolver.resolve_all()
    save_to_file(ips)

    await db_close()


if __name__ == "__main__":
    asyncio.run(main())
