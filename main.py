import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.utils.i18n import FSMI18nMiddleware

from bot.handlers import *
from db import db
from config import conf
i18n = I18n(path='locales')


async def main() -> None:
    await db.create_all()
    bot = Bot(conf.bot.BOT_TOKEN)
    dp.update.middleware(FSMI18nMiddleware(i18n))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
