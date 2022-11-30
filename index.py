from flask import render_template
from __init__ import app
import utils


@app.route('/')
def home():
    bks =  utils.load_books()
    return render_template('index.html',
                            books = bks)


if __name__ == '__main__':
    app.run(debug = True)