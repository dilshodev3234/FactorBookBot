from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from bot.buttons.inline import categories_inline_btn, product_order_inline_btn
from bot.dispatcher import dp
from bot.states.main import OrderState
from db.models.models import Order, OrderItem, Book


@dp.callback_query(OrderState.book)
async def category_handler(call: CallbackQuery, state: FSMContext):
    book_caption = _('🔹 Title') + \
                   ": {}\n" + _('Category') + \
                   ": {}\n" + _('Description') + \
                   ": {}\n" + _('Page') + \
                   ": {}\n" + _('Vol') + \
                   ": {}\n" + _('Price')
    data = await state.get_data()
    book: Book = await Book().get(id_= int(call.data))
    await state.set_state(OrderState.order)
    await call.message.delete()
    data["count"] = data.get("count" , 0) + 1
    data["book_id"] = int(call.data)
    await state.set_data(data)
    ikm = await product_order_inline_btn(data.get("count"))
    caption = book_caption.format(book.title , data.get("category") , book.description, book.page , book.vol.name , book.price)
    await call.message.answer_photo(photo=book.photo,caption=caption ,reply_markup=ikm)


@dp.callback_query(OrderState.order)
async def choose_order_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    count = data.get("count")
    match call.data:
        case "-":
            ikm = await product_order_inline_btn(count - 1)
            await state.update_data({"count": count - 1})
            await call.message.edit_reply_markup(call.inline_message_id, reply_markup=ikm)

        case "+":
            ikm = await product_order_inline_btn(count + 1)
            await state.update_data({"count": count + 1})
            await call.message.edit_reply_markup(call.inline_message_id, reply_markup=ikm)

        case "back":
            await call.message.delete()
            ikm = await categories_inline_btn()
            await call.message.answer(_("Select one of the categories"), reply_markup=ikm)

        case "cart":
            order = await Order().get(user_id=call.from_user.id)
            if not order:
                await Order.create(user_id= call.from_user.id)
            order: Order = await Order().get(user_id=call.from_user.id)
            book_id = data.get("book_id")
            await OrderItem.create(count = count , book_id = book_id, order_id = order.id)
            order_items = await OrderItem.filter(order_id=order.id)
            await call.message.delete()
            ikm = await categories_inline_btn(order_items)
            await state.clear()
            await state.update_data({"order_id" : order.id})
            await state.set_state(OrderState.category)
            await call.message.answer(_("Select one of the categories"), reply_markup=ikm)

