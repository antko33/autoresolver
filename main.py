import asyncio
import os

from dotenv import load_dotenv

from app.db import db_close, db_init
from app.resolver import Resolver, load_dns, load_urls, save_to_file
from bot.bot import Bot


async def main() -> None:
    load_dotenv()
    bot_token = os.getenv("BOT_TOKEN")
    user_id = os.getenv("USER_ID")

    await db_init()

    resolver = Resolver(await load_dns(), await load_urls())
    ips = await resolver.resolve_all()
    result_file = save_to_file(ips)

    if result_file.strip():
        bot = Bot(bot_token)
        await bot.send_file(user_id, result_file)

    await db_close()


if __name__ == "__main__":
    asyncio.run(main())
