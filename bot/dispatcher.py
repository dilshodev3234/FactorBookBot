from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis
from config import conf

redis = Redis(
    db=conf.rd.DB,
    host=conf.rd.HOST,
    port=conf.rd.PORT,
)
dp = Dispatcher(storage=RedisStorage(redis))
