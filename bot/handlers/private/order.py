from aiogram import F, Router
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton
from aiogram.utils.i18n import gettext as _
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.buttons.inline import categories_inline_btn, product_order_inline_btn
from bot.buttons.reply import phone_btn
from bot.states.main import OrderState
from db import Order, OrderItem, Book, User

order_router = Router()


@order_router.callback_query(OrderState.book)
async def category_handler(call: CallbackQuery, state: FSMContext):
    book_caption = _('🔹 Title') + \
                   ": {}\n" + _('Category') + \
                   ": {}\n" + _('Description') + \
                   ": {}\n" + _('Page') + \
                   ": {}\n" + _('Vol') + \
                   ": {}\n" + _('Price')
    data = await state.get_data()
    book: Book = await Book().get(id_=int(call.data))
    await state.set_state(OrderState.order)
    await call.message.delete()
    data["count"] = data.get("count", 0) + 1
    data["book_id"] = int(call.data)
    await state.set_data(data)
    ikm = await product_order_inline_btn(data.get("count"))
    caption = book_caption.format(book.title, data.get("category"), book.description, book.page, book.vol.name,
                                  book.price)
    await call.message.answer_photo(photo=book.photo, caption=caption, reply_markup=ikm)


@order_router.callback_query(OrderState.order)
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
                await Order.create(user_id=call.from_user.id)
            order: Order = await Order().get(user_id=call.from_user.id)
            book_id = data.get("book_id")
            await OrderItem.create(count=count, book_id=book_id, order_id=order.id)
            order_items = await OrderItem.filter(order_id=order.id)
            await call.message.delete()
            ikm = await categories_inline_btn(order_items)
            await state.clear()
            await state.update_data({"order_id": order.id})

            await state.set_state(OrderState.phone)
            text = _('Telefon raqamingizni qoldiring: (Telefon raqam)')
            await call.message.answer(text, reply_markup=phone_btn())


@order_router.message(F.content_type.in_({ContentType.CONTACT}), OrderState.phone)
async def choose_order_handler(message: Message, state: FSMContext):
    await User.update(message.from_user.id, phone_number=message.contact.phone_number)
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
    text += _("💲Total") + (f": {amount} so'm\n"
                           f"Telefon raqamingiz: {message.contact.phone_number}")
    text += 'Buyurtma berasizmi ?'
    ikm = InlineKeyboardBuilder()
    ikm.row(*[
        InlineKeyboardButton(text='Yoq', callback_data='confirmation_order_0'),
        InlineKeyboardButton(text='Xa', callback_data='confirmation_order_1')
    ])
    await message.answer(text, reply_markup=ikm.as_markup())
