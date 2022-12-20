import hashlib
import json
import os
from sqlalchemy import func
from flask_login import current_user
from __init__ import app, db
from models import Category, Book, User, UserRole, Receipt, ReceiptDetail
from sqlalchemy.sql import extract


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def load_books(cate=None, kw=None, price=None, page=1):
    books = Book.query.filter(Book.active.__eq__(True))
    if cate:
        books = books.filter(Book.genres.__eq__(cate))

    if kw:
        books = books.filter(Book.name.contains(kw))

    if price:
        books = books.filter(Book.price.__lt__(price))

    page_size = app.config['PAGE_SIZE']
    start = (page-1)*page_size
    end = start + page_size

    return books.slice(start, end).all()
    # books = read_json(os.path.join(app.root_path, 'data/Books.json'))

    # if cate:
    #     books = [b for b in books if b['genres'] == cate]
    # if kw:
    #     books = [b for b in books if b['name'].lower().find(kw.lower()) >= 0]
    # if price:

    #     books = [b for b in books if b['price'] <= int(price)]

    # return books


def count_books():
    return Book.query.filter(Book.active.__eq__(True)).count()


def add_user(username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(username=username.strip(),
                password=password, email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))
    db.session.add(user)
    db.session.commit()


def check_user(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(
            password.strip().encode('utf-8')).hexdigest())
        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def load_categorys():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/Category.json'))


def get_book_by_id(book_id):
    return Book.query.get(book_id)


def count_cart(cart):
    total_quantity = 0
    total_amount = 0

    if cart:
        for c in cart.values():
            total_amount += c['quantity'] * c['price']
            total_quantity += c['quantity']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount

    }


def books_stats(kw=None, from_date=None, to_date=None):
    books = db.session.query(Book.id, Book.name, func.sum(ReceiptDetail.quantity*ReceiptDetail.unit_price))\
        .join(ReceiptDetail, ReceiptDetail.book_id.__eq__(Book.id), isouter=True)\
        .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
        .group_by(Book.id, Book.name)

    if kw:
        books = books.filter(Book.name.contains(kw))

    if from_date:
        books = books.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        books = books.filter(Receipt.created_date.__le__(to_date))

    return books.all()


def book_month_stats(year):
    return db.session.query(extract('month', Receipt.created_date), func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
        .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id))\
        .filter(extract('year', Receipt.created_date) == year)\
        .group_by(extract('month', Receipt.created_date)).all()


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(
                receipt=receipt, book_id=c['id'], quantity=c['quantity'], unit_price=c['price'])
            db.session.add(d)

        db.session.commit()


def category_stats():
    '''
    SELECT c.id, c.name, count(b.id)
    FROM category c left outer join book b on c.id = b.category_id
    group by c.id, c.name
    '''

    # return Category.query.join(Book, Book.category_id.__eq__(Category.id))\
    #     .add_columns(func.count(Book.id))\
    #     .group_by(Category.id, Category.name).all()

    return db.session.query(Category.id, Category.name, func.count(Book.id))\
        .join(Book, Category.id.__eq__(Book.category_id), isouter=True)\
        .group_by(Category.id, Category.name).all()
