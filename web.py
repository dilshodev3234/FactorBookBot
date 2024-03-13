from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin, ModelView

from db import db, User, Order , Book , Network
from db.models.models import Category

app = Starlette()  # FastAPI()

# Create admin
admin = Admin(db._engine ,title="Example: SQLAlchemy")

# Add view
admin.add_view(ModelView(User))
admin.add_view(ModelView(Order))
admin.add_view(ModelView(Book))
admin.add_view(ModelView(Network))
admin.add_view(ModelView(Category))

# Mount admin to your app
admin.mount_to(app)