import os
from typing import Any, Dict, Union

import anyio.to_thread
import uvicorn
from libcloud.storage.drivers.local import LocalStorageDriver
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    Session,
)
from sqlalchemy_file.storage import StorageManager
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette_admin.contrib.sqla import Admin, ModelView

from config import conf
from db import OrderItem, User, Category, Book, Order, database
from web.provider import UsernameAndPasswordProvider

middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY)
]

app = Starlette(middleware=middleware)

logo_url = 'https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/346993714/original/d524eed3a6df4f37fe7e5f81d4c717b601117736/do-telegram-bot-with-python-aiogram.png'
admin = Admin(
    engine=database._engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider()
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))


class BookModelView(ModelView):
    exclude_fields_from_list = ('created_at', 'updated_at', 'order_items', 'vol')
    exclude_fields_from_create = ('created_at', 'updated_at', 'order_items')
    exclude_fields_from_edit = ('created_at', 'updated_at')


admin.add_view(BookModelView(Book))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItem))

# Mount admin to your app
admin.mount_to(app)

# Configure Storage
os.makedirs("./media/attachment", 0o777, exist_ok=True)
container = LocalStorageDriver("./media").get_container("attachment")
StorageManager.add_storage("default", container)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
    # 10.10.1.92
