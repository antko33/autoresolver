import aiogram
from aiogram.types import FSInputFile


class Bot:

    def __init__(self, token):
        self.__bot = aiogram.Bot(token)

    async def send_file(self, user, filepath):
        file = FSInputFile(filepath)
        await self.__bot.send_document(chat_id=user, document=file)
        await self.__bot.session.close()
