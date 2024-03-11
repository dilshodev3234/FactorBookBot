import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.utils.i18n import FSMI18nMiddleware

from bot.dispatcher import TOKEN
from bot.handlers import *
from db import db

i18n = I18n(path='locales')


async def main() -> None:
    await db.create_all()
    bot = Bot(TOKEN)
    dp.update.middleware(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
