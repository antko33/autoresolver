import asyncio

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import API_URL, BOT_TOKEN

bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher()


@dispatcher.message(Command("start"))
async def start(message: Message):
    await message.answer("Я пока не знаю, как реагировать на эту команду")


@dispatcher.message(Command("generate"))
async def generate(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/generate_table") as resp:
            if resp.status == 200:
                await message.answer("Создаю таблицу. Это может занять несколько минут")
            else:
                await message.answer("Ошибка генерации 😓")


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
