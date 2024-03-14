from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _
from db import Category, OrderItem, Book


async def categories_inline_btn(order_item: list[OrderItem] = None):
    categories: list[Category] = await Category.get_all()
    ikm = InlineKeyboardBuilder()
    if categories:
        ikm.add(*[
            InlineKeyboardButton(text=category.name, callback_data=f"{category.id}")
            for category in categories
        ])
    ikm.add(InlineKeyboardButton(text=_("Search 🔎"), switch_inline_query_current_chat=''))
    if order_item:
        ikm.add(InlineKeyboardButton(text=_("🛒 Cart ({0})").format(len(order_item)), callback_data="cart"))
    ikm.adjust(2)
    return ikm.as_markup()


async def books_inline_btn(books: list[Book], order_items: list[OrderItem]):
    ikm = InlineKeyboardBuilder()
    if books:
        ikm.add(*[
            InlineKeyboardButton(text=book.title, callback_data=f"{book.id}")
            for book in books
        ])
    if order_items:
        ikm.add(InlineKeyboardButton(text=_("🛒 Cart ({0})").format(len(order_items)), callback_data="cart"))
    ikm.add(InlineKeyboardButton(text=_("◀ Back"), callback_data="back"))
    ikm.adjust(2)
    return ikm.as_markup()


async def product_order_inline_btn(count):
    ikm = InlineKeyboardBuilder()
    ikm.add(*[
        InlineKeyboardButton(text="➖", callback_data="-"),
        InlineKeyboardButton(text=f"{count}", callback_data="count"),
        InlineKeyboardButton(text=f"➕", callback_data="+"),
        InlineKeyboardButton(text=_("◀ Back"), callback_data="back"),
        InlineKeyboardButton(text="🛒 Add to Cart", callback_data="cart"),
    ])
    ikm.adjust(3, 2)
    return ikm.as_markup()


async def order_inline_btn():
    ikm = InlineKeyboardBuilder()
    ikm.add(*[
        InlineKeyboardButton(text=_("❌ Clear the basket"), callback_data="❌"),
        InlineKeyboardButton(text=f"✅ Order confirmation", callback_data="✅"),
        InlineKeyboardButton(text=_("◀ Back"), callback_data="back"),
    ])
    ikm.adjust(1)
    return ikm.as_markup()
