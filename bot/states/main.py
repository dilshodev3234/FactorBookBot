from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    choose_language = State()


class ButtonState(StatesGroup):
    main = State()
    category = State()
    choose_language = State()
