from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from db import User


class Command(Filter):
    def __init__(self, my_text: str, prefix='/') -> None:
        self.my_text = f"{prefix}{my_text}"

    async def __call__(self, message: Message, state: FSMContext) -> bool:
        user: User = await User.get(id_=message.from_user.id)
        await state.clear()
        if user:
            await state.update_data({'locale': user.lang.value})

        return message.text == self.my_text
