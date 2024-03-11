from os import getenv

from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
from aiogram import Dispatcher
from redis.asyncio import Redis

load_dotenv(".env")

TOKEN = getenv("BOT_TOKEN")
redis = Redis()
dp = Dispatcher(storage=RedisStorage(redis))
