import asyncio
import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.i18n import FSMI18nMiddleware, I18n
from redis.asyncio import Redis

from bot.handlers import private_router
from config import conf
from db import database

redis = Redis(db=conf.rd.DB, host=conf.rd.HOST, port=conf.rd.PORT)
dp = Dispatcher(storage=RedisStorage(redis))

i18n = I18n(path='../locales')


async def register_all_handlers():
    dp.include_routers(*[
        private_router
    ])


async def register_all_middlewares():
    dp.update.middleware(FSMI18nMiddleware(i18n))


async def main() -> None:
    await database.create_all()
    await register_all_handlers()
    await register_all_middlewares()

    bot = Bot(conf.bot.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
