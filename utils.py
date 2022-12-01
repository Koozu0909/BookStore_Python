import json, os
from __init__ import app


def read_json(path):
    with open(path,'r') as f:
        data = json.load(f)

    return data

def load_books(cate=None, kw =None, from_frice=None, to_price=None):
    books = read_json(os.path.join(app.root_path, 'data/Books.json'))

    if cate:
        books = [b for b in books if b['genres'] == cate]

    return books

def load_categorys():
    return read_json(os.path.join(app.root_path, 'data/Category.json'))