from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _, I18n
from aiogram.utils.i18n import lazy_gettext as __
from bot.buttons.reply import main_menu_btn, language_btn
from bot.dispatcher import dp
from bot.states.main import UserState, ButtonState
from config.enums.main import LangEnum
from db import User


@dp.message(UserState.choose_language)
async def choose_lang_handler(msg: Message, state: FSMContext):
    lang = "uz" if msg.text == __("Uzbek 🇺🇿") else 'en'
    await state.update_data({"locale": lang})
    user = {"id": msg.from_user.id, "username": msg.from_user.username,
            "full_name": f"{msg.from_user.full_name}", "lang": LangEnum(lang).name}
    await User.create(**user)
    await state.set_state(ButtonState.main)
    await msg.answer(_("Hello, {}!").format(msg.from_user.full_name), reply_markup=main_menu_btn())


@dp.message(F.text == __("🇺🇿 🔁 🇬🇧 Lang"),ButtonState.main)
async def choose_lang_handler(msg: Message, state: FSMContext):
    await state.set_state(ButtonState.choose_language)
    await msg.answer(text=_("Choose language :"), reply_markup=language_btn())

@dp.message(ButtonState.choose_language)
async def choose_lang_handler(msg: Message, state: FSMContext, i18n:I18n):
    lang = "uz" if msg.text == __("Uzbek 🇺🇿") else 'en'
    await state.update_data({"locale": lang})
    i18n.current_locale = lang
    await User.update(id_=msg.from_user.id, lang = LangEnum(lang).name)
    await state.set_state(ButtonState.main)
    await msg.answer(_("Hello, {}!").format(msg.from_user.full_name), reply_markup=main_menu_btn())
    print(123)



