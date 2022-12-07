from __init__ import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Category, Book


admin = Admin(app=app, name='BookStore Admin', template_mode='bootstrap4')


class BookView(ModelView):
    can_view_details = True
    column_searchable_list = ('name', 'genres', 'description', 'author')


admin.add_view(ModelView(Category, db.session))
admin.add_view(BookView(Book, db.session))
