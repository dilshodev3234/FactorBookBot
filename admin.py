from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db
from db.models.models import User, Category, Book, Order, OrderItem, Network

app = Starlette()

admin = Admin(engine=db._engine, title="Example: SQLAlchemy")

admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Book))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(OrderItem))
admin.add_view(ModelView(Network))


# Mount admin to your app
admin.mount_to(app)
