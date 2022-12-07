import json
import os
from __init__ import app
from models import Category, Book


def read_json(path):
    with open(path, 'r') as f:
        data = json.load(f)

    return data


def load_books(cate=None, kw=None, price=None):
    books = Book.query.filter(Book.active.__eq__(True))
    if cate:
        books = books.filter(Book.genres.__eq__(cate))

    if kw:
        books = books.filter(Book.name.contains(kw))

    if price:
        books = books.filter(Book.price.__lt__(price))

    return books
    # books = read_json(os.path.join(app.root_path, 'data/Books.json'))

    # if cate:
    #     books = [b for b in books if b['genres'] == cate]
    # if kw:
    #     books = [b for b in books if b['name'].lower().find(kw.lower()) >= 0]
    # if price:

    #     books = [b for b in books if b['price'] <= int(price)]

    # return books


def load_categorys():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/Category.json'))


def get_book_by_id(book_id):
    return Book.query.get(book_id)
    # books = read_json(os.path.join(app.root_path, 'data/Books.json'))

    # for b in books:
    #     if b['id'] == book_id:
    #         return b

    # return None
