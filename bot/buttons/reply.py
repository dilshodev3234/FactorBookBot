from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def language_btn():
    rkm = ReplyKeyboardBuilder()
    rkm.add(*[
        KeyboardButton(text=_("Uzbek 🇺🇿")),
        KeyboardButton(text=_("Enlish 🇬🇧"))
    ])
    return rkm.as_markup(resize_keyboard=True)


def main_menu_btn():
        rkm = ReplyKeyboardBuilder()
        rkm.add(*[
            KeyboardButton(text=_("📚 Books")),
            KeyboardButton(text=_("📃 My Order")),
            KeyboardButton(text=_("🔵 We network")),
            KeyboardButton(text=_("📞 Contact us")),
            KeyboardButton(text=_("🇺🇿 🔁 🇬🇧 Lang"))
        ])
        rkm.adjust(1, 1, 2)
        return rkm.as_markup(resize_keyboard=True)
