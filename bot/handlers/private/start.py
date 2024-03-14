from typing import Optional

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, LabeledPrice, \
    PreCheckoutQuery, SuccessfulPayment
from aiogram.utils.i18n import gettext as _, I18n
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.reply import language_btn, main_menu_btn
from bot.filters.command import Command
from bot.states.main import ButtonState, UserState
from db import User, Book
from config import conf

# @dp.message()
# async def command_start_handler(message: Message, state: FSMContext) -> None:
#     if message.successful_payment:
#         print(message.successful_payment.order_info)
#         print(message.successful_payment.total_amount)
#         print(message.successful_payment.invoice_payload)  # TODO update order status to confirm
#         print('Tolandi!')
#     else:
#
#         prices = [
#             LabeledPrice(label='product narxi', amount=100000)
#         ]
#         await message.answer_invoice('Product nomi', 'mahsulot haqida', 'order_id=2', conf.bot.PAYMENT_CLICK_TOKEN,
#                                      'UZS', prices)
#
#
# @dp.pre_checkout_query()
# async def command_start_handler(pre_checkout_query: PreCheckoutQuery) -> None:
#     print('Tolov boshlanishi')
#     print(pre_checkout_query.invoice_payload)  # productning_idsi
#     print(pre_checkout_query.order_info)
#     await pre_checkout_query.answer(True)

start_router = Router()


@start_router.message(Command("start"))
async def command_start_handler(msg: Message) -> None:
    user: Optional[User] = await User.get(id_=msg.from_user.id)
    if user is None:
        user = {"id": msg.from_user.id, "username": msg.from_user.username,
                "full_name": f"{msg.from_user.full_name}", "lang": User.LangEnum(msg.from_user.language_code).name}
        await User.create(**user)

    await msg.answer(_("Hello, {}!").format(msg.from_user.full_name), reply_markup=main_menu_btn())


@start_router.message(UserState.choose_language)
async def choose_lang_handler(msg: Message, state: FSMContext, i18n: I18n):
    lang = "uz" if msg.text == __("Uzbek 🇺🇿") else 'en'
    await state.update_data({"locale": lang})
    i18n.current_locale = lang
    user = {"id": msg.from_user.id, "username": msg.from_user.username,
            "full_name": f"{msg.from_user.full_name}", "lang": User.LangEnum(lang).name}
    await User.create(**user)

    await msg.answer(__("Hello, {}!").format(msg.from_user.full_name), reply_markup=main_menu_btn())


@start_router.inline_query()
async def books_inline_query_handler(inline_query: InlineQuery):
    books = await Book.get_all()
    result = [InlineQueryResultArticle(
        id=str(book.title),
        title=book.title,
        thumbnail_url=str(book.photo),
        description=f"{book.description}\nNarxi: {book.price} {book.money_type.name}",
        input_message_content=InputTextMessageContent(message_text=book.title)) for book in books]

    await inline_query.answer(result)
