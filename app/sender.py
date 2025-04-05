import os

import aiohttp

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")


async def send_file_to_user(filepath: str):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(filepath, "rb") as file:
        data = aiohttp.FormData()
        data.add_field("chat_id", USER_ID)
        data.add_field("document", file, filename=os.path.basename(filepath))

        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                if resp.status == 200:
                    os.remove(filepath)
