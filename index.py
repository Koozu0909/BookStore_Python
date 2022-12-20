import math
from flask import render_template, request, redirect, url_for, session, jsonify
from __init__ import app, login
from models import UserRole
import utils
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required


@app.route('/')
def home():
    bks = utils.load_books()
    return render_template('index.html',
                           books=bks)


@app.route("/products")
def product_list():
    cate = request.args.get('genres')
    kw = request.args.get('keyword')
    price = request.args.get('price')
    page = request.args.get('page', 1)
    bks = utils.load_books(cate=cate, kw=kw, price=price, page=int(page))

    counter = utils.count_books()
    return render_template('productsList.html',
                           books=bks, pages=math.ceil(counter/app.config['PAGE_SIZE']))


@app.route("/products/<int:book_id>")
def product_detail(book_id):
    book = utils.get_book_by_id(book_id)
    return render_template('sanpham.html',
                           book=book)


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    image = data.get('image')

    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'image': image,
            'quantity': 1
        }

    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route("/cart")
def cart():
    return render_template('cart.html')


@app.route("/api/pay", methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 400})

    return jsonify({'code': 200})


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/cart/<int:book_id>', methods=['delete'])
def delete_cart(book_id):
    data = request.json
    cart = session.get('cart')
    id = str(data.get('book_id'))
    if cart and id in cart:
        del cart[id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.context_processor
def common_response():
    return {
        'cates': utils.load_categorys(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@login.user_loader
def get_user(user_id):
    try:
        return utils.get_user_by_id(user_id=user_id)
    except:
        return None


@app.route("/login", methods=['get', 'post'])
def login():
    err_msg = ' '
    if request.method.__eq__('POST'):
        username_check = request.form.get('username-check')
        password_check = request.form.get('password-check')

        user = utils.check_user(username=username_check,
                                password=password_check)
        if user:
            login_user(user=user)
            next = request.args.get('next', 'home')
            return redirect(url_for(next))
        else:
            err_msg = 'username or pass not right'

    return render_template('login.html', err_msg=err_msg)


@app.route("/user-logout")
def user_signout():

    ()
    return redirect(url_for('login'))


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ' '
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None

        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(username=username,
                               password=password, email=email, avatar=avatar_path)
                return redirect(url_for('login'))
            else:
                err_msg = 'Mat Khau Ko Khop'
        except Exception as ex:
            err_msg = 'ERROR' + str(ex)

    return render_template('register.html', err_msg=err_msg)


@app.route('/admin-login', methods=['post'])
def signin_admin():
    err_msg = ' '
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user(username=username,
                            password=password,
                            role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/staff-login', methods=['post'])
def signin_staff():
    err_msg = ' '
    username = request.form.get('username')
    password = request.form.get('password')

    user = utils.check_user(username=username,
                            password=password,
                            role=UserRole.STAFF)
    if user:
        login_user(user=user)

    return redirect('/admin')


    # @login.user_loader
    # def user_load(user_id):
    #     return utils.get_book_by_id(user_id)
if __name__ == '__main__':
    from admin import *
    app.run(debug=True)
