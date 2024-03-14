from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    choose_language = State()


class ButtonState(StatesGroup):
    main = State()
    category = State()
    choose_language = State()


class OrderState(StatesGroup):
    category = State()
    order_cart = State()
    book = State()
    order = State()
    phone = State()
