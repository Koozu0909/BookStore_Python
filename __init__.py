from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = '$@F!#GWWT#$^@#GWT#GWGWG'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:kiet741852963@localhost/bookstore?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
