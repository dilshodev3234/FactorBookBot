from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db
from db.models import User, Category, Book, Order

app = Starlette()

admin = Admin(engine=db._engine, title="Example: SQLAlchemy")

admin.add_view(ModelView(User))
admin.add_view(ModelView(Category))
admin.add_view(ModelView(Book))
admin.add_view(ModelView(Order))

# Mount admin to your app
admin.mount_to(app)