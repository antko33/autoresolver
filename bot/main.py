import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from bot.config import BOT_TOKEN

bot = Bot(BOT_TOKEN)
dispatcher = Dispatcher()


@dispatcher.message(Command("start"))
async def start(message: Message):
    await message.answer("Я пока не знаю, как реагировать на эту команду")


@dispatcher.message(Command("generate"))
async def generate(message: Message):
    await message.answer("Создаю таблицу")


async def main():
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
