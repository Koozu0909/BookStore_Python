from flask import render_template, request
from __init__ import app
import utils


@app.route('/')
def home():
    bks = utils.load_books()
    cate = utils.load_categorys()
    return render_template('index.html',
                           books=bks, cates=cate)


@app.route("/products")
def product_list():
    cate = request.args.get('genres')
    kw = request.args.get('keyword')
    price = request.args.get('price')
    bks = utils.load_books(cate=cate, kw=kw, price=price)
    cate = utils.load_categorys()
    return render_template('productsList.html',
                           books=bks, cates=cate)


@app.route("/products/<int:book_id>")
def product_detail(book_id):
    cate = utils.load_categorys()
    book = utils.get_book_by_id(book_id)
    return render_template('sanpham.html',
                           cates=cate, book=book)


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/login&res")
def login():
    return render_template('login&res.html')


if __name__ == '__main__':
    from admin import *
    app.run(debug=True)
