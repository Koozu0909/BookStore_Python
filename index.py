from flask import render_template,request
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
    bks = utils.load_books(cate=cate)
    cate = utils.load_categorys()
    return render_template('productsList.html',
                            books=bks,cates=cate)


@app.route("/products/1")
def product():
    cate = utils.load_categorys()
    return render_template('sanpham.html',
                            cates=cate)

if __name__ == '__main__':

    app.run(debug=True)
