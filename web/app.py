import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db, OrderItem
from db.models.models import User, Category, Book, Order
from web.provider import UsernameAndPasswordProvider
from starlette.middleware.sessions import SessionMiddleware
from config import conf

middleware = [
    Middleware(SessionMiddleware, secret_key=conf.web.SECRET_KEY)
]

app = Starlette(middleware=middleware)

logo_url = 'https://fiverr-res.cloudinary.com/images/q_auto,f_auto/gigs/346993714/original/d524eed3a6df4f37fe7e5f81d4c717b601117736/do-telegram-bot-with-python-aiogram.png'
admin = Admin(
    engine=db._engine,
    title="Aiogram Web Admin",
    base_url='/',
    logo_url=logo_url,
    auth_provider=UsernameAndPasswordProvider()
)

admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Book))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItem))

# Mount admin to your app
admin.mount_to(app)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
