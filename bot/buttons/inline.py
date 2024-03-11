from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from db import Category


async def categories_inline_btn():
    categories: list[Category] = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories:
        ikm.add(*[
            InlineKeyboardButton(text = category.name , callback_data=f"{category.id}")
            for category in categories
        ])
    ikm.add(InlineKeyboardButton(text='<-Back', callback_data="back"))
    ikm.add(InlineKeyboardButton(text=_("Search 🔎"), switch_inline_query_current_chat=''))
    ikm.adjust(2)
    return ikm.as_markup()




