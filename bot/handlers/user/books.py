from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import categories_inline_btn
from bot.dispatcher import dp
from bot.states.main import ButtonState


@dp.message(F.text == __("📚 Books"), ButtonState.main)
async def main_handler(msg: Message, state: FSMContext):
    ikm = await categories_inline_btn()
    await msg.answer(_("Select one of the categories"), reply_markup=ikm)
