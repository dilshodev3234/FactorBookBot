from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.reply import language_btn, main_menu_btn
from bot.dispatcher import dp
from bot.filters.main import Command
from bot.states.main import ButtonState, UserState
from db import User, Book
from db.enums.main import LangEnum


@dp.message(Command("start"))
async def command_start_handler(message: Message, state: FSMContext) -> None:
    user: User = await User.get(id_=message.from_user.id)
    if user:
        await state.set_state(ButtonState.main)
        await message.answer(_("Hello, {}!").format(user.full_name), reply_markup=main_menu_btn())
    else:
        await state.set_state(UserState.choose_language)
        await message.answer(text=_("Choose language :"), reply_markup=language_btn())


@dp.message(UserState.choose_language)
async def choose_lang_handler(msg: Message, state: FSMContext):
    lang = "uz" if msg.text == __("Uzbek 🇺🇿") else 'en'
    await state.update_data({"locale": lang})
    user = {"id": msg.from_user.id, "username": msg.from_user.username,
            "full_name": f"{msg.from_user.full_name}", "lang": LangEnum(lang).name}
    await User.create(**user)
    await state.set_state(ButtonState.main)
    await msg.answer(__("Hello, {}!").format(msg.from_user.full_name),reply_markup=main_menu_btn())


@dp.inline_query()
async def books_inline_query_handler(inline_query: InlineQuery):
    books = await Book.get_all()
    result = [InlineQueryResultArticle(
            id=str(book.title),
            title=book.title,
            thumbnail_url=str(book.photo),
            description=f"{book.description}\nNarxi: {book.price} {book.money_type.name}",
            input_message_content=InputTextMessageContent(message_text=book.title)) for book in books]

    await inline_query.answer(result)





