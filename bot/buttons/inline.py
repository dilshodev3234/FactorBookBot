from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from db import Category, Network


async def categories_inline_btn():
    categories: list[Category] = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories:
        ikm.add(*[
            InlineKeyboardButton(text=category.name, callback_data=f"{category.id}")
            for category in categories
        ])
    ikm.add(InlineKeyboardButton(text='<-Back', callback_data="back"))
    ikm.add(InlineKeyboardButton(text=_("Search 🔎"), switch_inline_query_current_chat=''))
    ikm.adjust(2)
    return ikm.as_markup()


async def book_list_inline_btn():
    network_list: list[Network] = await Network.get_all()
    ikm = InlineKeyboardBuilder()
    if network_list:
        ikm.add(*[
            InlineKeyboardButton(text=net.title, callback_data=f"{net.id}", url=net.link)
            for net in network_list
        ])
    ikm.adjust(1)
    return ikm.as_markup()
