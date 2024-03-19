from typing import Optional

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __

from bot.buttons.inline import categories_inline_btn, books_inline_btn, order_inline_btn
from bot.dispatcher import dp
from bot.states.main import ButtonState, OrderState
from db.enums.main import OrderStatusEnum
from db.models.models import Order, OrderItem, Category, Book


@dp.message(F.text == __("📚 Books"))
async def main_handler(msg: Message, state: FSMContext):
    order: Optional[Order] = await Order().get(user_id=msg.from_user.id)
    order_items = []
    if order:
        await state.update_data({"order_id": order.id})
        order_items = await OrderItem.filter(order_id=order.id)
    await state.set_state(OrderState.category)
    ikm = await categories_inline_btn(order_items)
    await msg.answer(_("Select one of the categories"), reply_markup=ikm)


@dp.callback_query(F.data == "cart", OrderState.category)
async def category_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    order_id = data.get("order_id")
    order_items: list[OrderItem] = await OrderItem.filter(order_id)
    text = _("🛒 Cart") + "\n\n"
    amount = 0
    for pos, order_item in enumerate(order_items, 1):
        book = await Book.get(order_item.book_id)
        summ = order_item.count * book.price
        amount += summ
        text += f"{pos}. {book.title}\n" + \
                f"{order_item.count} x {book.price} = {summ}\n\n"
    text += _("💲Total") + f": {amount} so'm"
    await state.set_state(OrderState.order_cart)
    await call.message.delete()
    ikm = await order_inline_btn()
    await call.message.answer(text, reply_markup=ikm)


@dp.callback_query(F.data == "❌", OrderState.order_cart)
async def order_cart_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await Order.delete(data.get("order_id"))
    ikm = await categories_inline_btn()
    await call.message.delete()
    await state.set_state(OrderState.category)
    await call.message.answer(text=_("Success clear"), reply_markup=ikm)


@dp.callback_query(F.data == "✅", OrderState.order_cart)
async def order_cart_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await Order.update(data.get("order_id"), status= OrderStatusEnum.APPROVED.name)
    ikm = await categories_inline_btn()
    await call.message.delete()
    await state.set_state(OrderState.category)
    await call.message.answer(text=_("Success order"), reply_markup=ikm)

@dp.callback_query(F.data == "back", OrderState.order_cart)
async def order_cart_handler(call: CallbackQuery, state: FSMContext):
    order: Optional[Order] = await Order().get(user_id=call.from_user.id)
    order_items = []
    if order:
        await state.update_data({"order_id": order.id})
        order_items = await OrderItem.filter(order_id=order.id)
    await state.set_state(OrderState.category)
    await call.message.delete()
    ikm = await categories_inline_btn(order_items)
    await call.message.answer(_("Select one of the categories"), reply_markup=ikm)


@dp.callback_query(OrderState.category)
async def category_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category: Category = await Category().get(id_=int(call.data))
    order_items = await OrderItem.filter(order_id=data.get("order_id"))
    await state.update_data({"category": category.name})
    books: list[Book] = await Book().filter(category_id=category.id)
    ikm = await books_inline_btn(books=books, order_items=order_items)
    await state.set_state(OrderState.book)
    await call.message.edit_text(text=category.name, reply_markup=ikm)
