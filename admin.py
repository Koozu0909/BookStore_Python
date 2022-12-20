from __init__ import app, db
import hashlib
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView
from models import Category, Book, Tag, User, UserRole
from flask_login import current_user, logout_user
from flask import redirect, request
import utils
from datetime import datetime
import json


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class StaffModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.STAFF


class BookView(ModelView):
    can_view_details = True
    column_searchable_list = ('name', 'genres', 'description', 'author')

    def is_accessible(self):
        if (current_user.is_authenticated):
            if (current_user.user_role == UserRole.STAFF or current_user.user_role == UserRole.ADMIN):
                return True


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


class StatsView(BaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)
        return self.render('admin/stats.html',
                           month_stats=utils.book_month_stats(year=year),
                           stats=utils.books_stats(kw=kw,
                                                   from_date=from_date,
                                                   to_date=to_date))

    def is_accessible(self):
        if (current_user.is_authenticated):
            if (current_user.user_role == UserRole.STAFF or current_user.user_role == UserRole.ADMIN):
                return True


class StaffLogin(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/staff.html')

    def is_visible(self):
        if (current_user.is_authenticated):
            return False
        else:
            return True


class AdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        data = utils.category_stats()
        return self.render('admin/index.html', stats=data)


admin = Admin(app=app,
              name='BookStore Admin',
              template_mode='bootstrap4',
              index_view=AdminIndex())

admin.add_view(AdminModelView(Tag, db.session))
admin.add_view(AdminModelView(Category, db.session))
admin.add_view(AdminModelView(User, db.session))
admin.add_view(BookView(Book, db.session))
admin.add_view(StatsView(name='Stats'))
admin.add_view(StaffLogin(name='Staff'))
admin.add_view(LogoutView(name='LogOut'))
