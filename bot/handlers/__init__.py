from aiogram import Router

from bot.handlers.private.start import start_router
from bot.handlers.private.books import book_router
from bot.handlers.private.language import langauge_router
from bot.handlers.private.order import order_router

private_router = Router(name='private')
private_router.include_routers(*[
    start_router,
    langauge_router,
    order_router,
    book_router
])